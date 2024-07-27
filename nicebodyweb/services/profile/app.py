# 匯入Blueprint模組
from flask import render_template, Blueprint, request, session, jsonify
from utils import db

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

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT a.level_id, point, upgrade_point, a.gender, a.birthday FROM body.user_profile as a left join body.level_list as b on a.level_id = b.level_id where "Uid" = %s;', (session['uid'],))

    profile_data = cursor.fetchone()

    connection.close()

    return render_template('/profile/profilePage.html', name=name, userImage=userImage, profile_data=profile_data)

#update - 個人檔案頁面
@profile_bp.route('/updateProfile', methods=['POST'])
def update_profile():
    uid = session['uid']

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            gender = request.form.get('gender')
            birthday = request.form.get('birthday')
            
            connection = db.get_connection()
            cursor = connection.cursor()

            gender = None if gender == '' else gender
            birthday = None if birthday == '' else birthday

            cursor.execute('UPDATE body.user_profile SET username = %s, gender = %s, birthday = %s WHERE "Uid" = %s;', (name, gender, birthday, uid))
            response = {'message': f'updateProfile successfully.'}

            session['name'] = name

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500



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