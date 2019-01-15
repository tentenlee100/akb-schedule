import requests
from bs4 import BeautifulSoup
from datetime import datetime


class GetTheater(object):
    AKB_IMG_NAME = 'cat_logo_akb48'
    SKE_IMG_NAME = 'cat_logo_ske48'
    NMB_IMG_NAME = 'cat_logo_nme48'
    HKT_IMG_NAME = 'cat_logo_hkt48'
    NGT_IMG_NAME = 'cat_logo_ngt48'

    def __init__(self):
        pass

    def _get_theater_info(self, element: BeautifulSoup) -> dict:
        return_dic = {
            'title': '休館日',
            'members': ''
        }
        a_tag = element.find('a')
        if a_tag is None:
            return return_dic

        detail_url = a_tag['href']
        title = a_tag.get_text().replace('\t', '').replace('\xa0', '').replace('\u3000', '').replace('\r', '').replace(
            '\n', '').replace('�U', 'Ⅱ').replace('�V', 'Ⅲ').replace('�W', 'Ⅳ')
        return_dic['title'] = title.split('開演:')[1] if title.split('開演:').__len__() > 1 else title
        return_dic['members'] = self._get_members(detail_url)
        return return_dic

    @staticmethod
    def _get_members(url: str) -> str:
        return_str = ''

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')
        detail_cont_box_list = s.find_all('div', 'detailContBox')

        for detail_cont_box in detail_cont_box_list:
            is_memeber_element = False
            for (index, child) in enumerate(detail_cont_box.find_all()):
                if index == 0 and 'メンバー' in child.get_text():
                    is_memeber_element = True
                    continue
                if is_memeber_element:
                    return_str = child.find().get_text().replace('\r\n', '\r\n\r\n').replace('※', '*')
                    is_memeber_element = False

        return return_str

    def get_schedule(self, query_date) -> dict:
        _query_date = datetime.strptime(query_date, "%Y/%m/%d")
        _query_date_string = _query_date.strftime("%Y-%m-%d")

        r = requests.get('https://ticket.akb48-group.com/home/event_live_list_dairy.php',
                         params={'date': _query_date_string})

        s = BeautifulSoup(r.text, 'html.parser')
        info_list = s.find('ul', 'infoList').find_all('li')

        # {
        #     'title': '休館日',
        #     'members': ''
        # }
        return_dic = {
            'AKB48': [],
            'SKE48': [],
            'NMB48': [],
            'HKT48': [],
            'NGT48': [],
        }

        for li in info_list:
            img_url = li.find('div', 'thumb').find('img')['src']
            if not img_url:
                continue
            if self.AKB_IMG_NAME in img_url:
                return_dic['AKB48'].append(self._get_theater_info(li))
            elif self.SKE_IMG_NAME in img_url:
                return_dic['SKE48'].append(self._get_theater_info(li))
            elif self.NMB_IMG_NAME in img_url:
                return_dic['NMB48'].append(self._get_theater_info(li))
            elif self.HKT_IMG_NAME in img_url:
                return_dic['HKT48'].append(self._get_theater_info(li))
            elif self.NGT_IMG_NAME in img_url:
                return_dic['NGT48'].append(self._get_theater_info(li))

        for key in return_dic.keys():
            if return_dic[key].__len__() == 0:
                return_dic[key].append({'title': '休館日', 'members': ''})

        return return_dic


if __name__ == '__main__':
    query_date_str = datetime.today().strftime("%Y/%m/%d")
    # query_date_str = '2019/01/13'
    members = GetTheater().get_schedule(query_date_str)
    print(members)
