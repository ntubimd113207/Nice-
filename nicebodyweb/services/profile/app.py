# 匯入Blueprint模組
from flask import render_template, Blueprint, request, session, jsonify
from utils import db
import time

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
        name = session['name']
        userImage = session['user_image']
        uid = session['uid']
    else:
        name = '0'
        userImage = '0'
        uid = '0'

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('select * from body."CookKeepCategory" where "Uid" = %s order by create_time;', (uid,))
    collection_list = cursor.fetchall()

    collection_details = {} 
    for collection in collection_list:
        ckid = collection[0]
        cursor.execute('''
            SELECT a.*, b.title, c."userImage" 
            FROM body."CookKeep" a
            LEFT JOIN body.cookbook b ON a."Cookid" = b."Cookid"
            LEFT JOIN body.user_profile c ON b."Uid" = c."Uid"
            WHERE a."CKid" = %s 
            ORDER BY a.update_time;
            ''', (ckid,))
        
        collection_details[ckid] = cursor.fetchall()

    connection.close()

    print(collection_details)
    return render_template('/profile/collectionList.html', name=name, userImage=userImage, collection_list=collection_list, collection_details=collection_details)

#addCollection
@profile_bp.route('/addCollection', methods=['POST'])
def add_collection():
    uid = session['uid']

    if request.method == 'POST':
        try:
            collection_name = request.form.get('collectionName')
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."CookKeepCategory"("Uid", "categoryName", create_time, update_time) VALUES (%s, %s, now(), now());', (uid, collection_name))
            response = {'message': f'addCollection successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#updateCollection
@profile_bp.route('/updateCollection', methods=['POST'])
def update_collection():
    uid = session['uid']

    if request.method == 'POST':
        try:
            collection_name = request.form.get('collectionName')
            old_collection_name = request.form.get('oldcollectionName')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('UPDATE body."CookKeepCategory" SET "categoryName" = %s, update_time = now() WHERE "Uid" = %s and "categoryName" = %s;', (collection_name, uid, old_collection_name))
            response = {'message': f'updateCollection successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#deleteCollection
@profile_bp.route('/deleteCollection', methods=['POST'])
def delete_collection():
    uid = session['uid']

    if request.method == 'POST':
        try:
            collection_name = request.form.get('collectionName')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."CookKeep" WHERE "CKid" IN (SELECT "CKid" FROM body."CookKeepCategory" WHERE "Uid" = %s and "categoryName" = %s);', (uid, collection_name))

            cursor.execute('DELETE FROM body."CookKeepCategory" WHERE "Uid" = %s and "categoryName" = %s;', (uid, collection_name))
            response = {'message': f'deleteCollection successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#addCollectionDetail
@profile_bp.route('/addCollectionDetail', methods=['POST'])
def add_collection_detail():
    uid = session['uid']

    if request.method == 'POST':
        try:
            item = request.form.get('item')
            cookid = request.form.get('detailId')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."CookKeep"("CKid", "Cookid", create_time, update_time) VALUES ((SELECT "CKid" FROM body."CookKeepCategory" WHERE "Uid" = %s and "categoryName" = %s), %s, now(), now());', (uid, item, cookid))
            response = {'message': f'addCollectionDetail successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#deleteCollectionDetail
@profile_bp.route('/deleteCollectionDetail', methods=['POST'])
def delete_collection_detail():
    uid = session['uid']

    if request.method == 'POST':
        try:
            item = request.form.get('item')
            cookid = request.form.get('detailId')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."CookKeep" WHERE "Cookid" = %s and "CKid" = (SELECT "CKid" FROM body."CookKeepCategory" WHERE "Uid" = %s and "categoryName" = %s);', (cookid, uid, item))
            response = {'message': f'deleteCollectionDetail successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

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