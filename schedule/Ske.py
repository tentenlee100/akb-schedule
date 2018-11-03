import time
import requests
from bs4 import BeautifulSoup
from .dataType.Schedule import *

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
        return members

    def get_schedule(self) -> [Schedule]:
        query_date = time.strptime(self.query_date, '%Y/%m/%d')
        query_year = time.strftime('%Y', query_date)
        query_month = time.strftime('%m', query_date)
        query_day = time.strftime('%d', query_date)
        query_date_key = '{year}_{month}_{day}'.format(year=query_year, month=query_month, day=int(query_day))

        schedule_list_url = 'http://www.ske48.co.jp/schedule/calendar.php?y={year}&m={month}'.format(year=query_year, month=query_month)
        schedule_list_html = self._get_html(schedule_list_url)

        days_in_month = schedule_list_html.select('table[title="SCHEDULE"] > a[name]')
        schedule_data = {}
        for day in days_in_month:
            day_number = day.get('name')
            schedule_in_day = schedule_list_html.select('table[title="SCHEDULE"] > a[name="{day}"] + tr li'.format(day=day_number))
            date = '{year}_{month}_{day}'.format(year=query_year, month=query_month, day=day_number)
            schedule_data[date] = []
            for event in schedule_in_day:
                category = event.get('class')[0]
                event_link = event.find('a').get('href')
                members = self._get_event_detail(event_link, category)
                schedule = Schedule()
                schedule.event_type = self.category.get(category, '')
                schedule.title = event.find('a').string
                schedule.members = members
                schedule_data[date].append(schedule)

        schedule_list = schedule_data.get(query_date_key)
        return schedule_list
