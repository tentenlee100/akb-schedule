"""
STU48 schedule and news.

ref:
  * http://www.stu48.com/schedule/?range=future_event_end_time&sort=asc
  * http://www.stu48.com/schedule/detail/2768
"""
from datetime import datetime

import requests
from pyquery import PyQuery as pq

try:
    from schedule.dataType.Schedule import Schedule
except ImportError:  # for test
    from dataType.Schedule import Schedule


class Stu(object):
    query_date = datetime.today().strftime("%Y/%m/%d")

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
        html_block = pq(html)
        root = html_block(".newsBlock > li")

        event_list = []
        for event in root.items():
            result = pq(event.html())

            qdate = "{:0>2}.{:0>2}".format(self.today.month, self.today.day)
            # match today (ex. "10.29")
            if self.is_get_all_event or (qdate == result("dt").text()):
                event_list.append({
                    "event_type": result(".newsCateIco").text(),
                    "title": result(".eventTit").text(),
                    "detail_url": result("a").attr("href"),
                })
            else:
                continue

        return event_list

    def _parse_event_detail(self, event, html) -> Schedule:
        """Parse HTML string to get detail information

        Args:
            event: (dict) event
            html: (string)

        Returns: Schedule object
        """

        html_block = pq(html)
        root = html_block(".detailTxt")
        raw_data = root("p").text()

        # parse member string
        member = ""
        try:
            parse_txt = raw_data.split("掲載メンバー")
            if len(parse_txt) > 1:
                member_data = parse_txt[1].split()[0]
                member = member_data.split("・")
            else:
                parse_txt = raw_data.split("出演メンバー")
                if len(parse_txt) > 1:
                    member_data = parse_txt[1].split()[0]
                    member = member_data.split("・")

        except IndexError:
            pass
        # -member

        # parse time string
        start_time = ""
        end_time = ""
        try:
            if event["event_type"] == "イベント":
                start_time = raw_data.split("時間")[1].split()[0]
                text = start_time.split("～")
                if len(text) > 1:
                    start_time = text[0]
                    end_time = text[1]

            elif event["event_type"] == "誕生日":
                pass
            elif event["event_type"] == "メディア":
                start_time = raw_data.split("日時")[1].split()[0]
            elif event["event_type"] == "公演":
                text = raw_data.split("開場 / 開演")[1].split("/")
                start_time = text[1]
        except IndexError:
            pass

        s = Schedule()
        s.event_type = event["event_type"]
        s.title = event["title"]
        s.members = member
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
