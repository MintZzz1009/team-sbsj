from flask import Flask, session, render_template, request, jsonify
import pymysql

from werkzeug.utils import secure_filename
import os

from datetime import datetime

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
    # print(rows)
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
    posting_receive = request.form['posting_id_give']
    # print(type(clock_receive))
    # clock_receive = str(clock_receive)
    # print(3)
    sql = """INSERT INTO comment
            (comments, comment_created_at, posting_id)
            VALUES (%s, %s, %s)
            """
    curs.execute(sql, (comment_receive, clock_receive, posting_receive))
    db.commit()
    db.close()

    return jsonify({"msg": "댓글작성 완료!"})


# 댓글 조회
@app.route('/show_comment', methods=['POST'])
def show_comment():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    curs = db.cursor()

    pid_receive = int(request.form['pid_give'])
    sql = """SELECT * FROM comment"""

    curs.execute(sql)
    rows = curs.fetchall()

    user_list = []

    for list in rows:
        if pid_receive == list[4]:
            temp = {
                'comment_id': list[0],
                'comment': list[2],
                'clock': list[3],
                'post_id': list[4]
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


# 댓글 삭제
@app.route('/delete/comment', methods=['POST'])
def delete_comment():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    curs = db.cursor()

    delete_receive = request.form['delete_give']

    sql = """DELETE FROM comment WHERE comment_id = %s"""
    curs.execute(sql, (delete_receive))

    db.commit()
    db.close()

    return jsonify({'msg': '삭제 완료!'})


# 게시글 작성하기
@app.route('/mypage/newsfeed', methods=['POST'])
def post_NewNewsfeed():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    curs = db.cursor()

    posting = request.form

    try:
        print(type(session['uniq_id']))
    except:
        return jsonify({'msg': '로그인 후 작성 가능합니다.'})

    posting_user_id_give = session['uniq_id']
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


@app.route('/mypage')
def mymage_main():
    return render_template('mypage.html')


# 마이페이지 불러오기
@app.route("/mypage/mypage_reload", methods=["GET"])
def mypage_reload():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    sql = '''
        SELECT u.user_unique_id, u.user_profile_img_src, u.user_name, u.user_id, u.user_email, u.user_created_at, u.user_desc, mi.mbti, mi.killingtime, mi.user_birth, mi.interest FROM mypage_info mi
    left join user u on mi.user_unique_id = u.user_unique_id
    where u.user_unique_id = %s 
    '''

    curs.execute(sql, "2")
    rows = curs.fetchall()  # curs.exe ~ 한거를 rows에 담음

    db.commit()
    db.close()

    return jsonify({'eachCards__list': rows})


@app.route("/mypage/mypage_modal_reload", methods=["GET"])
def mypage_modal_reload():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    sql = '''
        SELECT u.user_unique_id, u.user_profile_img_src, u.user_name, u.user_id, u.user_email, u.user_created_at, u.user_desc, mi.mbti, mi.killingtime, mi.user_birth, mi.interest FROM mypage_info mi
        left join user u on mi.user_unique_id = u.user_unique_id
        where u.user_unique_id = %s  
    '''

    curs.execute(sql, "2")
    rows = curs.fetchall()  # curs.exe ~ 한거를 rows에 담음

    db.commit()
    db.close()

    return jsonify({'eachCards__info__contents': rows})


@app.route("/mypage/mypage_upload", methods=["POST"])
def mypage_upload():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    desc_receive = (request.form['desc_give'])
    # photo_receive = request.form['photo_give']
    print(desc_receive)
    sql = '''update mypage_info set description = %s where user_unique_id = 2'''

    curs.execute(sql, desc_receive)

    rows = curs.fetchall()  # curs.exe ~ 한거를 rows에 담음
    print(rows)

    db.commit()
    db.close()

    return jsonify({'msg': '저장완료!'})


@app.route('/saveCharacters', methods=['POST'])
def saveCharacters():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    curs = db.cursor()

    category = request.form['categoryGive']
    content = request.form['contentGive']

    print(category)
    print(content)

    temp = 'update mypage_info set ' + category + ' = %s where user_unique_id = %s'
    sql = temp

    curs.execute(sql, (content, 2))

    db.commit()
    db.close()

    return jsonify({'msg': '저장완료'})


@app.route('/saveUserInfoInMyPage', methods=['POST'])
def saveUserInfoInMyPage():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    userName = request.form['userNameGive']
    userDesc = request.form['userDescGive']
    userProfileImgSrc = request.form['profileImgSrcGive']
    userUniqueId = request.form['userUniqueIdGive']

    print(userName)
    print(userDesc)
    print(userProfileImgSrc)
    print(len(userProfileImgSrc))
    print(userProfileImgSrc is None)

    if len(userProfileImgSrc) == 0:
        sql = '''
            update user set user_name = %s, user_desc = %s
            where user_unique_id = %s
        '''
        curs.execute(sql, (userName, userDesc, userUniqueId))
    else:
        sql = '''
            update user set user_name = %s, user_desc = %s, user_profile_img_src = %s
            where user_unique_id = %s
        '''
        curs.execute(sql, (userName, userDesc, userProfileImgSrc))

    db.commit()
    db.close()

    return jsonify({"msg": "수정 완료!"})


@app.route('/uploadProfileImg', methods=['POST'])
def upload():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()
    # file = request.files.getlist('files[0]')
    dir = "static/img/profileImg/"
    file = request.files['profileImg']

    # print("request" + request)
    # userUniqueId = request.files['user_unique_id']

    filename = secure_filename(file.filename)
    # print(filename)

    temp0 = os.path.splitext(filename)[0]
    temp1 = os.path.splitext(filename)[1]
    extension = ""

    print(temp0)
    print(temp1)
    # print("file= " + file)
    # print(userUniqueId)
    if temp1 == "":
        extension = "." + temp0
    else:
        extension = temp1

    now = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = "_" + now + extension

    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    sql = '''
        select user_profile_img_src from user
        where user_unique_id = %s
    '''

    curs.execute(sql, 2)
    existingImgSrc = curs.fetchall()[0][0]

    print(existingImgSrc)

    if existingImgSrc is not None:
        os.remove(existingImgSrc)

    # print(existingImgSrc)
    # print(existingImgSrc[0][0])

    os.chdir(dir)

    file.save(filename)
    # temp = os.path.dirname(file)
    # temp = os.path.basename(filename)
    # print(temp)

    os.chdir("../../../")
    dir = dir + filename

    sql = '''
            update user set user_profile_img_src = %s
            where user_unique_id = %s
        '''
    curs.execute(sql, (dir, 2))

    db.commit()
    db.close()

    return jsonify({'msg': 'success', 'profileImgSrc': dir})


@app.route('/showNewsfeedFilteredByTopic', methods=['POST'])
def showNewsfeedFilteredByTopic():
    topicNumReceive = int(request.form['topicNumGive'])
    dic = {}
    result = []

    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(host='localhost', user='root', db='sparta_sbsj', password='f2143142', charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    # posting_id 찾기
    sql = '''
        select posting_id from topics_in_posting
        where topic_num_%s = 1
    '''

    # curs.execute(sql)
    curs.execute(sql, topicNumReceive)
    rows = curs.fetchall()

    # print(rows)
    # print(len(rows))

    for i in range(len(rows)):  # posting_id로 찾기
        sql = '''
            select user_unique_id, posting_title, posting_text, posting_topic from posting
            where posting_id = %s
        '''

        curs.execute(sql, rows[i][0])
        temp = curs.fetchall()

        for j in range(len(temp)):  # posting 테이블에서 찾은거 넣기

            sql = '''
                select user_name, user_email, user_profile_img_src  from user
                where user_unique_id = %s
            '''

            curs.execute(sql, temp[j][0])
            userInfo = curs.fetchall()

            # sql = '''
            #     select * from topics_in_posting
            #     where posting_id = %s
            # '''
            #
            # curs.execute(sql, rows[i][0])
            # topicsInfo = curs.fetchall()
            # topicsArray = []
            #
            # for k in range(1, len(topicsInfo)):
            #     if topicsInfo[k] == 1:
            #         topicsArray.append(k)

            topicsArray = temp[j][3].split(" ")

            dic = {
                'posting_id': rows[i][0],
                'user_name': userInfo[0][0],
                'user_email': userInfo[0][1],
                'user_profile_img_src': userInfo[0][2],
                # 'user_unique_id' : temp[j][0],
                'posting_title': temp[j][1],
                'posting_text': temp[j][2],
                'topics_array': topicsArray
            }

            result.append(dic)

    # print(result)

    db.commit()
    db.close()

    return jsonify({'msg': 'success', 'result': result})


@app.route('/showNewsfeedOnlyMine', methods=['POST'])
def showNewsfeedOnlyMine():
    db = pymysql.connect(host=hostname, user=username, db='sparta_sbsj', password=userpw, charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    userIdReceive = request.form['userIdGive']

    sql = '''
        select user_unique_id, user_name, user_email, user_profile_img_src from user
        where user_id = %s
    '''

    curs.execute(sql, userIdReceive)
    userInfo = curs.fetchall()
    userUniqueId = userInfo[0][0]

    sql = '''
        select posting_id, posting_title, posting_text, posting_topic from posting p 
        where user_unique_id = %s
    '''

    curs.execute(sql, userUniqueId)
    rows = curs.fetchall()
    result = []

    for i in range(len(rows)):
        dic = {
            'posting_id': rows[i][0],
            'user_name': userInfo[0][1],
            'user_email': userInfo[0][2],
            'user_profile_img_src': userInfo[0][3],
            'posting_title': rows[i][1],
            'posting_text': rows[i][2],
            'topics_array': rows[i][3].split(" ")
        }

        result.append(dic)

    db.commit()
    db.close()

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
