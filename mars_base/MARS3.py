import numpy as np

def problem3():
    while True:
        try:
            # CSV 파일 읽기
            arr1 = np.genfromtxt("mars_base_main_parts-001.csv", delimiter=",", skip_header=1, dtype=str)
            arr2 = np.genfromtxt("mars_base_main_parts-002.csv", delimiter=",", skip_header=1, dtype=str)
            arr3 = np.genfromtxt("mars_base_main_parts-003.csv", delimiter=",", skip_header=1, dtype=str)

            # 세 배열 병합
            parts = np.vstack((arr1, arr2, arr3))

            # 숫자 부분만 추출 (2열 = strength)
            values = parts[:, 1].astype(float)

            # 항목별 평균값 계산 (소수점 3자리 제한)
            avg_strength = round(np.mean(values), 3)
            print(f"\n전체 항목 Strength 평균: {avg_strength:.3f}")

            # strength < 50 필터링
            filtered = parts[values < 50]

            if filtered.size > 0:
                print("\nStrength < 50 항목:")
                for row in filtered:
                    print(f"{row[0]} → {float(row[1]):.3f}")
            else:
                print("\n조건에 맞는 항목이 없습니다.")

            # CSV 저장 (예외 처리 포함)
            try:
                np.savetxt(
                    "parts_to_work_on.csv",
                    filtered,
                    delimiter=",",
                    fmt="%s",
                    header="parts,strength",
                    comments=""
                )
                print("\n✅ parts_to_work_on.csv 저장 완료")
            except Exception as e:
                print(f"\n⚠️ 파일 저장 중 오류 발생: {e}")

        except Exception as e:
            print(f"\n⚠️ 실행 오류: {e}")

        # 반복 실행 여부
        again = input("\n다시 실행할까요? (y/n): ").strip().lower()
        if again != "y":
            print("문제 3을 종료합니다.")
            break


# 이 파일을 직접 실행했을 때만 동작
if __name__ == "__main__":
    problem3()
