from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime

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
    book_title = db.Column(db.String(20), nullable=False)
    book_type = db.Column(db.String(20), nullable=False)
    buy_rental = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    expire = db.Column(db.DateTime())
    member = db.relationship('Member', backref=db.backref('order_set'))

# 책 정보
class Book(db.Model):
    book_no = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(20),nullable=False)
    book_type = db.Column(db.String(20),nullable=False) #paper or ebook
    book_author = db.Column(db.String(20),nullable=False)
    book_price = db.Column(db.Numeric(20),nullable=False)
    book_amount = db.Column(db.Numeric(10),nullable=False)

# 리뷰
class Review(db.Model):
    review_no = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.String(20), nullable=False)
    book_title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    score = db.Column(db.String(20), nullable=False)

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

# 책 서비스
class BookService:

    # 책 추가
    def addBook(self,pb:Book):
        db.session.add(pb)
        db.session.commit()

    # 책 전체 조회
    def getBookAll(self):
        return Book.query.order_by(Book.book_no.asc())

    # 책 상세정보
    def getBookDetail(self,book_no):
        return Book.query.get(book_no)

    # 책 이름으로 검색
    def getBookTitle(self,book_title):
        return Book.query.filter(Book.book_title.like('%' + book_title + '%')).all()
    # 책 지은이로 검색
    def getBookAuthor(self,book_author):
        return Book.query.filter(Book.book_author.like('%' + book_author + '%')).all()

    '''
    # 책 정보 수정
    def editBookInfo(self,book_no, name, author, price, amount):
        book = self.getBookDetail(book_no)
        book.book_name = name
        book.book_author = author
        book.book_price = price
        book.book_amount = amount
        db.session.commit()
    '''
    # 책 정보 삭제
    def deleteBook(self,book_no):
        book = self.getBookDetail(book_no)
        db.session.delete(book)
        db.session.commit()

    # 책 제목으로 정보 조회
    def getBookByTitle(self, book_title):
        return Book.query.filter(Book.book_title == book_title).all()

    # 책 주문시 수량 수정
    def editBookAmount(self, book_title):
        b = self.getBookByTitle(book_title)
        book = b[0]
        print(book.book_amount)
        book.book_amount -= 1
        print(book.book_amount)
        db.session.commit()

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

    # 도서 번호로 리뷰 검색
    def getByBookTitle(self, book_title):
        return Review.query.filter(Review.book_title == book_title)

    # 리뷰 수정
    def editReview(self, r:Review):
        r2 = self.getReview(r.review_no)
        r2.content = r.content
        r2.score = r.score
        r2.date = datetime.now()
        db.session.commit()

    # 리뷰 삭제
    def delReview(self, review_no):
        r = Review.query.get(review_no)
        db.session.delete(r)
        db.session.commit()

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
    def deleteOrder(self, order_no):
        o = Order.query.get(order_no)
        db.session.delete(o)
        db.session.commit()