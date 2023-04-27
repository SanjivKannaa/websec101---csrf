from crypt import methods
from encodings import search_function
from hashlib import new
from operator import methodcaller
import re
from sqlite3 import connect
import pickle
from urllib import response
from wsgiref.simple_server import make_server
from flask import Flask, jsonify, make_response, redirect, render_template, request
import database
import random
import mysql.connector as sql

app = Flask(__name__)


@app.route('/bruh')
def bruh():
    return render_template('feed.html', username="sanjiv")

@app.errorhandler(403)
def error_403(e):
    return render_template('error404.html', error = "403")

@app.errorhandler(404)
def error_404(e):
    return render_template('error404.html', error = "404")


@app.errorhandler(500)
def error_500(e):
    return render_template('error404.html', error = "500")

@app.route('/admin')
def admin_access_denied():
    return render_template('error404.html', error = "403")

@app.route('/admin/sanjiv')
def admin():
    return '''
    <html>
    <head>
    <title>admin page | Slambook</title>
    </head>
    <body>
    <a href="/admin/sanjiv/passwords">passwords database</a>
    <br><br>
    <a href="/admin/sanjiv/users">user database</a>
    <br><br>
    <a href="/admin/sanjiv/posts">all posts</a>
    <br><br>
    <a href="/admin/sanjiv/follow">all profile following and followers list</a>
    </body>
    </html>
    '''

@app.route('/admin/sanjiv/passwords')
def admin_pass():
    return make_response(jsonify(database.get_login_info()), 200)

@app.route('/admin/sanjiv/users')
def admin_users():
    return make_response(jsonify(database.get_all_user_info()), 200)

@app.route('/admin/sanjiv/posts')
def admin_posts():
    return make_response(jsonify(database.get_all_posts()), 200)

@app.route('/admin/sanjiv/follow')
def admin_follow():
    return make_response(jsonify(database.get_follow()), 200)



@app.route('/', methods = ["GET", "POST"])
def function():
    if request.method == "GET":
        if request.cookies.get('login_status') == 'True':
            redirect('/home')
        else:
            return redirect('./login')


@app.route('/profile/<rollno>', methods=["GET", "POST"])
def user_profile(rollno):
    if request.method == "GET":
        f = open("./data/user_info.bin", "rb")
        content = pickle.load(f)
        f.close()
        f = open("./data/posts.bin", "rb")
        all_posts = list(pickle.load(f))[::-1]    #[["by", "message", ["tags"...], "timestamp"]...]
        f.close()
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "rb")
        following = list(pickle.load(f))
        f.close()
        if rollno in following:
            follow_or_unfollow = 'Unfollow'
        else:
            follow_or_unfollow = "Follow"
        posts = []
        for i in all_posts:
            if i[0] == "@"+rollno or "@"+rollno in i[2]:
                #posts.append([i[1], i[0]])
                posts.append([database.change_rollno_to_username(i[1]), database.change_rollno_to_username(i[0]), len(all_posts)-1-all_posts.index(i)])
        if len(posts) == 0:
            posts = [["NO POSTS", "", ""]]
        for bruh in range(31-len(posts)):
            posts.append(["", "", ""])
        username = content[rollno]['username']
        name = content[rollno]['name']
        dept = content[rollno]['branch'] + " " + content[rollno]['section']
        return render_template("profile.html", login_username = request.cookies.get('login_username'), rollno = rollno, name = name, username = username, dept =  dept, follow_or_unfollow = follow_or_unfollow + " " + username, post0 = posts[0][0], postby0 = posts[0][1], postID0 = posts[0][2], post1 = posts[1][0], postby1 = posts[1][1], postID1 = posts[1][2], post2 = posts[2][0], postby2 = posts[2][1], postID2 = posts[2][2], post3 = posts[3][0], postby3 = posts[3][1], postID3 = posts[3][2], post4 = posts[4][0], postby4 = posts[4][1], postID4 = posts[4][2], post5 = posts[5][0], postby5 = posts[5][1], postID5 = posts[5][2], post6 = posts[6][0], postby6 = posts[6][1], postID6 = posts[6][2], post7 = posts[7][0], postby7 = posts[7][1], postID7 = posts[7][2], post8 = posts[8][0], postby8 = posts[8][1], postID8 = posts[8][2], post9 = posts[9][0], postby9 = posts[9][1], postID9 = posts[9][2], post10 = posts[10][0], postby10 = posts[10][1], postID10 = posts[10][2], post11 = posts[11][0], postby11 = posts[11][1], postID11 = posts[11][2], post12 = posts[12][0], postby12 = posts[12][1], postID12 = posts[12][2], post13 = posts[13][0], postby13 = posts[13][1], postID13 = posts[13][2], post14 = posts[14][0], postby14 = posts[14][1], postID14 = posts[14][2], post15 = posts[15][0], postby15 = posts[15][1], postID15 = posts[15][2], post16 = posts[16][0], postby16 = posts[16][1], postID16 = posts[16][2], post17 = posts[17][0], postby17 = posts[17][1], postID17 = posts[17][2], post18 = posts[18][0], postby18 = posts[18][1], postID18 = posts[18][2], post19 = posts[19][0], postby19 = posts[19][1], postID19 = posts[19][2], post20 = posts[20][0], postby20 = posts[20][1], postID20 = posts[20][2], post21 = posts[21][0], postby21 = posts[21][1], postID21 = posts[21][2], post22 = posts[22][0], postby22 = posts[22][1], postID22 = posts[22][2], post23 = posts[23][0], postby23 = posts[23][1], postID23 = posts[23][2], post24 = posts[24][0], postby24 = posts[24][1], postID24 = posts[24][2], post25 = posts[25][0], postby25 = posts[25][1], postID25 = posts[25][2], post26 = posts[26][0], postby26 = posts[26][1], postID26 = posts[26][2], post27 = posts[27][0], postby27 = posts[27][1], postID27 = posts[27][2], post28 = posts[28][0], postby28 = posts[28][1], postID28 = posts[28][2], post29 = posts[29][0], postby29 = posts[29][1], postID29 = posts[29][2], post30 = posts[30][0], postby30 = posts[30][1], postID30 = posts[30][2])
    if request.method == "POST":
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "rb")
        content = list(pickle.load(f))
        f.close()
        if rollno in content:
            content.remove(rollno)
        else:
            content.append(rollno)
        f = open("./data/user_data/{}.bin".format(request.cookies.get('login_rollno')), "wb")
        pickle.dump(content, f)
        f.close()
        return redirect('/profile/{}'.format(rollno))



@app.route('/developer')
def developer_information():
    return render_template('developer.html')

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login_validation():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        content = database.get_login_info()
        rollno = str(request.form.get('rollno'))
        password = str(request.form.get('password'))
        #print('\n\n\n\n{}\n\n{}\n\n\n\n'.format(len(rollno), len(password)))
        #return "username = {} password = {}".format(rollno, password)
        if rollno not in content.keys():
            return make_response(redirect("/login"))
        if content[rollno] == password:
            res = make_response(render_template('index.html'))
            username = database.get_user_info(rollno)['username']
            res.set_cookie('login_status', 'True')
            res.set_cookie('login_rollno', rollno)
            res.set_cookie('login_username', username)
            return res
        else:
            return redirect("./login")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == "POST":
        name = str(request.form.get('name'))
        rollno = str(request.form.get('rollno'))
        password1 = str(request.form.get('password1'))
        password2 = str(request.form.get('password2'))
        gender = str(request.form.get('gender'))
        programme = str(request.form.get('programme'))
        branch = str(request.form.get('branch'))
        section = str(request.form.get('section'))
        username = str(request.form.get('username'))
        hostel = str(request.form.get('hostel'))
        name.replace(" ", "_")
        f = open("./data/user_data/{}.bin".format(rollno), "wb")
        content = []  #[following]
        pickle.dump(content, f)
        f.close()
        if database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[0]:
            return render_template('signup_success.html')
        else:
            return database.check_signup(name, rollno, password1, password2, gender, programme, branch, section, username, hostel)[1]


@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == 'GET':
        res = make_response(redirect('./login'))
        res.set_cookie('login_status', "false")
        res.set_cookie('login_rollno', '')
        res.set_cookie('login_username', '')
        return res

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    if request.method == "POST":
        rollno = request.form.get('rollno')
        f = open('./data/otp.bin', "wb")
        otp = str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        print(otp)
        pickle.dump([rollno, otp], f)
        f.close()
        email_bot.send_otp(str(rollno)+"@nitt.edu", otp)
        return render_template("forgot_password_step_2.html")

@app.route('/forgot_password/otp_accepted', methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template('forgot_password_Step_2.html')
    if request.method == "POST":
        f = open("./data/otp.bin", 'rb')
        rollno, given_otp = list(pickle.load(f))
        f.close()
        otp = request.form.get('otp')
        newpassword1 = request.form.get('newpassword1')
        newpassword2 = request.form.get('newpassword2')
        if otp == given_otp and newpassword1 == newpassword2:
            database.put_login_info(rollno, newpassword1)
            return render_template('password_changed.html')
        else:
            return "error"



@app.route('/my_profile', methods=["POST", "GET"])
def my_profile():
    return redirect("/profile/{}".format(request.cookies.get('login_username')))


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if request.method == "GET":
        return render_template('settings.html', username = request.cookies.get('login_username'))
    if request.method == "POST":
        post_number = str(request.form.get('post_number'))
        old_password = str(request.form.get('old_password'))
        new_password1 = str(request.form.get('new_password1'))
        new_password2 = str(request.form.get('new_password2'))
        if post_number != "None":
            database.del_post(post_number)
            return redirect('/settings')
        if old_password != "None" or new_password1 != "None" or new_password2 != "None":
            rollno = request.cookies.get('login_rollno')
            database.change_password(rollno = rollno, old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            return redirect('/setings')









   
if __name__ == '__main__':
    app.run(port='8080')
