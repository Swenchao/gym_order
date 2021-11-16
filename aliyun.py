# -*- coding: utf-8 -*-
import time

import requests
import datetime


# 健身房预约时间
class GymTime:
    def __init__(self, gym_dict):
        for key in gym_dict:
            setattr(self, key, gym_dict[key])


# server酱 key（不填无所谓，只不过无法收到通知）
server_key = ""

# 用户信息（需要替换自己的）
user_info = {
    # 姓名
    'userName': '',
    # 手机号
    'userPhone': '',
    # 身份证号
    'userIdentityNo': '',
}

# 需要预约的时间（12 14 17）
gym_time = 17

# 微信 openId（需要替换自己的）
openId = ''

# 请求
s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)


# 判断是否可预约
def is_gym_order(date, startTime, endTime):
    # 拿到预约数据
    url = "http://wechartdemo.zckx.net/API/TicketHandler.ashx?dataType=json&date=" + date + "&projectNo=1000000637&method=GetStrategyList";
    data = s.get(url).json().get("list")

    # 遍历判断
    for item in data:
        gym_item = GymTime(item)
        if startTime == gym_item.sTime and endTime == gym_item.eTime:
            if gym_item.isCanReserve == 1 and gym_item.restCount > 0:
                return True
            else:
                return False

    return False


def gym_order(date, time_detail):
    url = "http://wechartdemo.zckx.net/Ticket/SaveOrder?"

    other_info = {
        'styleNo': "1000001069",
        'styleGroupNo': "1000000379",
        'styleName': "体育馆健身房",
        'price': "0.00",
        'discountPrice': "0.00",
        'ticketNum': 1,
        'solutionNo': "1000000632",
        'projectNo': "1000000637"
    }

    data = {
        'userInfoList': [user_info],
        'timeList': [time_detail],
        'styleInfoList': [other_info],
        'userDate': date,
        'totalprice': 0,
        'openId': openId,
        'sellerNo': 'weixin'
    }
    url = url + 'dataType=json&orderJson=' + str(data)
    print(url)
    r = s.post(url)
    # print(r.json())

    return r.json()


# 查看是否预约成功
def is_success_order(date):
    url = "https://wechartdemo.zckx.net/Ticket/MyOrder?openId=" + openId
    gym_html = s.get(url).text
    new_date = date.split("-")[0] + '年' + date.split("-")[1] + '月' + date.split("-")[2] + '日'
    if new_date in gym_html:
        return True
    return False


# 微信通知
def send_message(key, title, body):
    if server_key != "":
        msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
        requests.get(msg_url)


def handler(event, context):
    # 预约时间
    order_time = {
        "12": {"minDate": "12:00", "maxDate": "14:00", "strategy": "1000000175"},
        "14": {"minDate": "14:30", "maxDate": "16:30", "strategy": "1000000176"},
        "17": {"minDate": "17:00", "maxDate": "19:00", "strategy": "1000000174"}
    }
    date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    time_detail = order_time.get(str(gym_time))

    # 查看是否还可预约
    flag = is_gym_order(date, time_detail.get("minDate"), time_detail.get("maxDate"))

    if flag:
        r = gym_order(date, time_detail)

        # 发送请求后，挂起10分钟，再请求查看是否成功
        time.sleep(6000)

        is_success = is_success_order(date)
        if is_success:
            send_message(server_key, str(gym_time) + "预约成功", r)
        else:
            send_message(server_key, str(gym_time) + "预约失败", r)
    else:
        send_message(server_key, str(gym_time) + "不可预约", flag)