import requests

class GetVideo(object):

    def __init__(self):
        pass

    def get_video(self) -> dict:

        r = requests.get('https://docs.google.com/document/export?format=txt&id=1e5IYXWMxCYEEKi4jnuaoy7BntcpDGqka54yrZEJl9FQ&includes_info_params=true'
                         )
        txt = r.text

        start = txt.find('-----')
        txt = txt[start + 5:]

        title_start_text = '┤'
        start_title_index = txt.find(title_start_text)

        return_list = []
        while start_title_index != -1:
            title_end_index = txt.find('\r\n', start_title_index)
            title = txt[start_title_index:title_end_index]
            # 找下一個title
            start_title_index = txt.find(title_start_text, title_end_index)
            # 處理這個title間的連結
            link_txt = txt[title_end_index:start_title_index]
            link_list = [ x.strip().split('\r\n') for x in link_txt.split('\r\n\r\n') if x.strip().__len__() > 0]
            return_list.append({'title': title, 'links':link_list })

        return return_list


if __name__ == '__main__':
    members = GetVideo().get_video()
    print(members)
