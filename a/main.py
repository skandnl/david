import json
import os

def main():
    log_file = "mission_computer_main.log"
    json_file = "mission_computer_main.json"
    
    try:
        # 1️⃣ 파일 읽기
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print("=== 로그 파일 전체 내용 ===")
        print("".join(lines))
        
        # 2️⃣ 콤마로 분리 → 리스트 변환
        log_list = []
        for line in lines:
            parts = line.strip().split(",", 1)  # 첫 번째 콤마만 분리
            if len(parts) == 2:
                log_list.append([parts[0].strip(), parts[1].strip()])
        
        print("\n=== 리스트 객체 ===")
        print(log_list)
        
        # 3️⃣ 시간 역순 정렬 (날짜/시간이 첫 번째 요소)
        sorted_list = sorted(log_list, key=lambda x: x[0], reverse=True)
        print("\n=== 시간 역순 정렬된 리스트 ===")
        print(sorted_list)
        
        # 4️⃣ Dict로 변환
        log_dict = {entry[0]: entry[1] for entry in sorted_list}
        print("\n=== Dict 객체 ===")
        print(log_dict)
        
        # 5️⃣ JSON 파일 저장
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(log_dict, jf, ensure_ascii=False, indent=4)
        print(f"\n✅ 변환된 Dict 객체가 '{json_file}' 파일로 저장되었습니다.")
    
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {log_file}")
    except UnicodeDecodeError:
        print("❌ 파일 디코딩 중 오류가 발생했습니다. UTF-8 인코딩을 확인하세요.")
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")

if __name__ == "__main__":
    main()

