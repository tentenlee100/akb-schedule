from scheule.dataType.Schedule import *

# AKB行事曆
#
# 網頁: https://www.akb48.co.jp/about/schedule/
# API: https://www.akb48.co.jp/public/api/schedule/calendar/
# method: POST
# input: month=10&year=2018&category=0


class Akb(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_scheule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
