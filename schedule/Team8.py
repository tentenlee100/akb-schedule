from schedule.dataType.Schedule import *

# TEAM 8行事曆
# 網頁: https://toyota-team8.jp/schedule/index.php
# 指定月份網頁: https://toyota-team8.jp/schedule/201810/index.php

class Team8(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_schedule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
