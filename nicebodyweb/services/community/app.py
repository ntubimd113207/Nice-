# 匯入Blueprint模組
from flask import render_template, session, Blueprint

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
    else:
        name='0'
        userImage='0'

    return render_template('/community/communityMain.html', name=name, userImage=userImage)


#單一貼文(子畫面)
@community_bp.route('/detailedPost')
def detailed_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/community/detailedPost.html', name=name, userImage=userImage)


#AI食譜發布
@community_bp.route('/airecipePost')
def airecipe_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/community/airecipePost.html', name=name, userImage=userImage)