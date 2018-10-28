from schedule.dataType.Schedule import *

# 網頁: http://www.hkt48.jp/schedule/

class Hkt(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_schedule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
