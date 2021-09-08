import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
from models.mem_model import Order, Member
db = SQLAlchemy()
migrate = Migrate()

class OrderService:
    # 주문 추가
    def addOrder(self, o:Order): # 주문자, 책 제목, 타입, 구입/렌탈 여부
        o.date = datetime.now()
        db.session.add(o)
        db.session.commit()

    # 번호로 가져오기
    def getOrder(self, order_no):
        return Order.query.get(order_no)

    # 전체 가져오기
    def getAll(self):
        return Order.query.order_by(Order.order_no.asc())

    '''
    # 주문자의 모든 주문 검색
    def getByOrderer(self, orderer):
        mem = Member.query.get(orderer)
        if mem is not None:
            return mem.order_set
    '''

    # 주문자의 모든 주문 검색
    def getByOrderer(self, orderer):
        return Order.query.filter(Order.orderer == orderer)

    # 제목으로 검색
    def getByTitle(self, tit):
        return Order.query.filter(Order.book_title.like('%'+tit+'%')).all()

    # 주문 삭제
    def delReview(self, order_no):
        o = Order.query.get(order_no)
        db.session.delete(o)
        db.session.commit()



