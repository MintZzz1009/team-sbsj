from flask import Flask, session, render_template, request, jsonify

import pymysql

app = Flask(__name__)
app.secret_key = "My_Secret_Key"

# db = pymysql.connect(host='121.166.127.220', user='haksoo', db='sparta_sbsj', password='12345678', charset='utf8')
# db = pymysql.connect(host='localhost', user='root', db='sparta_sbsj', password='bobo1200', charset='utf8')
hostname = 'localhost'
username = 'root'
userpw = 'bobo1200'


@app.route("/")
def home():
    return render_template('index.html')


# ID 중복 확인
@app.route("/main/signup/userid", methods=["POST"])
def user_id_confirm():
    user_id_receive = request.form['user_id_give']

    # mySQL db 접속
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()

    #  전체 데이터 조회 후 data_list 변수에 할당
    sql = "SELECT * FROM sparta_sbsj.`user` u"
    curs.execute(sql)
    data_list = curs.fetchall()
    result = []
    for data in data_list:
        if user_id_receive == data[1]:
            temp = {'user_id': data[1]}
            result.append(temp)
            break
    db.commit()
    db.close()
    result_msg = 'fail' if len(result) == 1 else 'available'
    return jsonify({'result': result_msg})


# 회원 가입시 회원 정보 DB에 입력
@app.route("/main/signup", methods=["POST"])
def sign_up():
    user_id_receive = request.form['user_id_give']
    user_pw_receive = request.form['user_pw_give']
    user_name_receive = request.form['user_name_give']
    user_email_receive = request.form['user_email_give']

    data_receive = (user_id_receive, user_pw_receive, user_name_receive, user_email_receive)

    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()

    sql = "insert into user (user_id, user_pw, user_name, user_email) values(%s, %s, %s, %s);"

    curs.execute(sql, data_receive)
    db.commit()
    db.close()

    return jsonify({'msg': 'data insert 성공!'})


# 로그인 요청시 정보 확인
@app.route("/main/login", methods=["POST"])
def log_in():
    input_id_receive = request.form['input_id_give']
    input_pw_receive = request.form['input_pw_give']

    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()

    sql = "SELECT * FROM sparta_sbsj.`user` u"
    curs.execute(sql)
    data_list = curs.fetchall()

    result = []
    for data in data_list:
        if data[1] == input_id_receive:
            if data[2] == input_pw_receive:
                result_msg = 'login'
                session['uniq_id'] = data[0]
                session['user_id'] = data[1]
                session['user_pw'] = data[2]
                session['user_name'] = data[3]
                session['user_email'] = data[4]
                session['user_topic'] = data[5]
                session['user_desc'] = data[6]
                session['user_created_at'] = data[7]
                session['user_profile_img_src'] = data[8]
                print(session)
                print(len(session))

                break
            else:
                result_msg = 'wrong_pw'
                break
    else:
        result_msg = 'fail'

    db.commit()
    db.close()
    return jsonify({'msg': result_msg, 'result': result})


# 로그 아웃 요청시 세션 클리어
@app.route("/main/logout", methods=["GET"])
def log_out():
    session.clear()
    msg = '세션클리어!'
    print(f'현재 세션: {session}')
    return jsonify({'msg': msg})


# 뉴스피드 조회
@app.route('/main', methods=['GET'])
def get_AllNewsfeed():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()
    sql = """SELECt * FROM posting p 
                INNER JOIN `user` u ON p.user_unique_id = u.user_unique_id GROUP BY posting_id
            """
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)
    db.commit()
    db.close()
    return jsonify({'posting__box': rows})


# 댓글 저장
@app.route('/save_comment', methods=['POST'])
def save_comment():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()
    comment_receive = request.form['comment_give']
    clock_receive = request.form['clock_give']
    print(type(clock_receive))
    clock_receive = str(clock_receive)
    print(3)
    sql = """INSERT INTO comment
            (comments, comment_created_at)
            VALUES (%s, %s)
            """
    print(4)
    curs.execute(sql, (comment_receive, clock_receive))
    db.commit()
    db.close()
    print(5)

    return jsonify({"msg": "댓글작성 완료!"})


# 댓글 조회
@app.route('/show_comment', methods=['GET'])
def show_comment():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()

    sql = """SELECT comment_id, comments, comment_created_at FROM comment"""

    curs.execute(sql)
    rows = curs.fetchall()

    user_list = []

    for list in rows:
        temp = {
            'comment_id': list[0],
            'comment': list[1],
            'clock': list[2]
        }
        user_list.append(temp)
    return jsonify({'msg': user_list})


# 댓글 수정
@app.route('/update/comment', methods=['POST'])
def update_comment():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')

    curs = db.cursor()

    edit_done_receive = request.form['edit_done_give']
    edit_comment_id_receive = request.form['edit_comment_id_give']

    sql = """UPDATE comment SET comments = %s WHERE comment_id = %s"""
    curs.execute(sql, (edit_comment_id_receive, edit_done_receive))

    db.commit()
    db.close()
    return jsonify({'msg': '수정 완료!'})


# 게시글 작성하기
@app.route('/mypage/newsfeed', methods=['POST'])
def post_NewNewsfeed():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    curs = db.cursor()

    posting = request.form
    posting_user_id_give = int(posting['user_id_give'])
    posting_title_give = posting['posting_title_give']
    posting_text_give = posting['posting_text_give']
    posting_topic_give = posting['posting_topic_give']

    sql = """
    insert into posting (user_unique_id, posting_title, posting_text, posting_topic) values (%s,%s,%s,%s)
            """

    curs.execute(sql, (posting_user_id_give, posting_title_give, posting_text_give, posting_topic_give))
    rows = curs.fetchall()

    db.commit()
    db.close()
    return jsonify({'msg': '등록 완료'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
