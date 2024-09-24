# 替代問題1：收入穩定性
income_stability = int(input("您的收入穩定性如何？\n1. 不穩定，收入可能隨時減少\n2. 偶爾波動，收入大致穩定\n3. 非常穩定，幾乎沒有波動\n請選擇 (1/2/3): "))
if income_stability == 1:
    income_score = 1
elif income_stability == 2:
    income_score = 3
else:
    income_score = 5

# 替代問題2：每月結餘
monthly_savings = int(input("您每月的收入與支出情況如何？\n1. 每月幾乎無結餘，甚至入不敷出\n2. 有少量結餘，能存下一些錢\n3. 每月有較大結餘，存款穩定增加\n請選擇 (1/2/3): "))
if monthly_savings == 1:
    savings_score = 1
elif monthly_savings == 2:
    savings_score = 3
else:
    savings_score = 5

