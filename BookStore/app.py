from flask import Flask, request, render_template, redirect, session
from models.mem_model import db, migrate

import config

import routes.mem_route as mr
import routes.ord_route as ort
import routes.rev_route as rrt
import routes.book_route as bkt
# 플라스크 객체 생성
app = Flask(__name__)

# 시크릿 키 설정
app.secret_key = 'session_key'

# config
app.config.from_object(config)

# 블루프린트
app.register_blueprint(mr.bp)
app.register_blueprint(ort.bp)
app.register_blueprint(rrt.bp)
app.register_blueprint(bkt.bp)


# ORM
db.init_app(app)
migrate.init_app(app, db)

# 메인페이지('/')
@app.route('/')
def root():
    if 'flag' not in session.keys():
        session['flag']=False
    return render_template('index.html')

# flask 서버 실행
if __name__ == '__main__':
    app.run()








