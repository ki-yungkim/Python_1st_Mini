import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
from models.mem_model import Member,PaperBook

db = SQLAlchemy()
migrate = Migrate()

class PaperBookService:

    # 책 추가
    def addPaperBook(self,pb:PaperBook):
        db.session.add(pb)
        db.session.commit()

    # 책 전체 조회
    def getPaperBookAll(self):
        return PaperBook.query.order_by(PaperBook.book_no.asc())

    # 책 상세정보
    def getPaperBookDetail(self,paper_book_no):
        return PaperBook.query.get(paper_book_no)

    # 책 이름으로 검색
    def getPaperBookName(self,paper_book_name):
        return PaperBook.query.filter(PaperBook.paper_book_name.like('%' + paper_book_name + '%')).all()
    # 책 지은이로 검색
    def getPaperBookPublisher(self,paper_book_publisher):
        return PaperBook.query.filter(PaperBook.paper_book_publisher.like('%' + paper_book_publisher + '%')).all()

    # 책 정보 수정
    def editPaperBookInfo(self,paper_book_no,name,publisher,price,amount):
        book = self.getPaperBookDetail(paper_book_no)
        book.paper_book_name = name
        book.paper_book_publisher = publisher
        book.paper_book_price = price
        book.paper_book_amount = amount

    # 책 정보 삭제
    def deletePaperBook(self,paper_book_no):
        book = self.getPaperBookDetail(paper_book_no)
        db.session.delete(book)
        db.session.commit()