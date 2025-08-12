from flask import Flask, render_template
import socket  # ✅ socket 모듈 추가

app = Flask(__name__)




@app.route('/test333')
def test():
    return render_template('test333.html')




def home():
    # ✅ debug 모드에 따라 컴퓨터 이름 표시
    if app.debug:
        hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
    else:
        hostname = ' '
    
    # ✅ index.html 렌더링 시 computername 전달
    return render_template('index.html', computername=hostname)

@app.route('/menu')
def menu():
    # menu.html을 templates 폴더에서 불러옴
    return render_template('menu.html')

if __name__ == '__main__':
    # ✅ debug=True 옵션 유지
    app.run(host='0.0.0.0', port=5000, debug=True)
