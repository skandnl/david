import math

# 전역 변수 저장용
last_result = {}

def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적(m^2)과 무게(kg)를 계산
    diameter: 지름 (m)
    material: 'glass', 'aluminum', 'carbon_steel'
    thickness: 두께 (cm), 기본값 1
    """
    # 재질별 밀도 (g/cm^3)
    densities = {
        "glass": 2.4,
        "aluminum": 2.7,
        "carbon_steel": 7.85
    }

    # 입력 검증
    if material not in densities:
        raise ValueError("재질은 glass, aluminum, carbon_steel 중 하나여야 합니다.")
    if diameter <= 0:
        raise ValueError("지름은 0보다 커야 합니다.")
    if thickness <= 0:
        raise ValueError("두께는 0보다 커야 합니다.")

    radius = diameter / 2.0  # m
    area = 2 * math.pi * (radius ** 2)  # 반구 표면적 (m^2)

    # 두께와 면적을 부피로 변환 (cm^3 단위로 변환)
    thickness_m = thickness / 100.0  # cm → m
    volume_m3 = area * thickness_m  # m^3
    volume_cm3 = volume_m3 * 1e6    # m^3 → cm^3

    # 질량(g) → kg 변환
    mass_g = volume_cm3 * densities[material]
    mass_kg = mass_g / 1000.0

    # 화성 중력 반영 (0.38배)
    mass_mars = mass_kg * 0.38

    # 전역 변수 저장
    global last_result
    last_result = {
        "material": material,
        "diameter": diameter,
        "thickness": thickness,
        "area": round(area, 3),
        "weight": round(mass_mars, 3)
    }

    return last_result


def main():
    print("=== Mars Dome Design Program ===")
    while True:
        try:
            material = input("재질을 입력하세요 (glass/aluminum/carbon_steel, 종료하려면 'q'): ").strip()
            if material.lower() == 'q':
                print("프로그램을 종료합니다.")
                break

            diameter = float(input("지름을 입력하세요 (m): ").strip())
            thickness_input = input("두께를 입력하세요 (cm, 기본값=1): ").strip()
            thickness = float(thickness_input) if thickness_input else 1.0

            result = sphere_area(diameter, material, thickness)

            print(f"재질 ⇒ {result['material']}, 지름 ⇒ {result['diameter']}, "
                  f"두께 ⇒ {result['thickness']}, 면적 ⇒ {result['area']}, "
                  f"무게 ⇒ {result['weight']} kg")

        except ValueError as ve:
            print(f"입력 오류: {ve}")
        except Exception as e:
            print(f"예기치 못한 오류 발생: {e}")

if __name__ == "__main__":
    main()
