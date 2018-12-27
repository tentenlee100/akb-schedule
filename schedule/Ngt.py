import datetime
import requests
from schedule.dataType.Schedule import *
from bs4 import BeautifulSoup

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
        self.schedule_list = []

    def request_ngt(self, calendar_id, ngt_type):
        time_start = datetime.datetime.strptime(self.query_date, '%Y/%m/%d').strftime('%Y-%m-%dT00:00:00+09:00')
        time_end = datetime.datetime.strptime(self.query_date, '%Y/%m/%d').strftime('%Y-%m-%dT23:59:59+09:00')

        url = "https://clients6.google.com/calendar/v3/calendars/{calendarId}/events"
        querystring = {
            "calendarId": calendar_id,
            "singleEvents": "true",
            "timeZone": "Asia/Tokyo",
            "maxAttendees": "1",
            "maxResults": "250",
            "sanitizeHtml": "true",
            "timeMin": time_start,
            "timeMax": time_end,
            "key": "AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
        }

        response = requests.request("GET", url, params=querystring)
        # print(response.text)
        datas = response.json()
        # print(datas['items'])
        self.data_output(datas, ngt_type)

    def data_output(self, datas, ngt_type):
        for data in datas['items']:
            schedule = Schedule()
            # print('summary: ', data['summary'])
            schedule.title = data['summary']
            schedule.event_type = ngt_type
            if 'dateTime' in data['start']:
                # print('start: ', data['start']['dateTime'])
                schedule.start_time = data['start']['dateTime'][11:16]
                if int(schedule.start_time[0:2]) <= 3:
                    schedule.start_time = str(int(schedule.start_time[0:2]) + 24) + schedule.start_time[2:]
            if 'dateTime' in data['end']:
                # print('end: ', data['end']['dateTime'])
                schedule.end_time = data['end']['dateTime'][11:16]
                if int(schedule.end_time[0:2]) < 3:
                    schedule.end_time = str(int(schedule.end_time[0:2]) + 24) + schedule.end_time[2:]
            if 'date' in data['start']:
                # print('start: ', data['start']['date'])
                schedule.start_time = ""
            if 'date' in data['end']:
                # print('end: ', data['end']['date'])
                schedule.end_time = ""
            if 'description' in data:
                # print('description: ', data['description'])
                description = data['description']
                soup = BeautifulSoup(description, 'html.parser').get_text()
                schedule.description = soup
            if 'location' in data:
                # print('location: ', data['location'])
                schedule.location = data['location']
            self.schedule_list.append(schedule)

    def get_schedule(self) -> [Schedule]:

        performance = "5qokjrh6f4ee9op129j0mfvioc@group.calendar.google.com"
        audition = "6sqi65kh3u38tmpjibnmordj10@group.calendar.google.com"
        birthday = "crnkrfg8jl3r8csfjjodj09uag@group.calendar.google.com"
        other = "j9dlo0i5cjtu4v1cqe16jgu50g@group.calendar.google.com"
        # holidays = "ja.japanese#holiday@group.v.calendar.google.com"
        release = "m2ajd5t81ig9at9bmvnqn48otk@group.calendar.google.com"
        radio = "madmrl5ev8ueva1kfddn5oh08g@group.calendar.google.com"
        ngt48cal = "ngt48cal@gmail.com"
        media = "nmdaqiikpgmkdbigrkfkkavp7g@group.calendar.google.com"
        handshake_meeting = "o0vl9n0d4jncr0f73cj98mnnuo@group.calendar.google.com"
        tv = "o4fhr788ajuhhj22bk93bvk4r4@group.calendar.google.com"
        event = "r265gb7ufvmtugtjjpj03nf854@group.calendar.google.com"
        magazine = "u2dktkl97uipdnqiirikm99eo4@group.calendar.google.com"
        web = "uruvbla1g4sqpj3d6qn1ai2a0s@group.calendar.google.com"

        self.request_ngt(performance, '公演')
        self.request_ngt(audition, 'オーディション')
        self.request_ngt(birthday, '誕生日')
        self.request_ngt(other, 'その他')
        # self.request_ngt(holidays, '日本の祝日')
        self.request_ngt(release, 'リリース')
        self.request_ngt(radio, 'ラジオ')
        self.request_ngt(ngt48cal, 'ngt48cal@gmail.com')
        self.request_ngt(media, 'メディア')
        self.request_ngt(handshake_meeting, '握手会')
        self.request_ngt(tv, 'テレビ')
        self.request_ngt(event, 'イベント')
        self.request_ngt(magazine, '新聞・雑誌')
        self.request_ngt(web, 'WEB')

        self.schedule_list.sort(key=lambda x: x.start_time)
        return self.schedule_list


if __name__ == '__main__':
    result = Ngt("2018/12/26").get_schedule()
    print(result)
    print(f"total: {len(result)} events")
