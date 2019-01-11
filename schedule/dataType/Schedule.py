import json


class Schedule(object):
    event_type = ""  # 類別  活動 or 電視 等等 可用日文
    title = ""  # 行事曆標題
    start_time = ""  # 開始時間HH:mm (日本時間)  24小時製  EX: 10:00
    end_time = ""  # 結束時間 HH:mm (日本時間)   24小時製  若沒資料回寫入空白字串 EX: 10:00
    members = []  # 參加活動的成員，若沒有可不塞值
    description = "" # NMB行事曆描述
    location = "" # NMB行事曆地點

    def __repr__(self):
        return "\n<Schedule type:%s title:%s start_time:%s end_time:%s members:%s description:%s location:%s>" % (
        self.event_type, self.title, self.start_time, self.end_time, str(self.members), self.description, self.location)

    def __str__(self):
        dic = dict(type=self.event_type,
                   title=self.title,
                   start_time=self.start_time,
                   end_time=self.end_time,
                   members=self.members,
                   description=self.description,
                   location=self.location
                   )
        string = json.dump(dic, ensure_ascii=False)
        return string
