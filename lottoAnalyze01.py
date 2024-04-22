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
# print(lotto_df)

# 당첨번호와 보너스 번호만 추출하여 데이터프레임 생성
lotto_nums_df = pd.DataFrame(lotto_df.iloc[0:, 2:])
# print(lotto_nums_df)
# print(lotto_nums_df.value_counts())
lotto_nums = []

# for row in lotto_nums_df["win_num1"]:
#         lotto_nums.append(row)
#         print(row)
# print(lotto_nums)


lotto_nums = list(lotto_nums_df["win_num1"]) + list(lotto_nums_df["win_num2"]) + list(lotto_nums_df["win_num3"]) + list(lotto_nums_df["win_num4"]) + list(lotto_nums_df["win_num5"]) + list(lotto_nums_df["win_num6"]) + list(lotto_nums_df["bonus_num"])
print(len(lotto_nums))

'''
lotto_num_freq = {}
for i in range(1, 46):
    count = 0
    for num in lotto_nums:
        if num == i:
            count += 1
    lotto_num_freq[i] = count

print(lotto_num_freq)
'''

freq_lotto_num = Counter(lotto_nums)
print(freq_lotto_num)

data = pd.Series(freq_lotto_num)
data = data.sort_index()
data.plot(kind="barh", grid=True, title="lotto number frequency data", figsize=(15, 15))

plt.show()