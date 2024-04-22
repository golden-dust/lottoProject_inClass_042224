import pymysql
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter

dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="lottodb")

sql = f"SELECT * FROM lotto_tbl"

cur = dbConn.cursor()
cur.execute(sql)
db_result = cur.fetchall()

cur.close()
dbConn.close()

lotto_df = pd.DataFrame(db_result, columns=["draw_no", "draw_date", "win_num1", "win_num2", "win_num3", "win_num4", "win_num5", "win_num6", "bonus_num"])

# pandas의 날짜 형식으로 변환
lotto_df['draw_date'] = pd.to_datetime(lotto_df['draw_date'])

# 추첨일에서 월(month)만 추출하여 새로운 필드 생성
lotto_df['draw_month'] = lotto_df['draw_date'].dt.month
# print(lotto_df)

by_month = lotto_df.melt(id_vars='draw_month', value_vars=["win_num1", "win_num2", "win_num3", "win_num4", "win_num5", "win_num6", "bonus_num"])
# print(by_month)

by_monthAndNum = by_month.groupby(["draw_month", "value"]).count()
print(by_monthAndNum)
top10 = by_monthAndNum.sort_values(by="variable", ascending=False).head(10)

# plt.subplot(4, 3)
top10.plot(figsize=(10,20), kind="barh", grid=True, title="by month")