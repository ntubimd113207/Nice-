# 匯入Blueprint模組
import re
import os
import uuid
import random
import string
from flask import render_template, Blueprint, request, session, jsonify
from utils import db
from werkzeug.utils import secure_filename
from datetime import datetime
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
        uid = session['uid']
    else:
        name='0'
        userImage='default.jpg'
        uid='1'


    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT a.level_id, point, upgrade_point, a.gender, a.birthday, a."isNutritionist" FROM body.user_profile as a left join body.level_list as b on a.level_id = b.level_id where "Uid" = %s;', (uid,))

    profile_data = cursor.fetchone()

    connection.close()

    return render_template('/profile/profilePage.html', name=name, userImage=userImage, uid=uid, profile_data=profile_data)

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

#update - 個人檔案頭像
@profile_bp.route('/uploadImage', methods=['POST'])
def upload_image():
    uid = session['uid']

    if request.method == 'POST':
        try:
            image = request.files.get('file')
            if image:
                # 使用 secure_filename 確保文件名安全
                image_name = secure_filename(image.filename)

                # 生成唯一的文件名，包含時間戳和使用者 ID
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                unique_filename = f'{timestamp}_{uid}_{str(uuid.uuid4())[:8]}_{image_name}'

                base_folder = "static/images/userImage/"
                uid_folder = os.path.join(base_folder, str(uid))

                if not os.path.exists(uid_folder):
                    os.makedirs(uid_folder)

                # 確定文件保存的路徑
                image_path = os.path.join(uid_folder, unique_filename)
                image.save(image_path)

                connection = db.get_connection()
                cursor = connection.cursor()

                cursor.execute('UPDATE body.user_profile SET "userImage" = %s WHERE "Uid" = %s;', (unique_filename, uid))
                response = {'message': f'uploadImage successfully.'}

                session['user_image'] = unique_filename

                connection.commit()
                connection.close()

                return jsonify(response)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#申請營養師
@profile_bp.route('/applynutritionist', methods=['POST'])
def apply_nutritionist():
    uid = session['uid']

    if request.method == 'POST':
        try:
            union = request.form.get('union')
            files = request.files.getlist('files[]')

            # 檢查資料夾是否存在，若不存在則創建
            base_path = "static/files/nutritionist_certificate/"
            uid_folders = [d for d in os.listdir(base_path) if d.startswith(str(uid))]
            
            print(uid_folders)
            if uid_folders:
                folder_path = os.path.join(base_path, uid_folders[0])  # 返回找到的第一個資料夾
                folder_name = uid_folders[0]
            else:
                # 創建唯一的資料夾
                random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                folder_name = f"{uid}_{random_str}"
                folder_path = os.path.join(base_path, folder_name)
                os.makedirs(folder_path)

                connection = db.get_connection()
                cursor = connection.cursor()

                cursor.execute('''INSERT INTO body.nutritionist_apply
                        ("Uid", area_id, certificate, create_time, update_time)
                        VALUES(%s, %s, %s, now(), now());''', (uid, union, folder_name))
                
                cursor.execute('UPDATE body.user_profile SET "isNutritionist" = 1 WHERE "Uid" = %s;', (uid,))

                response = {'message': f'applyNutritionist successfully.'}

                connection.commit()
                connection.close()

            for file in files:
                if file and file.filename:
                    file.save(os.path.join(folder_path, file.filename))

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
            SELECT a.*, b.title, c."userImage" , c."Uid"
            FROM body."CookKeep" a
            LEFT JOIN body.cookbook b ON a."Cookid" = b."Cookid"
            LEFT JOIN body.user_profile c ON b."Uid" = c."Uid"
            WHERE a."CKid" = %s 
            ORDER BY a.update_time;
            ''', (ckid,))
        
        collection_details[ckid] = cursor.fetchall()

    connection.close()

    return render_template('/profile/collectionList.html', name=name, userImage=userImage, collection_list=collection_list, collection_details=collection_details, uid=uid)

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
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'
    
    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('select * from body."QnAKeepCategory" where "Uid" = %s order by create_time;', (uid,))
    collection_list = cursor.fetchall()

    collection_details = {} 
    for collection in collection_list:
        Qkid = collection[0]
        cursor.execute('''
            SELECT a.*, b.title, c."userImage" , c."Uid"
            FROM body."QnAKeep" a
            LEFT JOIN body.question b ON a."Qid" = b."Qid"
            LEFT JOIN body.user_profile c ON b."Uid" = c."Uid"
            WHERE a."QKid" = %s 
            ORDER BY a.update_time;
            ''', (Qkid,))
        
        collection_details[Qkid] = cursor.fetchall()

    connection.close()

    return render_template('/profile/QAcollection.html', name=name, userImage=userImage, collection_list=collection_list, collection_details=collection_details, uid=uid)

#updateQnACollection
@profile_bp.route('/updateQnACollection', methods=['POST'])
def update_QnAcollection():
    uid = session['uid']

    if request.method == 'POST':
        try:
            collection_name = request.form.get('collectionName')
            old_collection_name = request.form.get('oldcollectionName')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('UPDATE body."QnAKeepCategory" SET "categoryName" = %s, update_time = now() WHERE "Uid" = %s and "categoryName" = %s;', (collection_name, uid, old_collection_name))
            response = {'message': f'updateCollection successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#deleteQnACollection
@profile_bp.route('/deleteQnACollection', methods=['POST'])
def delete_QnAcollection():
    uid = session['uid']

    if request.method == 'POST':
        try:
            collection_name = request.form.get('collectionName')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."QnAKeep" WHERE "CKid" IN (SELECT "CKid" FROM body."QnAKeepCategory" WHERE "Uid" = %s and "categoryName" = %s);', (uid, collection_name))

            cursor.execute('DELETE FROM body."QnAKeepCategory" WHERE "Uid" = %s and "categoryName" = %s;', (uid, collection_name))
            response = {'message': f'deleteQnACollection successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#addQnACollectionDetail
@profile_bp.route('/addQnACollectionDetail', methods=['POST'])
def add_QnAcollection_detail():
    uid = session['uid']

    if request.method == 'POST':
        try:
            item = request.form.get('item')
            Qid = request.form.get('detailId')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."QnAKeep"("QKid", "Qid", create_time, update_time) VALUES ((SELECT "QKid" FROM body."QnAKeepCategory" WHERE "Uid" = %s and "categoryName" = %s), %s, now(), now());', (uid, item, Qid))
            response = {'message': f'addCollectionDetail successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#deleteQnACollectionDetail
@profile_bp.route('/deleteQnACollectionDetail', methods=['POST'])
def delete_QnAcollection_detail():
    uid = session['uid']

    if request.method == 'POST':
        try:
            item = request.form.get('item')
            Qid = request.form.get('detailId')

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."QnAKeep" WHERE "Qid" = %s and "QKid" = (SELECT "QKid" FROM body."QnAKeepCategory" WHERE "Uid" = %s and "categoryName" = %s);', (Qid, uid, item))
            response = {'message': f'deleteCollectionDetail successfully.'}

            connection.commit()
            connection.close()
          
            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500