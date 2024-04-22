from sqlalchemy import create_engine
import pymysql

import pandas as pd

'''
크롤링 후 새로 추가되는 데이터들은 기존 테이블에 APPEND로 추가할 수 있도록
sqlalchemy를 사용하는 방법!
'''

data = {"학번": range(2000, 2015), '성적': [70, 60, 100, 90, 50, 75, 65, 99, 78, 63, 100, 86, 53, 30, 78]}

df = pd.DataFrame(data=data, columns=['학번', '성적'])

print(df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
                                    # //user:password@host:port/db
                                                            # 한글이 있다면 -> ?charset=utf8mb4
engine.connect()

df.to_sql(name="testtbl", con=engine, if_exists="append", index=False)
