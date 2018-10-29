import time
import requests
from schedule.dataType.Schedule import *


class Nmb(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date

    def get_schedule(self) -> [Schedule]:
        get_time = time.strptime(self.query_date, '%Y/%m/%d')
        year = time.strftime('%Y', get_time)
        month = time.strftime('%m', get_time)
        day = time.strftime('%d', get_time)

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

        schedule_list = []

        def request_nmb(calendarId, nmb_type):
            #global schedule_list
            url = "https://clients6.google.com/calendar/v3/calendars/{calendarId}/events"
            querystring = {
                "calendarId":calendarId,
                "singleEvents":"true",
                "timeZone":"Asia/Tokyo",
                "maxAttendees":"1",
                "maxResults":"250",
                "sanitizeHtml":"true",
                "timeMin":year+"-"+month+"-"+day+"T00:00:00+09:00",
                "timeMax":year+"-"+month+"-"+str(int(day)+1)+"T00:00:00+09:00",
                "key":"AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
            }

            response = requests.request("GET", url, params=querystring)
            #print(response.text)
            datas = response.json()
            #print(datas['items'])
            data_output(datas, nmb_type)
            #return datas

        def data_output(datas, nmb_type):
        	for data in datas['items']:
        		schedule = Schedule()
        		#print('summary: ', data['summary'])
        		schedule.title = data['summary']
        		schedule.event_type = nmb_type
        		if 'dateTime' in data['start']:
        			#print('start: ', data['start']['dateTime'])
        			schedule.start_time = data['start']['dateTime'][11:16]
        		if 'dateTime' in data['end']:
        			#print('end: ', data['end']['dateTime'])
        			schedule.end_time = data['end']['dateTime'][11:16]
		        if 'date' in data['start']:
		            #print('start: ', data['start']['date'])
		            schedule.start_time = data['start']['date'][11:16]
		        if 'date' in data['end']:
		            #print('end: ', data['end']['date'])
		            schedule.end_time = data['end']['date'][11:16]
		        if 'description' in data:
		            #print('description: ', data['description'])
		            schedule.description = data['description']
		        if 'location' in data:
		            #print('location: ', data['location'])
		            schedule.location = data['location']
		        schedule_list.append(schedule)

        request_nmb(birthday, '誕生日')
        request_nmb(web, 'WEB')
        request_nmb(magazine, '雑誌')
        request_nmb(event, 'イベント')
        request_nmb(hall, 'ホール公演')
        request_nmb(radio, 'ラジオ')
        request_nmb(sign, 'サイン会')
        request_nmb(handshake_meeting, '握手会')
        request_nmb(theater, 'NMB48劇場公演')
        request_nmb(other, 'その他')
        request_nmb(release, 'リリース')
        request_nmb(shamekai, '写メ会')
        request_nmb(tv, 'テレビ')

        return schedule_list
