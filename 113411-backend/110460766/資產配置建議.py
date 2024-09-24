def risk_tolerance_assessment():
    """
    根據四個問題評估投資者的風險承受度，並建議資產配置。
    """
    # 問題1：財務狀況
    financial_status = int(input("您的資產與負債比是多少？\n1. < 1\n2. 1 - 3\n3. > 3\n請選擇 (1/2/3): "))
    if financial_status == 1:
        financial_score = 1
    elif financial_status == 2:
        financial_score = 3
    else:
        financial_score = 5

    # 問題2：投資經驗
    experience = int(input("您的投資經驗有多少年？\n1. 無經驗\n2. 1 - 5 年\n3. 超過 5 年\n請選擇 (1/2/3): "))
    if experience == 1:
        experience_score = 1
    elif experience == 2:
        experience_score = 3
    else:
        experience_score = 5

    # 問題3：投資目標期限
    investment_goal = int(input("您的投資期限是多久？\n1. 少於 3 年\n2. 3 - 10 年\n3. 超過 10 年\n請選擇 (1/2/3): "))
    if investment_goal == 1:
        goal_score = 1
    elif investment_goal == 2:
        goal_score = 3
    else:
        goal_score = 5

    # 問題4：風險偏好
    risk_preference = int(input("您能承受的最大損失是多少？\n1. 5% 以下\n2. 5% - 15%\n3. 超過 15%\n請選擇 (1/2/3): "))
    if risk_preference == 1:
        risk_score = 1
    elif risk_preference == 2:
        risk_score = 3
    else:
        risk_score = 5

    # 計算總分
    total_score = financial_score + experience_score + goal_score + risk_score

    # 根據總分進行資產配置建議
    if total_score >= 16:
        allocation = "建議高風險投資，股票佔比 80%，儲蓄佔比 20%。"
    elif 8 <= total_score < 16:
        allocation = "建議中等風險投資，股票佔比 60%，儲蓄佔比 40%。"
    else:
        allocation = "建議低風險投資，股票佔比 40%，儲蓄佔比 60%。"

    print(f"您的風險承受度分數是 {total_score}，{allocation}")
    
    return total_score

# 執行風險承受度評估
risk_tolerance_assessment()
