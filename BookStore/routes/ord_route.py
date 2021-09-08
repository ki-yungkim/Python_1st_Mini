import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request, render_template, redirect, Blueprint, session
from models.mem_model import Order, OrderService, BookService

service = OrderService()
book_service = BookService()

bp = Blueprint('order', __name__, url_prefix='/order')

# 주문 폼
@bp.route('/add')
def addForm():
    return render_template('order/form.html')

# 주문
@bp.route('/add', methods=['POST'])
def add():
    orderer = request.form['orderer']
    book_title = request.form['book_title']
    book_type = request.form['book_type']
    buy_rental = request.form['buy_rental']
    service.addOrder(Order(orderer=orderer, book_title=book_title, book_type=book_type, buy_rental=buy_rental))
    # 주문시 수량 수정
    book_service.editBookAmount(book_title)
    return redirect('/order/myOrder')


# 제목으로 찾기
@bp.route('/getbybooktitle/<string:book_title>')
def addFormbyBookTitle(book_title):
    return render_template('order/form.html', book_title=book_title)

# 전체 목록
@bp.route('/list')
def list():
    olist = service.getAll()
    return render_template('order/list.html', olist = olist)

# 주문자로 찾기
@bp.route('/getbyorderer/<string:orderer>')
def getbyorderer(orderer):
    olist = service.getByOrderer(orderer)
    return render_template('order/list.html', olist = olist)

# 제목으로 찾기
@bp.route('/getbytitle/<string:book_title>')
def getbytitle(book_title):
    olist = service.getByTitle(book_title)
    return render_template('order/list.html', olist = olist)

# 내 주문 보기
@bp.route('/myOrder')
def myOrder():
    orderer= session['login_id']
    olist = service.getByOrderer(orderer)
    return render_template('order/list.html', olist = olist)

# 주문삭제
@bp.route('delete/<string:order_no>')
def delete(order_no):
    service.deleteOrder(order_no)
    return render_template('index.html')

