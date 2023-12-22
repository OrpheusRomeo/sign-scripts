# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
import logging

def sign(page, topic_list, cookie, loop):
    try:
        n = 0
        payload={}
        for topic_dict in topic_list:
            topic_id = topic_dict['id']
            topic_name = topic_dict['name']
            content1 = topic_dict['content1']
            content2 = topic_dict['content2']
            url = "https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=1&id="+topic_id+"&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=MacIntel&ua=Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/100.0.4896.60%20Safari/537.36&screen=1440*900&__rnd=1663768486494"

            headers = {
                'Cookie': cookie,
                'refer': 'https://weibo.com/p/'+ topic_id +'/super_index'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            #print(response)
            str = response.text
            res_data = json.loads(str)
            message = res_data['msg']
            n = n + 1
            local_time = int(time.time())
            time_struct = time.localtime(local_time)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
            if loop == 1:
                print("{}--{}--{}--{}--{}--{}".format(strTime, page, n, topic_name, message, content2))
            else:
                if n%20==0:
                    print("{}--{}--{}--{}--{}--{}".format(strTime, page, n, topic_name, message, content2))
            time.sleep(1)
    except Exception as e:
        print(e)
        logging.error("Topic [{0}]  Sign Exception: ".format(topic_name))


def get_topics(cookie, start, end, n):
    for page in range(start, end):
        topic_list = []
        topic_keys = []
        url = "https://weibo.com/ajax/profile/topicContent?tabid=231093_-_chaohua&page={}".format(page)
        payload={}
        headers = {
            'Cookie': cookie,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        #print(response.text)
        json_data = json.loads(response.text)
        data = json_data['data']['list']
        for i in data:
            topic_dict = {}
            topic_id = i['oid'].replace("1022:","")
            topic_name = i['title']
            content1 = i['content1']
            content2 = i['content2']
            topic_dict['id'] = topic_id
            topic_dict['name'] = topic_name
            topic_dict['content1'] = content1
            topic_dict['content2'] = content2
            if topic_id not  in topic_keys:
                topic_keys.append(topic_id)
                topic_list.append(topic_dict)
            else:
                print("repeat:{}:{}".format(topic_id, topic_name))

        #print(page, topic_list)
        sign(page, topic_list, cookie, n)
        #time.sleep(25)
    #return topic_list


if __name__ == '__main__':
    args = sys.argv
    #print(args)
    start = int(args[1])
    end = int(args[2])
    loop = int(args[3])
    cookie = args[4]
    for i in range(1,loop):
        print("====第{}次====".format(i))
        get_topics(cookie, start, end, i)
        time.sleep(10)
