from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session


db = SQLAlchemy()
migrate = Migrate()

# 회원
class Member(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    pwd = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)

# 주문
class Order(db.Model):
    order_no = db.Column(db.Integer, primary_key=True)
    orderer = db.Column(db.String(20), db.ForeignKey('member.id', ondelete='CASCADE'))
    book_name = db.Column(db.String(20), nullable=False)
    book_type = db.Column(db.String(20), nullable=False)
    buy_rental = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    expire = db.Column(db.DateTime())
    member = db.relationship('Member', backref=db.backref('order_set'))

# 리뷰

class Review(db.Model):
    review_no = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    score = db.Column(db.Numeric)

# 회원 서비스
class MemService:
    # 회원가입
    def join(self, m:Member):
        # insert
        db.session.add(m)
        db.session.commit()

    # 로그인
    def login(self, id:str, pwd:str):
        mem = Member.query.get(id)
        if mem is not None:
            if pwd == mem.pwd:
                session['login_id'] = id
                session['flag'] = True
                return True

        return False

    # 로그아웃
    def logout(self):
        session.pop('login_id')
        session['flag']=False

    # 내 정보 보기
    def myInfo(self):
        id = session['login_id']
        return Member.query.get(id)


    # 정보 수정
    def editMyInfo(self, pwd, email):
        mem = self.myInfo()
        mem.pwd = pwd
        mem.email = email
        db.session.commit()

    # 탈퇴
    def out(self):
        mem = self.myInfo()
        db.session.delete(mem)
        db.session.commit()
        self.logout()






