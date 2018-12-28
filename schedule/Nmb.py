import datetime
import requests
from schedule.dataType.Schedule import *
from bs4 import BeautifulSoup


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
#     雑誌: 2l1sj3tjrob16vbpc578mp7jk4@group.calendar.google.com
#     イベント: 3261024m48c21dka24ce1460ts@group.calendar.google.com
#     ホール公演: 7hg0gb8cu7qmfp784npu1anboc@group.calendar.google.com
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
        self.schedule_list = []

    def request_nmb(self, calendar_id, nmb_type):
        query_time_time = datetime.datetime.strptime(self.query_date, '%Y/%m/%d')

        if nmb_type == 'テレビ' or nmb_type == 'ラジオ':
            time_start = query_time_time.strftime('%Y-%m-%dT03:59:59+09:00')
            time_end = query_time_time + datetime.timedelta(days=1)
            time_end = time_end.strftime('%Y-%m-%dT03:59:59+09:00')
        else:
            time_start = query_time_time.strftime('%Y-%m-%dT00:00:00+09:00')
            time_end = query_time_time.strftime('%Y-%m-%dT23:59:59+09:00')

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
        j = response.json()
        # print(datas['items'])
        self.data_output(j, nmb_type)

    def data_output(self, datas, nmb_type):

        for data in datas['items']:
            schedule = Schedule()
            # print('summary: ', data['summary'])
            schedule.title = data['summary']
            schedule.event_type = nmb_type
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

        birthday = "05iuhma3fmhdl8508e3iiiio20@group.calendar.google.com"
        web = "0mjv20rnp5l39k1401pop392n4@group.calendar.google.com"
        magazine = "2l1sj3tjrob16vbpc578mp7jk4@group.calendar.google.com"
        event = "3261024m48c21dka24ce1460ts@group.calendar.google.com"
        hall = "7hg0gb8cu7qmfp784npu1anboc@group.calendar.google.com"
        radio = "8p87bnk3uvprptahmn7ab0ueo8@group.calendar.google.com"
        sign = "ddl92o5j9aie7silrq86gj07pg@group.calendar.google.com"
        handshake_meeting = "g9afs4ntoqs99ljs81kdoi4l6k@group.calendar.google.com"
        theater = "jau9mtvjop63iit4g9o1s3qkec@group.calendar.google.com"
        other = "mepcj5hof4vd7mid57quca01v8@group.calendar.google.com"
        release = "nmb48schedule@gmail.com"
        shamekai = "nodnglo3pr5ep5bocb4dg3qpm0@group.calendar.google.com"
        tv = "oug148i963c3g23drkmgd4brbk@group.calendar.google.com"

        self.request_nmb(birthday, '誕生日')
        self.request_nmb(web, 'WEB')
        self.request_nmb(magazine, '雑誌')
        self.request_nmb(event, 'イベント')
        self.request_nmb(hall, 'ホール公演')
        self.request_nmb(radio, 'ラジオ')
        self.request_nmb(sign, 'サイン会')
        self.request_nmb(handshake_meeting, '握手会')
        self.request_nmb(theater, 'NMB48劇場公演')
        self.request_nmb(other, 'その他')
        self.request_nmb(release, 'リリース')
        self.request_nmb(shamekai, '写メ会')
        self.request_nmb(tv, 'テレビ')

        self.schedule_list.sort(key=lambda x: x.start_time)
        return self.schedule_list


if __name__ == '__main__':
    result = Nmb("2018/11/01").get_schedule()
    print(result)
    print(f"total: {len(result)} events")
