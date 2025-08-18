import csv
import os

def problem1_revised():
    try:
        # 현재 py 파일 위치 기준으로 CSV 경로 설정
        # 사용자 환경에 맞게 파일 경로를 설정해야 합니다.
        # 예: file_path = "Mars_Base_Inventory_List.csv"
        base_dir = os.path.dirname(__file__) if '__file__' in locals() else os.getcwd()
        file_path = os.path.join(base_dir, "Mars_Base_Inventory_List.csv")

        inventory = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # 첫 줄 헤더 가져오기

            # 실제 CSV 파일은 5개의 열을 가집니다.
            for row in reader:
                # 1. 열 개수 확인 로직 수정
                if len(row) != 5:
                    print("⚠️ 잘못된 행 무시:", row)
                    continue
                try:
                    # 2. 올바른 열에서 데이터 추출
                    name = row[0].strip()
                    # 수량(qty)은 두 번째 열(Weight)을 사용, 숫자 변환이 불가능하면 0으로 처리
                    try:
                        qty = float(row[1].strip())
                    except ValueError:
                        qty = 0 # 'Various'와 같은 문자열은 0으로 처리
                    # 인화성(flam)은 다섯 번째 열에서 추출
                    flam = float(row[4].strip())

                    inventory.append([name, qty, flam])
                except (ValueError, IndexError):
                    print("⚠️ 데이터 처리 실패:", row)
                    continue

        # === 출력 ===
        print("\n=== 전체 적재물 목록 ===")
        for item in inventory:
            print(item)

        # === 정렬 (flammability 기준 내림차순) ===
        inventory_sorted = sorted(inventory, key=lambda x: x[2], reverse=True)
        print("\n=== 인화성 지수 기준 내림차순 정렬 ===")
        for item in inventory_sorted:
            print(item)

        # === 필터링 (인화성 ≥ 0.7) ===
        danger_items = [item for item in inventory_sorted if item[2] >= 0.7]
        print("\n=== 위험 물품 목록 (인화성 ≥ 0.7) ===")
        for item in danger_items:
            print(item)

        # === CSV 저장 ===
        danger_file = os.path.join(base_dir, "Mars_Base_Inventory_danger.csv")
        with open(danger_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # 저장할 파일의 헤더는 3개 열에 맞게 수정
            writer.writerow(['Substance', 'Quantity (Weight)', 'Flammability'])
            for item in danger_items:
                # item[1]은 수량(무게), item[2]는 인화성 지수
                writer.writerow([item[0], f"{item[1]:.3f}", f"{item[2]:.3f}"])

        print(f"\n✅ 위험 물품 목록이 저장되었습니다 → {danger_file}")

    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        print("❌ 예기치 못한 오류:", e)

# 함수 호출
problem1_revised()