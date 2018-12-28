import time
import requests
from bs4 import BeautifulSoup
from schedule.dataType.Schedule import *

# 網頁: http://www.hkt48.jp/schedule/


class Hkt(object):
    query_date = ""  # 查詢時間 時間格式 yyyy/MM/dd ex: 2018/08/10
    CATEGORY = {
        '35': '誕生日',
        '85': '握手会',
        '20': '公演',
        '36': 'リリース',
        '21': 'イベント',
        '86': 'コンサート',
        '22': 'メディア',
        '23': 'メンバー',
        '24': 'その他',
    }

    def __init__(self, query_date):
        self.query_date = query_date

    @staticmethod
    def _get_html(url):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        return BeautifulSoup(html, 'html.parser')

    def get_schedule(self) -> [Schedule]:
        query_date = time.strptime(self.query_date, '%Y/%m/%d')
        query_year = time.strftime('%Y', query_date)
        query_month = time.strftime('%m', query_date)
        query_day = int(time.strftime('%d', query_date))

        schedule_list_url = 'http://www.hkt48.jp/schedule/{year}/{month}/'.format(year=query_year, month=query_month)
        schedule_list_html = self._get_html(schedule_list_url)

        schedule_list = []
        event_list = schedule_list_html.select('th[id="day{query_day}"] + td p'.format(query_day=query_day))
        for event in event_list:
            category = event.get('class')[0]
            schedule = Schedule()
            schedule.event_type = self.CATEGORY.get(category, '')
            schedule.title = event.get_text().strip()
            schedule_list.append(schedule)

        return schedule_list

if __name__ == '__main__':
    result = Hkt("2018/12/29").get_schedule()
    print(result)