import requests
from bs4 import BeautifulSoup
import datetime


class GetBirthMember(object):
    def __init__(self):
        self.group_dic = {
            'ＡＫＢ４８': "AKB48",
            'ＳＫＥ４８': "SKE48",
            'ＮＭＢ４８': "NMB48",
            'ＨＫＴ４８': "HKT48",
            'ＮＧＴ４８': "NGT48",
            'ＳＴＵ４８': "STU48",
            'ＢＮＫ４８': "BNK48",
            'AKB48 TeamTP': "AKB48 TeamTP",
        }
    def get_birth_member(self, query_date):
        r = requests.get("https://www.ptt.cc/bbs/AKB48/M.1506782468.A.727.html")
        r.encoding = 'utf-8'
        html = r.text
        s = BeautifulSoup(html, 'html.parser')
        html_string = s.get_text()
        start_index = html_string.find("==ＡＫＢ４８==")
        end_index = html_string.find("==待畢業/移籍成員")
        member_string = html_string[start_index:end_index].replace('AB20', 'AB 20').replace('AB19', 'AB 19')
        pre_index = 0
        find_index = member_string.find(query_date)
        year = datetime.datetime.today().strftime("%Y")
        members = []
        while find_index != -1:
            # group = member_string.rfind("\n", pre_index, find_index)
            start_index = member_string.rfind("\n", pre_index, find_index)
            end_index = member_string.find("\n", find_index)
            birth_member = [x for x in member_string[start_index + 1 + 5:end_index].split(' ') if x != '']
            #  要抓到是哪團的
            group_line_end_index = member_string.rfind("=", 0, find_index)
            group_line_start_index = member_string.rfind("\n", 0, group_line_end_index)
            group_line = member_string[group_line_start_index + 1:group_line_end_index]
            group = ''
            find_group = [x for x in group_line.split('=') if x != '']
            if find_group.__len__() > 0:
                group = self.group_dic[find_group[0]]

            # print(group)
            if list(filter(lambda x: x["name"] == birth_member[0] and x["birth"] == birth_member[4],
                           members)).__len__() > 0:
                pass
            else:
                members.append({
                    'name': birth_member[0],
                    'birth': birth_member[4],
                    'age': str(int(year) - int(birth_member[4][:4])),
                    'group': group
                })
            # print(birth_member)
            pre_index = find_index
            find_index = member_string.find(query_date, find_index + 1)
        # print(member_string)
        # print(members)
        return members

if __name__ == '__main__':
    query_date = datetime.datetime.today().strftime("/%m/%d")
    # query_date = '/12/24'
    members = GetBirthMember().get_birth_member(query_date)
    print(members)
