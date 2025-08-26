# cctv.py
# 딥러닝(DNN) 모델을 사용한 최종 완성 버전

import sys
import os
import zipfile
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

CCTV_ZIP_FILE = 'CCTV.zip'
CCTV_FOLDER = 'CCTV'
# --- 딥러닝 모델 파일 경로 및 신뢰도 임계값 ---
MODEL_PATH = 'models/deploy.prototxt.txt'
WEIGHT_PATH = 'models/res10_300x300_ssd_iter_140000_fp16.caffemodel'
# 신뢰도 60% 이상인 것만 얼굴로 판단 (탐지가 잘 안되면 0.3 ~ 0.5 사이로 낮춰보세요)
CONFIDENCE_THRESHOLD = 0.15
# ---------------------------------------------

class CCTVManager(QWidget):
    def __init__(self):
        super().__init__()
        self.image_files = []
        self.current_index = 0
        self.mode = 'viewer'

        # 딥러닝(DNN) 얼굴 탐지기 로드
        if not (os.path.exists(MODEL_PATH) and os.path.exists(WEIGHT_PATH)):
            QMessageBox.critical(self, "오류", "딥러닝 모델 파일이 없습니다.\n'models' 폴더와 그 안의 파일들을 확인하세요.")
            sys.exit()
        self.net = cv2.dnn.readNetFromCaffe(MODEL_PATH, WEIGHT_PATH)

        self.init_ui()
        self.prepare_images()
        self.set_viewer_mode()

    def init_ui(self):
        self.setWindowTitle('CCTV 통합 관리 시스템 (DNN 최종 버전)')
        self.setGeometry(200, 200, 800, 650)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.viewer_mode_button = QPushButton('뷰어 모드')
        self.detector_mode_button = QPushButton('얼굴 탐지 모드')
        hbox = QHBoxLayout()
        hbox.addWidget(self.viewer_mode_button)
        hbox.addWidget(self.detector_mode_button)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.image_label, 1)
        self.setLayout(vbox)
        self.viewer_mode_button.clicked.connect(self.set_viewer_mode)
        self.detector_mode_button.clicked.connect(self.set_detector_mode)

    def prepare_images(self):
        # CCTV.zip 파일 압축 해제
        if not os.path.exists(CCTV_FOLDER) and os.path.exists(CCTV_ZIP_FILE):
            print(f"'{CCTV_ZIP_FILE}' 파일의 압축을 해제합니다...")
            with zipfile.ZipFile(CCTV_ZIP_FILE, 'r') as zip_ref:
                zip_ref.extractall('.')
            print("압축 해제 완료.")
        
        # 이미지 파일 목록 로드
        if os.path.exists(CCTV_FOLDER):
            try:
                files = os.listdir(CCTV_FOLDER)
                self.image_files = sorted([
                    os.path.join(CCTV_FOLDER, f) for f in files
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ])
                if not self.image_files:
                    self.show_message("오류", "CCTV 폴더에 이미지 파일이 없습니다.")
            except Exception as e:
                self.show_message("오류", f"파일을 읽는 중 오류 발생: {e}")
        else:
            self.show_message("오류", f"'{CCTV_FOLDER}' 폴더를 찾을 수 없습니다. CCTV.zip 파일이 있는지 확인하세요.")

    def set_viewer_mode(self):
        self.mode = 'viewer'
        self.status_label.setText("뷰어 모드: 좌/우 방향키로 이미지를 넘겨보세요.")
        self.viewer_mode_button.setEnabled(False)
        self.detector_mode_button.setEnabled(True)
        self.show_viewer_image()

    def set_detector_mode(self):
        self.mode = 'detector'
        self.current_index = 0
        self.status_label.setText("얼굴 탐지 모드: 첫 번째 얼굴을 찾는 중...")
        self.image_label.setText("탐색 중...")
        self.viewer_mode_button.setEnabled(True)
        self.detector_mode_button.setEnabled(False)
        QApplication.processEvents()
        self.search_for_face()

    def show_viewer_image(self):
        if not self.image_files: return
        image_path = self.image_files[self.current_index]
        pixmap = QPixmap(image_path)
        self.display_pixmap(pixmap)
        print(f"뷰어: {os.path.basename(image_path)} ({self.current_index + 1}/{len(self.image_files)})")

    def search_for_face(self):
        if not self.image_files or self.current_index >= len(self.image_files):
            self.show_message("탐색 완료", "모든 사진의 검색이 끝났습니다.")
            self.status_label.setText("얼굴 탐지 모드: 탐색이 완료되었습니다.")
            return

        print(f"{self.current_index + 1}번째 사진부터 탐색을 시작합니다...")
        face_found_in_any_image = False

        for i in range(self.current_index, len(self.image_files)):
            image_path = self.image_files[i]
            frame = cv2.imread(image_path)
            if frame is None: continue

            (h, w) = frame.shape[:2]
            # 원본 이미지에서 blob 생성 (자동 리사이즈 및 정규화)
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            
            self.net.setInput(blob)
            detections = self.net.forward()
            
            found_count = 0
            # 탐지 결과 순회
            for j in range(0, detections.shape[2]):
                confidence = detections[0, 0, j, 2]

                # 신뢰도가 설정된 임계값보다 높은 경우만 처리
                if confidence > CONFIDENCE_THRESHOLD:
                    found_count += 1
                    # 바운딩 박스 좌표 계산
                    box = detections[0, 0, j, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # 사각형 및 신뢰도 텍스트 그리기
                    text = f"{confidence * 100:.2f}%"
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

            if found_count > 0:
                print(f"얼굴 발견! -> {os.path.basename(image_path)} ({found_count}명)")
                self.current_index = i
                self.status_label.setText(f"얼굴 발견: {os.path.basename(image_path)}\nEnter 키로 다음 탐색")
                self.display_cv_image(frame)
                face_found_in_any_image = True
                return

        if not face_found_in_any_image:
            self.current_index = len(self.image_files)
            self.show_message("탐색 완료", "더 이상 얼굴을 찾지 못했습니다.\n모든 사진의 검색이 끝났습니다.")
            self.status_label.setText("얼굴 탐지 모드: 탐색이 완료되었습니다.")

    def display_cv_image(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.display_pixmap(pixmap)

    def display_pixmap(self, pixmap):
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if self.mode == 'viewer':
            if not self.image_files: return
            if key == Qt.Key_Right:
                self.current_index = (self.current_index + 1) % len(self.image_files)
                self.show_viewer_image()
            elif key == Qt.Key_Left:
                self.current_index = (self.current_index - 1 + len(self.image_files)) % len(self.image_files)
                self.show_viewer_image()
        elif self.mode == 'detector':
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                self.status_label.setText("다음 얼굴을 찾는 중...")
                QApplication.processEvents()
                self.current_index += 1
                self.search_for_face()

    def resizeEvent(self, event):
        current_pixmap = self.image_label.pixmap()
        if current_pixmap and not current_pixmap.isNull():
            self.display_pixmap(current_pixmap)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = CCTVManager()
    manager.show()
    sys.exit(app.exec_())