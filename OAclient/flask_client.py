######################################################
#     > File Name: flask_client.py
#     > Author: jiayuhao
#     > Mail: jiayuhaowork@163.com
#     > Created Time: 2020 9 3
######################################################




from flask import Flask, send_file
import sys

app = Flask(__name__)


@app.route('/index')
def index():
    # 首页
    return send_file('templates/index.html')


@app.route('/c_login')
def c_login():
    # 企业登录 1
    return send_file('templates/c_login.html')

@app.route('/login')
def login():
    # 用户登录
    return send_file('templates/login.html')

@app.route('/login_callback')
def login_callback():
    #授权登录
    return send_file('templates/oauth_callback.html')

@app.route('/c_register')
def c_register():
    # 企业注册 2
    return send_file('templates/c_register.html')

@app.route('/register')
def register():
    #用户注册
    return send_file('templates/register.html')

@app.route('/<username>/info')
def info(username):
    #个人信息
    return send_file('templates/about.html')

@app.route('/<username>/change_info')
def change_info(username):
    #修改个人信息
    return send_file('templates/change_info.html')

@app.route('/<username>/change_password')
def change_password(username):
    #修改密码
    return send_file('templates/change_password.html')
	
@app.route('/<username>/topics')
def topics(username):
    #用户主页
    return send_file('templates/home.html')

@app.route('/<email>/users_show/')
def users_show(email):
    #　企业管理列表
    return send_file('templates/employer.html')
    # return send_file('templates/emoloyer_list.html')

@app.route('/excel/split_merge')
def split_excel():
    # excel 拆分
    return send_file('templates/excel.html')


@app.route('/test_api')
def test_api():
    # 测试
    return send_file('templates/employer.html')


if __name__ == '__main__':
    app.run(debug=True)
