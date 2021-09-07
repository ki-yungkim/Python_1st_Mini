import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
from models.mem_model import Review
db = SQLAlchemy()
migrate = Migrate()

class ReviewService:
    # 리뷰 작성
    def addReview(self, r:Review):
        r.date = datetime.now()
        db.session.add(r)
        db.session.commit()

    # 번호로 가져오기
    def getReview(self, review_no):
        return Review.query.get(review_no)

    # 전체 가져오기
    def getAll(self):
        return Review.query.order_by(Review.review_no.asc())

    # 리뷰어의 모든 리뷰 검색
    def getByReviewer(self, reviewer):
        return Review.query.filter(Review.reviewer == reviewer)

