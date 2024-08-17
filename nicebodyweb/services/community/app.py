# 匯入Blueprint模組
import os
from flask import render_template, session, Blueprint
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
@community_bp.route('/detailedPost')
def detailed_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/community/detailedPost.html', name=name, userImage=userImage, uid=uid)


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