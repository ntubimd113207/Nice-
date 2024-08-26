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
        uid='1'
        userImage='0'

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT a.level_id, point, upgrade_point FROM body.user_profile as a left join body.level_list as b on a.level_id = b.level_id where "Uid" = %s;', (uid,))

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
                    select '5' as taskType from body.user_profile up where birthday is not null and gender is not null and "Uid" = %s
                    ) as task
                    union 
                    select concat('b, ',COALESCE(STRING_AGG(DISTINCT awardtype, ', '), 'b')) from ( 
                    SELECT awardtype FROM body.award WHERE "Uid" = %s AND DATE(create_time) = CURRENT_DATE
                    union 
                    SELECT awardtype FROM body.award WHERE "Uid" = %s AND awardtype = '5') as award;
                   ''', (uid, uid, uid, uid, uid, uid, uid))
    
    data = cursor.fetchall()

    task_data, award_data = data[0][0].split(', '), data[1][0].split(', ')

    cursor.execute('''
                   select count(*), '1' as  num from body."checkIn" as a
                    left join body."checkCategory" as b 
                    on a."ChCategoryid" = b."ChCategoryid"
                    where "Uid" = %s
                    union
                    select count(*), '2' as  num from body.weight
                    where "Uid" = %s
                    union
                    select count(*), '3' as  num from body.cookbook c 
                    where "Uid" = %s
                    union
                    select count(*), '4' as  num from body."cookbookMessage"
                    where "Uid" = %s
                    order by num;
                    ''' % (uid, uid, uid, uid))
    milestone = cursor.fetchall()

    cursor.execute('''
                    select a.*, b.username, b."userImage" from body.achievement as a
                    left join body.user_profile as b on a."Uid" = b."Uid" 
                    where content is not null
                    order by create_time desc;
                   ''')
    
    achievement = cursor.fetchall()

    cursor.execute('''
        select count(*) from body.achievement a 
        where "Uid" = %s and "content" is null
                   ''', (uid,))
    
    achieve_time = cursor.fetchone()

    connection.close()

    return render_template('/task/taskPage.html', name=name, userImage=userImage, level_data=level_data, task_data=task_data, award_data=award_data, milestone=milestone, uid=uid, achievement=achievement, achieve_time=achieve_time)

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

#里程碑留言
@task_bp.route('/goalMessage', methods=['POST'])
def goal_message():
    if "google_id" in session:
        uid=session['uid']
    else:
        uid='0'

    if request.method == 'POST':
        try:
            message = request.form['message']

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('''
                UPDATE body."achievement"
                SET content = %s, create_time = now()
                WHERE "Achieveid" = (SELECT "Achieveid" FROM body."achievement" WHERE "Uid" = %s AND "content" is null ORDER BY create_time LIMIT 1);
            ''', (message, uid))

            response = {'message': f'goalMessage successfully.'}
            
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            response = {'message': f'Error: {str(e)}'}
            return jsonify(response)
    