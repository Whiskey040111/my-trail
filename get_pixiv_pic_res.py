import requests
from bs4 import BeautifulSoup
import json
import random
import time
import re
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.pixiv.net/',
    'Cookie': 'first_visit_datetime_pc=2024-02-24%2019%3A11%3A18; p_ab_id=5; p_ab_id_2=9; p_ab_d_id=510087837; yuid_b=FyVkBQU; _gcl_au=1.1.1464789798.1708769555; _gid=GA1.2.1167024928.1711031126; device_token=2d91068510bd1a56cb8a2b903ccf9940; privacy_policy_agreement=6; privacy_policy_notification=0; a_type=0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _im_vid=01HSJ2FT167499ZCTKN9891THZ; c_type=20; b_type=2; login_ever=yes; cc1=2024-03-23%2015%3A36%3A42; PHPSESSID=104520633_jZ6fYkkvFnfoGC7LuSWwyCOeVGewIWVm; _ga_MZ1NL4PHH0=GS1.1.1711175811.5.1.1711175845.0.0.0; cf_clearance=e09xK4R6S1MkTWusAcX0Kr7LrP53W4pisV7B7mW3Jrk-1711181936-1.0.1.1-Eo8dtN3RqWh7LZA3Ob5F22jBFM48Sdt4hjhZX0k5DuFOhB3HfL180UkYSuAuiSKiCGXYDw7abeKw3wetXgKo9w; _im_uid.3929=b.3adf98f84f2d78d4; _ga=GA1.2.215807379.1708769480; __cf_bm=3mYffrT4v2qMuLsQFvNXucH36McyH2jTr2EQRwQWSxs-1711183117-1.0.1.1-9KURKYJMi8GzLyFLF6_8OW0HtybujagBBT3CdtsN8gRN9qxHfSEzluAhUCizYAoJkETqQTOpHFVgG7G5QpFeTxGjlbPOHOQkQRRlLSohvJ8; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1711175806.7.1.1711183193.0.0.0'
}

def get_my_followed_user_id(offset=0, limit=24, header=headers):
    """获取关注列表中各个作者的id"""
    while True:
        url = f'https://www.pixiv.net/ajax/user/51673615/following?offset={offset}&limit={limit}&rest=show&tag=&acceptingRequests=0&lang=zh&version=8995b5449b5fa101b4bef0a0f262713d59994b15'
        resp = requests.get(url=url, headers=headers)
        text = resp.content.decode(resp.apparent_encoding)
        print(type(text))
        json_resp = json.loads(text)
        print(json_resp)
        print(type(json_resp))
        usr_lst = json_resp['body']['users']
        print(usr_lst)
        print(type(usr_lst))
        for usr_info in usr_lst:
            with open('usr_Id.txt', 'a+', encoding='utf8') as file:
                file.write(f'userId:{usr_info["userId"]} userName:{usr_info["userName"]} \n')
        time.sleep(random.randint(0, 10)/10)
        offset += 24
        if offset == 864:
            break



# 14 15 26 28 109 112 140 230 269 275 305 312 316
def get_illus(start = 160, end = 160):
    with open('usr_Id.txt', 'r', encoding='utf8') as file:
        now_line = 1
        if start != 1:
            while now_line < start:
                file.readline()
                now_line += 1
        usr_Id_pattern = re.compile(f'userId:(\d+)')
        usr_name_pattern = re.compile(f'userName:(.*)')
        usr_Id_line = file.readline()
        while usr_Id_line:
            if now_line <= end:
                pass
            else:
                exit(f'已经下载{end - start}个用户的插图作品',f'started line:{start}')
            usr_name = re.search(usr_name_pattern, usr_Id_line).group(1).strip()
            print(usr_name)
            print(type(usr_name))
            usr_Id = re.search(usr_Id_pattern, usr_Id_line).group(1)
            user_path = f'./pic_resource/{usr_name}'
            if os.path.exists(user_path):
                pass
            else:
                os.mkdir(user_path)
            user_illust_path = f'{user_path}/illust'
            if os.path.exists(user_illust_path):
                pass
            else:
                os.mkdir(user_illust_path)
            url = f'https://www.pixiv.net/ajax/user/{usr_Id}/profile/all?lang=zh&version=8995b5449b5fa101b4bef0a0f262713d59994b15'
            individual_illust_page_resp = requests.get(url=url, headers=headers)
            decoded_resp = individual_illust_page_resp.content.decode(individual_illust_page_resp.apparent_encoding)
            print(individual_illust_page_resp.status_code)
            print(decoded_resp)
            json_resp = json.loads(decoded_resp)
            print(type(json_resp))
            print(json_resp)
            illusts_dict = json_resp['body']['illusts']
            for key in illusts_dict.keys():
                int_key = int(key)
                individual_illust_url = f'https://www.pixiv.net/ajax/illust/{int_key}/pages?lang=zh&version=8995b5449b5fa101b4bef0a0f262713d59994b15'
                individual_illust_resp = requests.get(url=individual_illust_url, headers=headers)
                decoded_individual_illust_resp = individual_illust_resp.content.decode(
                    individual_illust_resp.apparent_encoding)
                json_individual_illust_resp = json.loads(decoded_individual_illust_resp)
                illust_url_msg_list = json_individual_illust_resp['body']
                for pic_msg in illust_url_msg_list:
                    orignal_pic_url = pic_msg['urls']['original']
                    pic_code_pattern = re.compile(f'.*/(\d+_p.*?)\..*')
                    pic_format_pattern = re.compile(f'_p.*?\.(.*)')
                    try:
                        pic_code = re.search(pic_code_pattern, orignal_pic_url).group(1)
                    except:
                        continue
                    print(orignal_pic_url)
                    print(type(orignal_pic_url))
                    binary_illust_resp = requests.get(url=orignal_pic_url, headers=headers, timeout=60).content
                    pic_path = f'{user_illust_path}/{pic_code}'
                    pic_format = re.search(pic_format_pattern, orignal_pic_url).group(1)
                    if pic_format == 'jpg':
                        if os.path.exists(f'{pic_path}.jpg'):
                            pass
                        else:
                            with open(f'{pic_path}.jpg', 'wb') as pic_file:
                                pic_file.write(binary_illust_resp)
                    elif pic_format == 'png':
                        if os.path.exists(f'{pic_path}.png'):
                            pass
                        else:
                            with open(f'{pic_path}.png', 'wb') as pic_file:
                                pic_file.write(binary_illust_resp)
                    elif pic_format == 'jepg':
                        if os.path.exists(f'{pic_path}.jpeg'):
                            pass
                        else:
                            with open(f'{pic_path}.jepg', 'wb') as pic_file:
                                pic_file.write(binary_illust_resp)
                    elif pic_format == 'gif':
                        if os.path.exists(f'{pic_path}.gif'):
                            pass
                        else:
                            with open(f'{pic_path}.gif', 'wb') as pic_file:
                                pic_file.write(binary_illust_resp)
                    elif pic_format == 'mp4':
                        if os.path.exists(f'{pic_path}.mp4'):
                            pass
                        else:
                            with open(f'{pic_path}.mp4', 'wb') as pic_file:
                                pic_file.write(binary_illust_resp)
                    else:
                        with open('error.txt', 'a+', encoding='utf8') as err0r_file:
                            file.write(f'picture formate error:{usr_name}-{pic_code} \n')
                    time.sleep(random.randint(0, 5)/10)
            usr_Id_line = file.readline()
            now_line += 1


get_illus(317, 400) # 记得重新下载164

