## 반달곰 커피 홈페이지

참조링크: [https://반달곰커피](https://반달곰커피)

문구: 오디오 출력 소스코드


![david](https://github.com/user-attachments/assets/dfe5ad90-10cc-43ea-988f-69f4d5fef2f8)






```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)
encoded_audio_data = base64.b64encode(fp.getvalue())


