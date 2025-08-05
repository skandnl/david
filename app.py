from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>메인 페이지</h1><p>/menu 로 이동하면 메뉴판을 볼 수 있습니다.</p>"

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
