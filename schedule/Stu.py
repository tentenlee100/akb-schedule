"""
STU48 schedule and news.

ref:
  * http://www.stu48.com/schedule/?range=future_event_end_time&sort=asc
  * http://www.stu48.com/schedule/detail/2768
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup

try:
    from schedule.dataType.Schedule import Schedule
except ImportError:  # for test
    from .dataType.Schedule import Schedule


class Stu(object):
    query_date = datetime.today().strftime("%Y/%m/%d")
    mapping_dic = {
        "が": "が",
        "ぎ": "ぎ",
        "ぐ": "ぐ",
        "げ": "げ",
        "ご": "ご",
        "ざ": "ざ",
        "じ": "じ",
        "ず": "ず",
        "ぜ": "ぜ",
        "ぞ": "ぞ",
        "だ": "だ",
        "ぢ": "ぢ",
        "づ": "づ",
        "で": "で",
        "ど": "ど",
        "ば": "ば",
        "び": "び",
        "ぶ": "ぶ",
        "べ": "べ",
        "ぼ": "ぼ",
        "ぱ": "ぱ",
        "ぴ": "ぴ",
        "ぷ": "ぷ",
        "ぺ": "ぺ",
        "ぽ": "ぽ",
# 片 假 名
        "ガ": "ガ",
        "ギ": "ギ",
        "グ": "グ",
        "ゲ": "ゲ",
        "ゴ": "ゴ",
        "ザ": "ザ",
        "ジ": "ジ",
        "ズ": "ズ",
        "ゼ": "ゼ",
        "ゾ": "ゾ",
        "ダ": "ダ",
        "デ": "デ",
        "ド": "ド",
        "バ": "バ",
        "ビ": "ビ",
        "ブ": "ブ",
        "ベ": "ベ",
        "ボ": "ボ",
        "パ": "パ",
        "ピ": "ピ",
        "プ": "プ",
        "ペ": "ペ",
        "ポ": "ポ"
    }

    def __init__(self, query_date="", debug=False):
        """Get query date string to datetime type.

        Args:
            query_date: (string) ex. 2018/08/10
        """
        if query_date:
            self.query_date = query_date

        self.is_get_all_event = False   # only today
        if debug:
            self.is_get_all_event = True

        try:
            self.today = datetime.strptime(self.query_date, "%Y/%m/%d")
        except (TypeError, ValueError):
            print("Please check your input date format (ex. 2018/10/10)")

    def check_title(self, title: str) -> str:
        return_title = title
        if "゙" in return_title or "゚" in return_title:
            for key in self.mapping_dic.keys():
                if key in return_title:
                    return_title = return_title.replace(key, self.mapping_dic[key])
        return return_title

    @staticmethod
    def _parse_start_date(string: str) -> str:
        return_string = ""
        check_start_time_index = string.find(":")
        # 看能不能拿到開始時間
        if check_start_time_index > -1:
            # 查看:前後數否為數字(前1或前2)
            before2 = string[check_start_time_index - 2:check_start_time_index]
            before1 = string[check_start_time_index - 1:check_start_time_index]
            end2 = string[check_start_time_index + 1:check_start_time_index + 3]
            if before2.isdigit() and end2.isdigit():
                return_string = before2 + ":" + end2
            elif before1.isdigit() and end2.isdigit():
                return_string = "0" + before1 + ":" + end2
        return return_string

    def _parse_event(self, html) -> list:
        """Parse HTML string to get basic event list.

        Args:
            html: (string) html page

        Returns:
            event list.
            ex. {
                "event_type": "Good event",
                "title": "Happy Birthday",
                "detail_url": "/schedule/detail/2768"
            }
        """
        html_block = BeautifulSoup(html, 'html.parser')
        root = html_block.find('ul', 'newsBlock')
        li_list = root.find_all('li')

        event_list = []
        for event in li_list:
            event_date = event.find('dl', 'eventListDate').find('dt').get_text()
            query_date = "{:0>2}.{:0>2}".format(self.today.month, self.today.day)
            # match today (ex. "10.29")
            if self.is_get_all_event or (query_date == event_date):
                event_obj = {
                    "event_type": event.find('span', 'newsCateIco').get_text(),
                    "title": event.find('h2', 'eventTit').get_text(),
                    "detail_url": event.find("a")["href"],
                }
                event_list.append(event_obj)
            else:
                continue
        print(event_list)
        return event_list

    def _parse_event_detail(self, event, html) -> Schedule:
        """Parse HTML string to get detail information

        Args:
            event: (dict) event
            html: (string)

        Returns: Schedule object
        """

        html_block = BeautifulSoup(html, 'html.parser')
        root = html_block.find("dd", "detailTxt")
        raw_data = root.get_text()
        print(raw_data)
        # parse member string
        members = []
        start_time = ""
        end_time = ""
        try:
            all_p = root.find_all('p')
            if len(all_p) == 0:
                all_p = root.find_all('div')

            detail_dic = {}

            now_key = ""
            detail_text = ""
            for p in all_p:
                # 是標題
                if '●' == p.get_text()[:1] or '▼' == p.get_text()[:1]:
                    # 先將之前的資訊存入detail_dic
                    if now_key.__len__() != 0:
                        detail_dic[now_key] = detail_text
                        detail_text = ""
                    # 找到新的key
                    now_key = p.get_text().replace("●", '').replace('▼', '')
                    continue
                # 是內文
                else:
                    # 如果這個P沒有資料跳過
                    if p.get_text().__len__() == 0:
                        continue
                    # 如果detail_text先前已經有資料的話先加上一個換行符號
                    if detail_text.__len__() > 0:
                        detail_text += '\n'
                    detail_text += p.get_text()
            # 最後一組時，不會存入detail_dic內，所以要再加入
            if now_key.__len__() != 0 and detail_text.__len__() != 0:
                detail_dic[now_key] = detail_text
            # print(detail_dic)

            # 開始判斷內文
            for key in detail_dic.keys():
                # 找成員
                if 'メンバー' in key or '出演' in key:
                    lines = detail_dic[key].split('\n')
                    for line in lines:
                        find_start = line.find('（')
                        find_end = line.find('）')
                        # 如果成員有用（）包起來的時候從包起來的地方取資料
                        if find_start > -1 and find_end > -1 and line.find('MC :') == -1:
                            split_point = line[find_start + 1:find_end].split("・")
                        else:
                            split_point = line.split("・")
                        if split_point.__len__() > 1:
                            members = split_point
                    # 若判斷後沒有任何成員資料，且此內容只有一行時，將此行資訊直接放入members中，有可能是籠統成員 OR 成員只有一位
                    if members.__len__() == 0 and lines.__len__() == 1:
                        members = [lines[0]]

                # 找開始時間結束時間
                elif "時間" in key or "日時" in key or "開場 / 開演" in key:
                    text = detail_dic[key].split("〜")
                    start_time = self._parse_start_date(text[0])
                    if text.__len__() > 1:
                        end_time = self._parse_start_date(text[1])

        except Exception as e:
            print("caught", repr(e))

        s = Schedule()
        s.event_type = event["event_type"]
        title = event["title"].replace("↗︎", "↗")
        s.title = self.check_title(title)
        s.members = members
        s.start_time = start_time
        s.end_time = end_time
        # print(s.__str__)
        return s

    def get_schedule(self) -> [Schedule]:
        """Get schedule data from website

        Returns:
            A list of schedule object
        """
        url = "http://www.stu48.com"
        headers = {
            "Cache-Control": "no-cache",
        }
        payload = {
            "range": "future_event_end_time",
            "sort": "asc"
        }

        schedule_list = []
        with requests.Session() as s:
            r = s.get(url + "/schedule/", headers=headers, params=payload)
            event_list = []
            if r.status_code == 200:
                event_list = self._parse_event(r.text)
            else:
                print("Connect to STU48 website fail.")

            for event in event_list:
                if event["detail_url"]:
                    dt_r = s.get(url + event["detail_url"], headers=headers)

                    if dt_r.status_code == 200:
                        schedule_list.append(
                            self._parse_event_detail(event, dt_r.text))
                    else:
                        print(f"Connect to {url + event['detail_url']} fail.")
                        continue

        return schedule_list


if __name__ == '__main__':
    result = Stu(debug=True).get_schedule()
    print(result)
