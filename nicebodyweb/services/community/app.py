# 匯入Blueprint模組
import os
from flask import render_template, session, Blueprint, request
from utils import db

# 產生目標服務藍圖
community_bp = Blueprint('community_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#社群主頁(母畫面)
@community_bp.route('/communityMain')
def community_Main(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
        is_nutritionist=session['is_nutritionist']
    else:
        name='0'
        userImage='0'
        uid='0'
        is_nutritionist='0'

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT a.*, 
            b."userImage" AS userProfileImage, 
            b.username, 
            c.message, 
            c.update_time, 
            c."Uid" AS answerUid,
            d."userImage" AS answerUserImage
        FROM body.question AS a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        LEFT JOIN body.answer AS c ON a."BestAid" = c."Aid"
        LEFT JOIN body.user_profile AS d ON c."Uid" = d."Uid"
        ORDER BY a.create_time DESC;
        '''
    )

    question = cursor.fetchall()
    connection.close()

    for i, q in enumerate(question):
        # 構建資料夾的完整路徑
        if q[4]:
            base_folder = os.path.join('static/images/community', str(q[1])) + '/' + q[4]
        
            # 如果資料夾存在，獲取所有的檔案名稱
            if os.path.exists(base_folder):
                image_files = os.listdir(base_folder)
                # 將檔案名稱清單加入到 question 中
                question[i] = q + (image_files,)
            else:
                # 資料夾不存在，則附加空清單
                question[i] = q + ([],)


    return render_template('/community/communityMain.html', name=name, userImage=userImage, uid=uid, question=question, is_nutritionist=is_nutritionist)


#單一貼文(子畫面)
@community_bp.route('/detailedPost', methods=['GET'])
def detailed_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
        is_nutritionist=session['is_nutritionist']
    else:
        name='0'
        userImage='0'
        uid='0'
        is_nutritionist='0'
    
    connection = db.get_connection() 
    
    cursor = connection.cursor()     

    question_id = request.args.get('question_id')

    cursor.execute('''
        SELECT a.*, 
            b."userImage" AS userProfileImage, 
            b.username
        FROM body.question AS a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        WHERE a."Qid" = %s;
        ''', (question_id, )
    )

    question = cursor.fetchone()

    cursor.execute('''
        select a.*, b."userImage" from body.answer as a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        where a."Qid" = %s
        order by a.update_time desc;
        ''', (question_id, )
    )

    answer = cursor.fetchall()
    connection.close()

    if question[4]:
        base_folder = os.path.join('static/images/community', str(question[1])) + '/' + question[4]
    
        # 如果資料夾存在，獲取所有的檔案名稱
        if os.path.exists(base_folder):
            image_files = os.listdir(base_folder)
            # 將檔案名稱清單加入到 question 中
            question = question + (image_files,)
        else:
            # 資料夾不存在，則附加空清單
            question = question + ([],)

    # 將 BestAid 放置在 answer 的第一個位置
    if question[5]:
        for i, ans in enumerate(answer):
            if str(ans[0]) == str(question[5]):
                best_answer = answer.pop(i)
                answer.insert(0, best_answer)
                break

    return render_template('/community/detailedPost.html', name=name, userImage=userImage, uid=uid, question=question, answer=answer, is_nutritionist=is_nutritionist)


#AI食譜發布
@community_bp.route('/airecipePost')
def airecipe_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/community/airecipePost.html', name=name, userImage=userImage, uid=uid)