# 匯入Blueprint模組
from flask import render_template, Blueprint, request, session, jsonify
from utils import db

# 產生目標服務藍圖
task_bp = Blueprint('task_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#任務頁面
@task_bp.route('/taskPage')
def task_page(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT a.level_id, point, upgrade_point FROM body.user_profile as a left join body.level_list as b on a.level_id = b.level_id where "Uid" = %s;', (session['uid'],))

    level_data = cursor.fetchone()

    cursor.execute('''
                   select concat('a, ',COALESCE(STRING_AGG(taskType, ', '), 'a')) AS taskType from (
                    SELECT '1' as taskType FROM body.user_profile where "Uid" = %s
                    union 
                    select taskType from (
                    SELECT '2' as taskType, create_time FROM body.weight where "Uid" = %s order by create_time desc limit 1) as w
                    where DATE(create_time) = CURRENT_DATE
                    union
                    select '3' as taskType from body.cookbook c  where "Uid" = %s and DATE(create_time) = CURRENT_DATE
                    union 
                    select taskType from (
                    SELECT '4' as taskType FROM body.v_check where "Uid" = %s and "isCheck"='1' limit 1) as c
                    union
                    select '5' as taskType from body.user_profile up where birthday is not null and gender is not null and diet is not null and "Uid" = %s
                    ) as task
                    union 
                    select concat('b, ',COALESCE(STRING_AGG(DISTINCT awardtype, ', '), 'b')) from ( 
                    SELECT awardtype FROM body.award WHERE "Uid" = %s AND DATE(create_time) = CURRENT_DATE
                    union 
                    SELECT awardtype FROM body.award WHERE "Uid" = %s AND awardtype = '5') as award;
                   ''', (uid, uid, uid, uid, uid, uid, uid))
    
    data = cursor.fetchall()

    task_data, award_data = data[0][0].split(', '), data[1][0].split(', ')
    
    connection.close()

    return render_template('/task/taskPage.html', name=name, userImage=userImage, level_data=level_data, task_data=task_data, award_data=award_data)

#taskPage - 領取獎勵
@task_bp.route('/receiveTask', methods=['POST'])
def receive_task():
    if "google_id" in session:
        uid=session['uid']
    else:
        uid='0'

    if request.method == 'POST':
        try:
            task_id = request.form['task_id']

            print(task_id)

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO body.award(awardtype, "Uid", create_time)
                VALUES (%s, %s, now());
            ''', (task_id, uid))

            cursor.execute('''
                update body.user_profile set point = point + 5, online_time = now() where "Uid" = %s;
            ''', (uid,))

            response = {'message': f'receiveTask successfully.'}
            
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            response = {'message': f'Error: {str(e)}'}
            return jsonify(response)


    