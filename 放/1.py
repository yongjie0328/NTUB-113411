from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('/評估結果.html')

@app.route('/風險承受評估表單', methods=['POST'])
def result():
    # 從表單中獲取數據
    monthly_savings = int(request.form['monthly_savings'])
    experience = int(request.form['experience'])
    investment_goal = int(request.form['investment_goal'])
    risk_preference = int(request.form['risk_preference'])

    # 計算風險承受度分數
    if monthly_savings == 1:
        savings_score = 1
    elif monthly_savings == 2:
        savings_score = 3
    else:
        savings_score = 5

    if experience == 1:
        experience_score = 1
    elif experience == 2:
        experience_score = 3
    else:
        experience_score = 5

    if investment_goal == 1:
        goal_score = 1
    elif investment_goal == 2:
        goal_score = 3
    else:
        goal_score = 5

    if risk_preference == 1:
        risk_score = 1
    elif risk_preference == 2:
        risk_score = 3
    else:
        risk_score = 5

    total_score = savings_score + experience_score + goal_score + risk_score

    # 根據總分提供資產配置建議
    if total_score >= 16:
        allocation = "建議高風險投資，股票佔比 80%，儲蓄佔比 20%。"
    elif 8 <= total_score < 16:
        allocation = "建議中等風險投資，股票佔比 60%，儲蓄佔比 40%。"
    else:
        allocation = "建議低風險投資，股票佔比 40%，儲蓄佔比 60%。"

    return render_template('風險承受評估表單.html', score=total_score, allocation=allocation)

if __name__ == '__main__':
    app.run(debug=True)
