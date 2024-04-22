from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd

from sqlalchemy import create_engine
import pymysql


def get_lotto_number(draw_num):     # 추첨 회차를 입력 받아 로또 당첨 번호 크롤링하는 함수
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={draw_num}"

    html = requests.get(url).text

    '''
    # 날짜 : p class="desc"
    # 번호 : div class="num win" > p
    # 보너스 : div class="num bonus" > p
    '''

    soup = BeautifulSoup(html, 'html.parser')

    # 해당 회차 발표 날짜 찾기
    raw_date = soup.find('p', {"class": "desc"}).text
    draw_date = datetime.strptime(raw_date, "(%Y년 %m월 %d일 추첨)").date()

    # 당첨 번호 찾기
    numbers_in_str = soup.find('div', {"class": "num win"}) \
        .find('p').text.strip().split('\n')

    win_numbers_list = []
    for number in numbers_in_str:
        win_numbers_list.append(int(number))

    # 보너스 번호 찾기
    bonus_num = int(
        soup.find('div', {"class": "num bonus"})
            .find('p').text.strip()
    )

    result_dict = {
        "draw_date": draw_date,
        "win_nums": win_numbers_list,
        "bonus_num": bonus_num
    }

    return result_dict


lotto_list = []

# 최신 회차 번호 크롤링
def get_recent_draw_number():
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    latest_draw_no = int(soup.find("strong", {"id":"lottoDrwNo"}).text.strip())
    return latest_draw_no


for count in range(1, get_recent_draw_number()+1):
    lotto_result = get_lotto_number(count)
    lotto_list.append({
        "count": count,  # 로또 추첨 회차
        "draw_date": lotto_result["draw_date"],  # 로또 추첨일
        "win_num_1": lotto_result["win_nums"][0],   # 로또 당첨 번호 1
        "win_num_2": lotto_result["win_nums"][1],
        "win_num_3": lotto_result["win_nums"][2],
        "win_num_4": lotto_result["win_nums"][3],
        "win_num_5": lotto_result["win_nums"][4],
        "win_num_6": lotto_result["win_nums"][5],
        "bonus_num": lotto_result["bonus_num"]      # 로또 보너스 번호
    })
    print("draw number", count, "completed")

# print(lotto_list)

lotto_df = pd.DataFrame(data=lotto_list,
             columns=["count", "draw_date", "win_num_1", "win_num_2", "win_num_3", "win_num_4", "win_num_5", "win_num_6", "bonus_num"])
# print(lotto_df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
                                    # //user:password@host:port/db
                                                            # 한글이 있다면 -> ?charset=utf8mb4
engine.connect()

lotto_df.to_sql(name="lotto_tbl", con=engine, if_exists="append", index=False)