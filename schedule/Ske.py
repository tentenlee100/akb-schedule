import time
import requests
from bs4 import BeautifulSoup
from schedule.dataType.Schedule import *

# 網頁: http://www.ske48.co.jp/schedule/calendar.php


class Ske(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10

    def __init__(self, query_date):
        self.query_date = query_date
        self.category = {
            'stage': '公演',
            'release': 'リリース',
            'event': 'イベント',
            'akushukai': '握手会',
            'media': 'メディア',
            'audition': 'オーディション',
            'web': 'WEB',
            'etc': 'その他',
            'bday': '誕生日',
        }

    def _get_html(self, url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return BeautifulSoup(html, 'html.parser')

    def _get_event_detail(self, link, category):
        url = 'http://www.ske48.co.jp/schedule/?{query_params}'.format(query_params=link[3:])
        html = self._get_html(url)
        members = [a.string for a in html.select('.memberProfile span > a')]
        html_string = html.find('div', class_='detail').get_text()
        # print(html_string)
        check_start_time_index = html_string.find(":")
        # 看能不能拿到開始時間
        start_time = ""
        if check_start_time_index > -1:
            # 查看:前後數否為數字(前1或前2)
            before2 = html_string[check_start_time_index - 2:check_start_time_index]
            before1 = html_string[check_start_time_index - 1:check_start_time_index]
            end2 = html_string[check_start_time_index + 1:check_start_time_index + 3]
            # print("before2 :{} before1:{}  end2: {}".format(before2, before1, end2))
            if before2.isdigit() and end2.isdigit():
                start_time = before2 + ":" + end2
            elif before1.isdigit() and end2.isdigit():
                start_time = "0" + before1 + ":" + end2

        return {
            'members': members,
            'start_time': start_time
        }

    def get_schedule(self) -> [Schedule]:
        query_date = time.strptime(self.query_date, '%Y/%m/%d')
        query_year = time.strftime('%Y', query_date)
        query_month = time.strftime('%m', query_date)
        query_day = int(time.strftime('%d', query_date))

        schedule_list_url = 'http://www.ske48.co.jp/schedule/calendar.php?y={year}&m={month}'.format(year=query_year, month=query_month)
        schedule_list_html = self._get_html(schedule_list_url)

        schedule_list = []
        event_list = schedule_list_html.select(
            'table[title="SCHEDULE"] > a[name="{day}"] + tr li'.format(day=query_day))
        for event in event_list:
            category = event.get('class')[0]
            event_link = event.find('a').get('href')
            detail = self._get_event_detail(event_link, category)
            schedule = Schedule()
            schedule.event_type = self.category.get(category, '')
            schedule.title = event.find('a').string
            schedule.members = detail["members"]
            schedule.start_time = detail["start_time"]
            schedule_list.append(schedule)

        return schedule_list


if __name__ == '__main__':
    result = Ske("2018/11/05").get_schedule()
    print(result)
    print(f"total: {len(result)} events")