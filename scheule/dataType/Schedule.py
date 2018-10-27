import json


class Schedule(object):
    type = ""  # 類別  活動 or 電視 等等 可用日文
    title = ""  # 行事曆標題
    start_time = ""  # 開始時間HH:mm (日本時間)  24小時製  EX: 10:00
    end_time = ""  # 結束時間 HH:mm (日本時間)   24小時製  若沒資料回寫入空白字串 EX: 10:00
    members = []  # 參加活動的成員，若沒有可不塞值

    def __repr__(self):
        return "<Schedule type:%s title:%s start_time:%s end_time:%s members:%s>" % (
        self.type, self.title, self.start_time, self.end_time, str(self.members))

    def __str__(self):
        dic = dict(type=self.type,
                   title=self.title,
                   start_time=self.start_time,
                   end_time=self.end_time,
                   members=self.members,
                   )
        string = json.dump(dic, ensure_ascii=False)
        return string
