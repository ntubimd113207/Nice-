# 匯入Blueprint模組
from flask import render_template, Blueprint, session

# 產生目標服務藍圖
profile_bp = Blueprint('profile_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#個人檔案頁面
@profile_bp.route('/profilePage')
def profile_page(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/profile/profilePage.html', name=name, userImage=userImage)


#關注列表頁面
@profile_bp.route('/followList')
def follow_list(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/profile/followList.html', name=name, userImage=userImage)


#食譜收藏頁面
@profile_bp.route('/collectionList')
def collection_list(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/profile/collectionList.html', name=name, userImage=userImage)


#Q&A收藏頁面
@profile_bp.route('/QAcollection')
def QA_collection(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/profile/QAcollection.html', name=name, userImage=userImage)