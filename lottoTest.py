import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1116"

html = requests.get(url).text

'''
# 날짜 : p class="desc"
# 번호 : div class="num win" > p
# 보너스 : div class="num bonus" > p
'''

soup = BeautifulSoup(html, 'html.parser')


# 해당 회차 발표 날짜 찾기
date = soup.find('p', {"class":"desc"}).text
date = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)").date()
print(date)


# 당첨 번호 찾기
# 방법 1: 다 찾아서 split하기
numbers = soup.find('div', {"class":"num win"}) \
                .find('p').text.strip().split('\n')
print(numbers)
win_numbers_list = []
for number in numbers:
    win_numbers_list.append(int(number))
print(win_numbers_list)

## 방법 2: for 문으로 list 만들기
# wins = soup.find('div', {"class":"num win"})
# print(wins)
# nums = [win.find('span') for win in wins.find('p')]
# print(nums)
## 이건 서치랑 고민을 좀 해보자...

# 보너스 번호 찾기
# 방법 1: 한 줄에 다 찾기
bonus_num = int( \
                soup.find('div', {"class":"num bonus"}) \
                    .find('p').text.strip())
print(bonus_num)
