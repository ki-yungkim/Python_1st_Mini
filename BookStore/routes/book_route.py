import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request,render_template,redirect,Blueprint,session
from models.mem_model import Book, BookService

service = BookService()

bp = Blueprint('book', __name__,url_prefix='/book')

# 책 등록
@bp.route('/add')
def addForm():
    return render_template('book/form.html')

@bp.route('/add',methods=['POST'])
def add():
    book_title = request.form['book_title']
    book_type = request.form['book_type']
    book_author = request.form['book_author']
    book_price = request.form['book_price']
    book_amount = request.form['book_amount']
    service.addBook(Book(book_title=book_title,book_type=book_type,book_author=book_author,book_price=book_price,book_amount=book_amount))
    return redirect('/book/list')

# 책 목록
@bp.route('/list')
def list():
    pblist = service.getBookAll()
    return render_template('/book/list.html',pblist=pblist)

# 책 검색
@bp.route('/getbybooktitle/<string:book_title>')
def getbytitle(book_title):
    pblist = service.getBookTitle(book_title)
    return render_template('/book/list.html',pblist=pblist)

@bp.route('/getbybookauthor/<string:book_author>')
def getbyauthor(book_author):
    pblist = service.getBookAuthor(book_author)
    return render_template('/book/list.html',pblist=pblist)

#책 상세 정보
@bp.route('/detail/<string:book_no>')
def bookInfo(book_no):
    pb = service.getBookDetail(book_no)
    return render_template('/book/detail.html',pb=pb)
'''
# 책 정보 수정
@bp.route('/edit/<string:book_no>')
def editForm(book_no):
    pb = service.getBookDetail(book_no)
    return render_template('/book/edit-form.html',pb=pb)

@bp.route('/edit',methods=['POST'])
def editBook(book_no):
    name = request.form['book_title']
    author = request.form['book_author']
    price = request.form['book_price']
    amount = request.form['book_amount']
    return render_template('/book/list.html')
'''

# 책 삭제
@bp.route('/delete/<string:book_no>')
def delete(book_no):
    service.deleteBook(book_no)
    return redirect('/book/list')


