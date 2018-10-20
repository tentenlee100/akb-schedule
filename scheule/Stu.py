from scheule.dataType.Schedule import *

# 網頁: http://www.stu48.com/schedule/?range=future_event_end_time&sort=asc


class Stu(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_scheule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
