## 반달곰 커피 홈페이지

참조링크: [https://반달곰커피](https://반달곰커피)

문구: 오디오 출력 소스코드

```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)
encoded_audio_data = base64.b64encode(fp.getvalue())
![david](https://github.com/user-attachments/assets/86c3c36e-fb90-468d-85e9-44474c332ba9)

