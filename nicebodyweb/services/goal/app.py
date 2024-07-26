# 匯入Blueprint模組
import re
import os
import uuid
from flask import jsonify, render_template, session, request, jsonify, Blueprint
from utils import db
from werkzeug.utils import secure_filename
from datetime import datetime

# 產生目標服務藍圖
goal_bp = Blueprint('goal_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

contrast_image_path = "/static/images/contrast"

@goal_bp.route('/goalMain', methods=['GET', 'POST'])
def goal_main(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='1'
        userImage='0'

    if request.method == 'POST':
        try:
            data = request.json
            isChecked = data.get('checked')
            goalId = data.get('id')

            if isChecked is None or goalId is None:
                return jsonify({'error': 'Invalid request data.'}), 400

            connection = db.get_connection() 
            cursor = connection.cursor()

            if isChecked:
                cursor.execute("INSERT INTO body.\"checkIn\"(\"ChCategoryid\", create_time) VALUES(%s, now())", (goalId,))
                response = {'message': f'checkIn {goalId} inserted successfully.'}
            else:
                cursor.execute("DELETE FROM body.\"checkIn\" WHERE \"ChCategoryid\" = %s", (goalId,))
                response = {'message': f'checkIn {goalId} deleted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    else:
        try:
            connection = db.get_connection() 
            cursor = connection.cursor()     
            cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid", "isCheck"  FROM body.v_check where "Uid" = %s order by create_time;', (uid,))
            data = cursor.fetchall()

            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d')

            cursor.execute('''
                SELECT COALESCE(a.weight, '0') AS weight
                FROM (
                    SELECT "Wid", weight, DATE(create_time) AS create_time
                    FROM body.weight
                    WHERE "Uid" = %s
                ) AS a
                RIGHT JOIN (
                    SELECT (DATE %s - INTERVAL '1 day' * i) AS create_time
                    FROM generate_series(0, 6) AS t(i)
                ) AS b
                ON a.create_time = b.create_time
                ORDER BY b.create_time;
            '''
                           ,(uid, formatted_date))
            weight = cursor.fetchall()
            weight = [item[0] for item in weight]
            weight = [float(w) for w in weight]
            print(weight)

            cursor.execute('SELECT before_image, after_image FROM body.contrast WHERE "Uid" = %s', (uid,))
            contrast = cursor.fetchone()

            connection.close()

            if contrast is None:
                contrast = (None, None)
            return render_template('/goal/goalMain.html', data=data, weight=weight, contrast=contrast, contrast_image_path=contrast_image_path, name=name, userImage=userImage, uid=uid)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#新增 - 打卡目標
@goal_bp.route('/saveCheckbox', methods=['POST'])
def save_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            icon_id = data['iconId']
            text = data['text']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."checkCategory"("checkName", "Uid", "Iconid", create_time, update_time) VALUES(%s, %s, %s, now(), now())', (text, uid, icon_id))
            response = {'message': f'saveCheckbox inserted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#修改 - 打卡目標
@goal_bp.route('/updateCheckbox', methods=['POST'])
def update_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            icon_id = data['iconId']
            text = data['text']
            goal_id = data['id']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('UPDATE body."checkCategory" SET "checkName"=%s, "Iconid"=%s, update_time=now() WHERE "Uid"=%s and "ChCategoryid"=%s;', (text, icon_id, uid, goal_id))
            response = {'message': f'updateCheckbox successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#刪除 - 打卡目標
@goal_bp.route('/deleteCheckbox', methods=['POST'])
def delete_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            goal_id = data['id']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."checkCategory" WHERE "Uid"=%s and "ChCategoryid"=%s;', (uid, goal_id,))
            response = {'message': f'deleteCheckbox successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#打卡目標列表
@goal_bp.route('/checkList')
def check_list(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='1'
        userImage='0'

    connection = db.get_connection() 
    cursor = connection.cursor()     
    cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid" FROM body."checkCategory" where "Uid" = %s order by create_time;', (uid,))
    data = cursor.fetchall()
    connection.close()   
    return render_template('/goal/checkList.html', data=data, name=name, userImage=userImage)

#體重紀錄列表
@goal_bp.route('/weightList')
def weight_list(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='0'
        userImage='0'
        
    connection = db.get_connection() 
    cursor = connection.cursor()     
    cursor.execute('SELECT "Wid", weight, TO_CHAR(create_time, \'YYYY/MM/DD\') FROM body.weight where "Uid"  = %s;', (uid,))
    data = cursor.fetchall()
    connection.close() 
    return render_template('/goal/weightList.html', data=data, name=name, userImage=userImage)

#新增 - 今日體重
@goal_bp.route('/saveTodayWeight', methods=['POST'])
def save_todayWeight():
    uid=session['uid']

    if request.method == 'POST':
        try:
            weight = request.form.get('weight')

            connection = db.get_connection() 
            cursor = connection.cursor()

            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d')

            cursor.execute('INSERT INTO body.weight(weight, "Uid", create_time, update_time) VALUES(%s, %s, %s, now())', (weight, uid, formatted_date))
            response = {'message': f'deleteCheckbox successfully.'}
            
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

# uploadBeforeImage
@goal_bp.route('/uploadBeforeImage', methods=['POST'])
def upload_before_image():
    uid = session['uid']

    if request.method == 'POST':
        try:
            image = request.files.get('image')
            if image:
                # 使用 secure_filename 確保文件名安全
                image_name = secure_filename(image.filename)

                # 生成唯一的文件名，包含時間戳和使用者 ID
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                unique_filename = f'{timestamp}_{uid}_{str(uuid.uuid4())[:8]}_{image_name}'

                base_folder = 'static/images/contrast/'
                uid_folder = os.path.join(base_folder, str(uid))

                if not os.path.exists(uid_folder):
                    os.makedirs(uid_folder)

                # 確定文件保存的路徑
                image_path = os.path.join(uid_folder, unique_filename)
                image.save(image_path)

                connection = db.get_connection() 
                cursor = connection.cursor()

                cursor.execute('SELECT "Uid" FROM body.contrast WHERE "Uid" = %s', (uid,))
                existing_uid = cursor.fetchone()

                if existing_uid:
                    cursor.execute('UPDATE body.contrast SET before_image = %s, update_time = now() WHERE "Uid" = %s',
                                   (unique_filename, uid))
                    message = 'Updated existing record.'
                else:
                    print(uid, unique_filename)
                    cursor.execute('INSERT INTO body.contrast("Uid", before_image, create_time, update_time) VALUES(%s, %s, now(), now())',
                                   (uid, unique_filename))
                    message = 'Inserted new record.'

                connection.commit()
                connection.close()

                return jsonify({'message': 'uploadBeforeImage successfully', 'image_url': f'/static/images/contrast/{unique_filename}'})
            else:
                return jsonify({'error': 'No image uploaded'}), 400
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# uploadAfterImage
@goal_bp.route('/uploadAfterImage', methods=['POST'])
def upload_after_image():
    uid = session['uid']

    if request.method == 'POST':
        try:
            image = request.files.get('image')
            if image:
                # 使用 secure_filename 確保文件名安全
                image_name = secure_filename(image.filename)

                # 生成唯一的文件名，包含時間戳和使用者 ID
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                unique_filename = f'{timestamp}_{uid}_{str(uuid.uuid4())[:8]}_{image_name}'

                base_folder = 'static/images/contrast/'
                uid_folder = os.path.join(base_folder, str(uid))

                if not os.path.exists(uid_folder):
                    os.makedirs(uid_folder)

                # 確定文件保存的路徑
                image_path = os.path.join(uid_folder, unique_filename)
                image.save(image_path)

                connection = db.get_connection() 
                cursor = connection.cursor()

                cursor.execute('SELECT "Uid" FROM body.contrast WHERE "Uid" = %s', (uid,))
                existing_uid = cursor.fetchone()

                if existing_uid:
                    cursor.execute('UPDATE body.contrast SET after_image = %s, update_time = now() WHERE "Uid" = %s',
                                   (unique_filename, uid))
                    message = 'Updated existing record.'
                else:
                    print(uid, unique_filename)
                    cursor.execute('INSERT INTO body.contrast("Uid", after_image, create_time, update_time) VALUES(%s, %s, CURRENT_DATE, now())',
                                   (uid, unique_filename))
                    message = 'Inserted new record.'

                connection.commit()
                connection.close()

                return jsonify({'message': 'uploadAfterImage successfully', 'image_url': f'/static/images/contrast/{unique_filename}'})
            else:
                return jsonify({'error': 'No image uploaded'}), 400
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# clearImage
@goal_bp.route('/clearImage', methods=['POST'])
def delete_contrast_image():
    uid = session['uid']

    if request.method == 'POST':
        try:
            image_type = request.form.get('type')

            connection = db.get_connection() 
            cursor = connection.cursor()

            if image_type == 'before':
                cursor.execute('UPDATE body.contrast SET before_image = NULL, update_time = now() WHERE "Uid" = %s', (uid,))
            elif image_type == 'after':
                cursor.execute('UPDATE body.contrast SET after_image = NULL, update_time = now() WHERE "Uid" = %s', (uid,))

            connection.commit()
            connection.close()

            return jsonify({'message': 'deletecontrastImage successfully'})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# 新增體重紀錄
@goal_bp.route('/saveWeight', methods=['POST'])
def save_weight():
    uid = session['uid']

    if request.method == 'POST':
        try:
            weight = request.form.get('weight')
            date = request.form.get('date')

            connection = db.get_connection() 
            cursor = connection.cursor()
        
            cursor.execute(
                '''
                INSERT INTO body.weight("Uid", weight, create_time, update_time)
                VALUES (%s, %s, %s, now())
                ON CONFLICT ("Uid", create_time)
                DO UPDATE SET
                    weight = EXCLUDED.weight,
                    update_time = now();
                ''', (uid, weight, date))
            response = {'message': f'saveWeight inserted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

