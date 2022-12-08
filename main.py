from flask import Flask, render_template, request, jsonify
import pymysql

from werkzeug.utils import secure_filename
import os
import urllib.request
from datetime import datetime

from flask import flash, redirect

app = Flask(__name__)

dbAdress = "host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8'"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mypage')
def mymage_main():
    return render_template('mypage.html')


# 마이페이지 불러오기
@app.route("/mypage/mypage_reload", methods=["GET"])
def mypage_reload():
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    sql = '''SELECT * FROM mypage_info where user_unique_id = 1'''

    curs.execute(sql)
    rows = curs.fetchall()  # curs.exe ~ 한거를 rows에 담음

    db.commit()
    db.close()

    return jsonify({'eachCards__list': rows})


@app.route("/mypage/mypage_modal_reload", methods=["GET"])
def mypage_modal_reload():
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
    # db = pymysql.connect(dbAdress)
    curs = db.cursor()

    sql = '''SELECT * FROM mypage_info where user_unique_id = 1'''

    curs.execute(sql)
    rows = curs.fetchall()  # curs.exe ~ 한거를 rows에 담음

    db.commit()
    db.close()

    return jsonify({'eachCards__info__contents': rows})


@app.route("/mypage/mypage_upload", methods=["POST"])
def mypage_upload():
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
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


@app.route('/saveUserInfoInMyPage', methods=['POST'])
def saveUserInfoInMyPage():
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
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


# @app.route('/sendUserUniqueId')
# def sendUserUniqueId():
#     # db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
#     # curs = db.cursor()
#
#     # sql = '''select user_unique_id from user
#     #     where user_id = %s
#     # '''
#     # curs.execute(sql, request.form['userIdGive'])
#     # userUniqueId = curs.fetchall()
#
#     # db.commit()
#     # db.close()
#
#     return jsonify({"msg" : "success", "userUniqueId": ""})


@app.route('/uploadProfileImg', methods=['POST'])
def upload():
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
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

    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
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
    db = pymysql.connect(host='121.166.127.220', user='seunghun', db='sparta_sbsj', password='12345678', charset='utf8')
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
