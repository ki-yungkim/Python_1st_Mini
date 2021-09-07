import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request, render_template, redirect, Blueprint, session
from models.mem_model import Order
from models.ord_model import OrderService

service = OrderService()

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/add')
def addForm():
    return render_template('order/form.html')

@bp.route('/add', methods=['POST'])
def add():
    orderer = request.form['orderer']
    book_name = request.form['book_name']
    book_type = request.form['book_type']
    buy_rental = request.form['buy_rental']
    service.addOrder(Order(orderer=orderer, book_name=book_name, book_type=book_type, buy_rental=buy_rental))
    return redirect('/order/list')

@bp.route('/list')
def list():
    olist = service.getAll()
    return render_template('order/list.html', olist = olist)

@bp.route('/getbyorderer/<string:orderer>')
def getbyorderer(orderer):
    olist = service.getByOrderer(orderer)
    return render_template('order/list.html', olist = olist)

@bp.route('/getbytitle/<string:book_name>')
def getbytitle(book_name):
    olist = service.getByTitle(book_name)
    return render_template('order/list.html', olist = olist)

@bp.route('/myOrder')
def myOrder():
    orderer= session['login_id']
    olist = service.getByOrderer(orderer)
    return render_template('order/list.html', olist = olist)
