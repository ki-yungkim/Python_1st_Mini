import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request, render_template, redirect, Blueprint, session
from models.mem_model import Review, ReviewService
#from models.rev_model import ReviewService

service = ReviewService()

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/add')
def addForm():
    return render_template('review/form.html')

@bp.route('/add', methods=['POST'])
def add():
    reviewer = request.form['reviewer']
    book_title = request.form['book_title']
    content = request.form['content']
    score = request.form['score']
    service.addReview(Review(reviewer=reviewer, book_title=book_title, content=content, score=score))
    return redirect('/review/myReview')

@bp.route('/add/<string:book_title>')
def addReviewByTitle(book_title):
    return render_template('review/form.html', book_title=book_title)

@bp.route('/list')
def list():
    rlist = service.getAll()
    return render_template('review/list.html', rlist = rlist)

@bp.route('/getbyreviewer/<string:reviewer>')
def getbyreviewer(reviewer):
    rlist = service.getByReviewer(reviewer)
    return render_template('review/list.html', rlist=rlist)
'''
@bp.route('/getbybookno/<string:book_no>')
def getbyno(book_no):
    rlist = service.getByBookTitle(book_no)
    return render_template('review/list.html', rlist=rlist)
'''
@bp.route('/getbybooktitle/<string:book_title>')
def getbytitle(book_title):
    rlist = service.getByBookTitle(book_title)
    return render_template('review/list.html', rlist=rlist)

@bp.route('/myReview')
def myReview():
    reviewer = session['login_id']
    rlist = service.getByReviewer(reviewer)
    return render_template('review/list.html', rlist=rlist)


@bp.route('/detail/<int:review_no>')
def detail(review_no):
    r = service.getReview(review_no)
    if r.reviewer == session['login_id']:
        flag = True
        msg = ''
    else:
        flag = False
        msg = 'readonly'
    return render_template('review/detail.html', r=r, flag=flag, msg=msg)

@bp.route('/edit', methods=['POST'])
def edit():
    review_no = request.form['review_no']
    content = request.form['content']
    score = request.form['score']
    service.editReview(Review(review_no=review_no, content=content, score=score))
    return redirect('/review/myReview')

@bp.route('/del')
def delete():
    review_no = request.args.get('num', 0, int)
    service.delReview(review_no)
    return render_template('index.html')
