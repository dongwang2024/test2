from flask import Flask, render_template, request, redirect, url_for  
import random  
  
app = Flask(__name__)  
  
# 生成一个1到100之间的随机数  
target_number = random.randint(1, 100)  
  
# 初始化尝试次数  
attempts_allowed = 6  
  
# 跟踪用户的尝试次数  
user_attempts = {}  
  
@app.route('/')  
def index():  
    # 如果用户已经开始了游戏并且有猜测记录，则获取当前尝试次数  
    attempt_count = user_attempts.get(request.remote_addr, 1)  
      
    # 如果用户已经用完了所有机会，显示结果  
    if attempt_count > attempts_allowed:  
        return render_template('result.html', target_number=target_number, attempts_allowed=attempts_allowed)  
      
    return render_template('index.html', attempt_count=attempt_count, attempts_allowed=attempts_allowed)  
  
@app.route('/guess', methods=['POST'])  
def guess():  
    guess = request.form['guess']  
      
    # 检查输入是否为数字  
    if not guess.isdigit():  
        return "请输入一个有效的数字！", 400  
      
    guess = int(guess)  
    remote_addr = request.remote_addr  
      
    # 获取或初始化用户的尝试次数  
    if remote_addr not in user_attempts:  
        user_attempts[remote_addr] = 1  
    else:  
        user_attempts[remote_addr] += 1  
      
    attempt_count = user_attempts[remote_addr]  
      
    # 检查猜测是否正确  
    if guess < target_number:  
        message = "小了！"  
    elif guess > target_number:  
        message = "大了！"  
    else:  
        return render_template('result.html', target_number=target_number, attempts_allowed=attempts_allowed)  
      
    # 如果用户用完了所有机会，重定向到结果页面  
    if attempt_count > attempts_allowed:  
        return redirect(url_for('result'))  
      
    return render_template('index.html', attempt_count=attempt_count, attempts_allowed=attempts_allowed, message=message)  
  
@app.route('/result')  
def result():  
    return render_template('result.html', target_number=target_number, attempts_allowed=attempts_allowed)  
  
if __name__ == '__main__':  
    app.run(debug=True)