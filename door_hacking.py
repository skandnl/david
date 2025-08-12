import zipfile
import time


def unlock_zip(zip_filename='emergency_storage_key.zip'):
    charset = '0123456789abcdefghijklmnopqrstuvwxyz'
    max_length = 6

    start_time = time.time()
    attempt_count = 0

    with zipfile.ZipFile(zip_filename) as zf:
        for c1 in charset:
            for c2 in charset:
                for c3 in charset:
                    for c4 in charset:
                        for c5 in charset:
                            for c6 in charset:
                                password = c1 + c2 + c3 + c4 + c5 + c6
                                attempt_count += 1

                                if attempt_count % 1000 == 0:
                                    elapsed_time = time.time() - start_time
                                    print(
                                        f'[INFO] 시도 횟수: {attempt_count}, 경과 시간: {elapsed_time:.2f}초'
                                    )

                                try:
                                    zf.extractall(pwd=password.encode('utf-8'))
                                    print(f'[SUCCESS] 암호를 찾았습니다: {password}')

                                    with open('password.txt', 'w') as f:
                                        f.write(password)
                                    return password
                                except Exception:
                                    continue

    print('[FAILED] 암호를 찾지 못했습니다.')
    return None


if __name__ == '__main__':
    unlock_zip()
