import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request, render_template, redirect, Blueprint, session
from models.mem_model import Review
from models.rev_model import ReviewService

service = ReviewService()

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/add')
def addForm():
    return render_template('review/form.html')

@bp.route('/add', methods=['POST'])
def add():
    reviewer = request.form['reviewer']
    book_name = request.form['book_name']
    content = request.form['content']
    score = request.form['score']
    service.addReview(Review(reviewer=reviewer, book_name=book_name, content=content, score=score))
    return redirect('/review/list')

@bp.route('/list')
def list():
    rlist = service.getAll()
    return render_template('review/list.html', rlist = rlist)

@bp.route('/getbyreviewer/<string:reviewer>')
def getbyreviewer(reviewer):
    rlist = service.getByReviewer(reviewer)
    return render_template('review/list.html', rlist=rlist)

@bp.route('/myReview')
def myReview():
    reviewer = session['login_id']
    rlist = service.getByReviewer(reviewer)
    return render_template('review/list.html', rlist=rlist)


@bp.route('detail/<int:review_no>')
def detail(review_no):
    r = service.getReview(review_no)
    if r.reviewer == session['login_id']:
        flag = True
        msg = ''
    else:
        flag = False
        msg = 'readonly'
    return render_template('review/detail.html', r=r, flag=flag, msg=msg)

