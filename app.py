from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>메인 페이지</h1><p><a href='/menu'>메뉴판 보러가기</a></p>"

@app.route('/menu')
def menu():
    # menu.html을 templates 폴더에서 불러옴
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
