# 匯入Blueprint模組
from flask import render_template, Blueprint, session

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
        userImage=session['user_image']
    else:
        name='0'
        userImage='0'

    return render_template('/task/taskPage.html', name=name, userImage=userImage)