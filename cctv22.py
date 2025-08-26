# cctv.py
# 이미지 뷰어와 사람 탐지 기능이 통합된 버전 (탐지 모드 로직 수정)

import sys
import os
import zipfile
import cv2  # OpenCV 라이브러리
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

CCTV_ZIP_FILE = 'CCTV.zip'
CCTV_FOLDER = 'CCTV'

class CCTVManager(QWidget):
    """
    CCTV 이미지 뷰어와 사람 탐지 기능을 모두 관리하는 통합 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.image_files = []
        self.current_index = 0
        self.mode = 'viewer'  # 'viewer' 또는 'detector'

        # OpenCV의 HOG 기반 사람 탐지기 초기화
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        self.init_ui()
        self.prepare_images()
        
        # 초기 모드는 뷰어 모드로 설정
        self.set_viewer_mode()

    def init_ui(self):
        """UI를 초기화하고 설정합니다."""
        self.setWindowTitle('CCTV 통합 관리 시스템')
        self.setGeometry(200, 200, 800, 650)

        # --- 위젯 생성 ---
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.viewer_mode_button = QPushButton('뷰어 모드')
        self.detector_mode_button = QPushButton('사람 탐지 모드')

        # --- 레이아웃 설정 ---
        hbox = QHBoxLayout()
        hbox.addWidget(self.viewer_mode_button)
        hbox.addWidget(self.detector_mode_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.image_label, 1)
        self.setLayout(vbox)
        
        # --- 이벤트 핸들러 연결 ---
        self.viewer_mode_button.clicked.connect(self.set_viewer_mode)
        self.detector_mode_button.clicked.connect(self.set_detector_mode)

    def prepare_images(self):
        """CCTV.zip 파일의 압축을 풀고 이미지 목록을 불러옵니다."""
        if not os.path.exists(CCTV_FOLDER) and os.path.exists(CCTV_ZIP_FILE):
            print(f"'{CCTV_ZIP_FILE}' 파일의 압축을 해제합니다...")
            with zipfile.ZipFile(CCTV_ZIP_FILE, 'r') as zip_ref:
                zip_ref.extractall('.')
            print("압축 해제 완료.")
        
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
            self.show_message("오류", f"'{CCTV_FOLDER}' 폴더를 찾을 수 없습니다.")

    # --- 모드 전환 함수 ---
    def set_viewer_mode(self):
        """뷰어 모드로 전환합니다."""
        self.mode = 'viewer'
        self.status_label.setText("뷰어 모드: 좌/우 방향키로 이미지를 넘겨보세요.")
        self.viewer_mode_button.setEnabled(False)
        self.detector_mode_button.setEnabled(True)
        self.show_viewer_image()

    def set_detector_mode(self):
        """사람 탐지 모드로 전환하고 즉시 첫 탐색을 시작합니다."""
        self.mode = 'detector'
        self.current_index = 0
        self.status_label.setText("사람 탐지 모드: 첫 번째 사람을 찾는 중...")
        self.image_label.setText("탐색 중...")
        self.viewer_mode_button.setEnabled(True)
        self.detector_mode_button.setEnabled(False)
        QApplication.processEvents() # UI가 즉시 업데이트되도록 함
        
        # *** 수정된 부분: 모드 전환 시 바로 첫 탐색 시작 ***
        self.search_for_person()

    # --- 핵심 기능 함수 ---
    def show_viewer_image(self):
        """(뷰어 모드) 현재 인덱스의 이미지를 표시합니다."""
        if not self.image_files: return
        
        image_path = self.image_files[self.current_index]
        pixmap = QPixmap(image_path)
        self.display_pixmap(pixmap)
        print(f"뷰어: {image_path} ({self.current_index + 1}/{len(self.image_files)})")

    def search_for_person(self):
        """(탐지 모드) 현재 인덱스부터 사람을 탐색합니다."""
        if not self.image_files or self.current_index >= len(self.image_files):
            self.show_message("탐색 완료", "모든 사진의 검색이 끝났습니다.")
            self.status_label.setText("사람 탐지 모드: 탐색이 완료되었습니다.")
            return

        print(f"{self.current_index + 1}번째 사진부터 탐색을 시작합니다...")
        
        for i in range(self.current_index, len(self.image_files)):
            image_path = self.image_files[i]
            frame = cv2.imread(image_path)
            if frame is None: continue

            (rects, weights) = self.hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
            
            if len(rects) > 0:
                print(f"사람 발견! -> {image_path}")
                self.current_index = i
                self.status_label.setText(f"사람 발견: {os.path.basename(image_path)}\nEnter 키로 다음 탐색")
                self.display_cv_image(frame)
                return

        self.current_index = len(self.image_files)
        self.show_message("탐색 완료", "더 이상 사람을 찾지 못했습니다.\n모든 사진의 검색이 끝났습니다.")
        self.status_label.setText("사람 탐지 모드: 탐색이 완료되었습니다.")

    # --- UI 헬퍼 함수 ---
    def display_cv_image(self, cv_image):
        """OpenCV 이미지를 PyQt 위젯에 표시합니다."""
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.display_pixmap(pixmap)

    def display_pixmap(self, pixmap):
        """QPixmap 객체를 창 크기에 맞게 스케일링하여 표시합니다."""
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def keyPressEvent(self, event):
        """키보드 입력을 모드에 따라 다르게 처리합니다."""
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
                self.status_label.setText("다음 사람을 찾는 중...")
                QApplication.processEvents()
                self.current_index += 1
                self.search_for_person()

    def resizeEvent(self, event):
        """창 크기 변경 시 현재 표시된 이미지를 다시 스케일링합니다."""
        current_pixmap = self.image_label.pixmap()
        if current_pixmap and not current_pixmap.isNull():
            self.display_pixmap(current_pixmap)
            
    def show_message(self, title, message):
        """사용자에게 메시지 상자를 보여줍니다."""
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = CCTVManager()
    manager.show()
    sys.exit(app.exec_())
