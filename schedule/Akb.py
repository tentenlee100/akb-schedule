import time
import requests
from schedule.dataType.Schedule import *

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
        self.category = {
            "1": "劇場公演",
            "2": "メディア出演情報",
            "3": "イベント出演情報",
            "7": "握手会",
            "4": "グッズ",
            "5": "CD・DVD/Blu-ray",
            "6": "チケット",
        }

    def get_schedule(self) -> [Schedule]:
        get_time = time.strptime(self.query_date, '%Y/%m/%d')
        year = time.strftime('%Y', get_time)
        month = time.strftime('%m', get_time)
        day = time.strftime('%d', get_time)

        body = {'month': str(int(month)), 'year': year, 'category': 0}
        url = 'https://www.akb48.co.jp/public/api/schedule/calendar/'
        response_json = requests.post(url, data=body).json()
        today_key = year + '_' + str(int(month)) + '_' + str(int(day))
        members_api = 'https://www.akb48.co.jp/public/api/member/list/'
        members_dic = requests.post(members_api).json()["data"]
        # print(json.dumps(response_json, ensure_ascii=False))

        if today_key not in response_json["data"]["thismonth"]:
            return []

        today_list = response_json["data"]["thismonth"][today_key]

        schedule_list = []
        for schedule_dic in today_list:
            schedule = Schedule()
            schedule.title = schedule_dic["title"]
            if schedule_dic["parent_category"] in self.category:
                schedule.event_type = self.category[schedule_dic["parent_category"]]
            schedule.start_time = schedule_dic["date"][-8:-3]
            schedule.end_time = schedule_dic["end_date"][-8:-3]
            if schedule_dic["member"]:
                member_key_list = schedule_dic["member"].split(',')
            else:
                member_key_list = []
            # print(member_key_list)

            if members_dic and len(member_key_list) > 0:
                members_name_list = []
                for member_no in member_key_list:
                    if member_no in members_dic:
                        name = members_dic[member_no]["name"].replace('\t', '')
                        members_name_list.append(name)
                schedule.members = members_name_list

            schedule_list.append(schedule)

        # print(today_list)
        return schedule_list


if __name__ == '__main__':
    akb = Akb("2018/10/29")
    akb_schedule = akb.get_schedule()
    print(akb_schedule)
