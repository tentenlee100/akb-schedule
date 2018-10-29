from schedule.dataType.Schedule import *


# 網頁: http://www.nmb48.com/
# API: https://clients6.google.com/calendar/v3/calendars/{calendarId}/events
# method: GET
# params:
#     calendarId=05iuhma3fmhdl8508e3iiiio20%40group.calendar.google.com
#     singleEvents=true
#     timeZone=Asia%2FTokyo&maxAttendees=1
#     maxResults=250
#     sanitizeHtml=true
#     timeMin=2018-10-20T00%3A00%3A00%2B09%3A00
#     timeMax=2018-10-21T00%3A00%3A00%2B09%3A00
#     key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs
#
# calendarId:
#     生日: 05iuhma3fmhdl8508e3iiiio20@group.calendar.google.com
#     WEB: 0mjv20rnp5l39k1401pop392n4@group.calendar.google.com
#     雑誌: 3261024m48c21dka24ce1460ts@group.calendar.google.com
#     イベント: 2l1sj3tjrob16vbpc578mp7jk4@group.calendar.google.com
#     ホール公演: 2l1sj3tjrob16vbpc578mp7jk4@group.calendar.google.com
#     ラジオ: 8p87bnk3uvprptahmn7ab0ueo8@group.calendar.google.com
#     サイン会: ddl92o5j9aie7silrq86gj07pg@group.calendar.google.com
#     握手会: g9afs4ntoqs99ljs81kdoi4l6k@group.calendar.google.com
#     NMB48劇場公演: jau9mtvjop63iit4g9o1s3qkec@group.calendar.google.com
#     その他: mepcj5hof4vd7mid57quca01v8@group.calendar.google.com
#     リリース: nmb48schedule@gmail.com
#     写メ会: nodnglo3pr5ep5bocb4dg3qpm0@group.calendar.google.com
#     テレビ: oug148i963c3g23drkmgd4brbk@group.calendar.google.com

class Nmb(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_schedule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
