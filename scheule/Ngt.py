from scheule.dataType.Schedule import *


# 網頁: https://ngt48.jp/schedule
#
# API: https://clients6.google.com/calendar/v3/calendars/{calendarId}/events
# method: GET
# params:
#     calendarId=05iuhma3fmhdl8508e3iiiio20%40group.calendar.google.com
#     singleEvents=true
#     timeZone=Asia%2FTokyo
#     maxAttendees=1
#     maxResults=250
#     sanitizeHtml=true
#     timeMin=2018-10-20T00%3A00%3A00%2B09%3A00
#     timeMax=2018-10-21T00%3A00%3A00%2B09%3A00
#     key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs
#
# calendarId:
#     公演: 5qokjrh6f4ee9op129j0mfvioc@group.calendar.google.com
#     オーディション: 6sqi65kh3u38tmpjibnmordj10@group.calendar.google.com
#     誕生日: crnkrfg8jl3r8csfjjodj09uag@group.calendar.google.com
#     テレビ: oug148i963c3g23drkmgd4brbk@group.calendar.google.com
#     その他: j9dlo0i5cjtu4v1cqe16jgu50g@group.calendar.google.com
#     日本の祝日: ja.japanese#holiday@group.v.calendar.google.com
#     リリース: m2ajd5t81ig9at9bmvnqn48otk@group.calendar.google.com
#     ngt48cal@gmail.com: ngt48cal@gmail.com
#     メディア: nmdaqiikpgmkdbigrkfkkavp7g@group.calendar.google.com
#     握手会: o0vl9n0d4jncr0f73cj98mnnuo@group.calendar.google.com
#     イベント: r265gb7ufvmtugtjjpj03nf854@group.calendar.google.com
#     Web: uruvbla1g4sqpj3d6qn1ai2a0s@group.calendar.google.com


class Ngt(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_scheule(self) -> [Schedule]:

        schedule_list = []
        schedule_list.append(Schedule())

        return schedule_list
