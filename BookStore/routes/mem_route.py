import os
import sys
# 현재 디렉토리 위치 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import request, render_template, redirect, Blueprint, session
from models.mem_model import Member, MemService
#from BookStore.models.mem_model import Member, MemService

service = MemService()

bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/join')
def joinForm():
    return render_template('member/form.html')

@bp.route('/join', methods=['POST'])
def join():
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    service.join(Member(id=id, pwd=pwd, name=name, email=email, mobile=mobile))
    return render_template('member/login.html')

@bp.route('/login')
def loginForm():
    return render_template('member/login.html')

@bp.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    flag = service.login(id, pwd)
    return render_template('index.html')

@bp.route('/logout')
def logout():
    service.logout()
    return render_template('index.html')

@bp.route('/myInfo')
def myInfo():
    m = service.myInfo()
    return render_template('member/detail.html', m=m)

@bp.route('/edit', methods=['POST'])
def edit():
    pwd = request.form['pwd']
    email = request.form['email']
    service.editMyInfo(pwd, email)
    return redirect('/member/myInfo')

@bp.route('/out')
def delete():
    service.out()
    return render_template('index.html')



