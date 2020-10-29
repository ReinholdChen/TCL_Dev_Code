import requests
import simplejson
import copy
import datetime
import time


# 展厅账号登录
def user_login():
    url = "https://io.zx.tcljd.com/v1/auth/user_login"
    headers = {'Content-Type': 'application/json'}
    global accessToken, userId
    data = {
        "loginType": "0",
        "sysInfo": {
            "osVersion": "android",
            "sysVersion": "5.1",
            "appVersion": "3000033",
            "deviceType": "Panasonic P50",
            "did": "00000000-51a9-695e-ffff-ffffecaa93bf"
        },
        "lang": "zh-cn",
        "account": "18126318454",
        "appId": "wx6e1af3fa84fbe523",
        "appSecret": "2024162b231b92a838eea82c9aa7f832",
        "passwordSHA1": "9bc34549d565d9505b287de0cd20ac77be1d3f2c",
        "passwordMD5": "16d7a4fca7442dda3ad93c9a726597e4"
    }
    json_data = simplejson.dumps(copy.deepcopy(data))
    r = requests.post(url, headers=headers, data=json_data)
    j = r.json()
    accessToken = j['data']['accessToken']
    return accessToken


# 展厅账号
headers = {'Content-Type': 'application/json', 'accessToken': user_login()}
masterId = "1103654"


def cur_date():
    cur_time_date = datetime.datetime.now().strftime('[%Y-%m-%d]')
    return cur_time_date


def cur_hour():
    cur_time_date = datetime.datetime.now().strftime('[%Y-%m-%d %H]')
    return cur_time_date


path = r'./test_record/{date}/{hour}.txt'.format(date=cur_date(), hour=cur_hour())

device_name = ["空气净化器", "客厅窗帘", "主卧窗帘", "书房窗帘", "电视插座", "客厅空调", "主卧空调", "书房空调",
               "客厅开关面板二", "客厅开关面板三", "玄关开关面板", "厨房开关面板", "主卧开关面板", "书房开关面板", "书房开关面板二"]
time_list = []

sence = {
    "回家模式": "5dba743ee4b09b4e14be1082",
    "观影模式": "5dba7758e4b09b4e14be1084",
    "晚餐模式": "5dba7859e4b09b4e14be1085",
    "睡眠模式": "5dba7911e4b09b4e14be1086",
    "起床模式": "5dba79d4e4b09b4e14be1087",
    "离家模式": "5e018953e4b0bb8e5cab1c1f",
}

device_status = {
    "空气净化器": {"deviceId": "1103364"},
    "客厅窗帘": {"deviceId": "1095558"},
    "主卧窗帘": {"deviceId": "1095569"},
    "书房窗帘": {"deviceId": "1095563"},
    "电视插座": {"deviceId": "2910130"},
    "客厅空调": {"deviceId": "1103766"},
    "主卧空调": {"deviceId": "1103678"},
    "书房空调": {"deviceId": "1103677"},
    "客厅开关面板二": {"deviceId": "2893520"},
    "客厅开关面板三": {"deviceId": "2894864"},
    "玄关开关面板": {"deviceId": "2894851"},
    "厨房开关面板": {"deviceId": "2894846"},
    "主卧开关面板": {"deviceId": "3649000"},
    "书房开关面板": {"deviceId": "3729288"},
    "书房开关面板二": {"deviceId": "3729317"}
}

off_model = ["观影模式", "睡眠模式", "离家模式"]
open_model = ["回家模式", "晚餐模式", "起床模式"]


# 获取系统当前时间
def cur_time():
    cur_time_date = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
    return cur_time_date


# 将字符串转为时间戳
def str_into_timstamp(str):
    timeArray = time.strptime(str, "[%Y-%m-%d %H:%M:%S.%f]")
    timeStamp = time.mktime(timeArray)
    return timeStamp


# 向txt文件写入内容
def write_text(path_txt, text):
    with open(path_txt, "a+")as text_file:
        text_file.writelines(text)


# 从列表中移除元素
def remove_value(list, value):
    try:
        list.remove(value)
    except:
        pass


# 执行场景
def execute_scene(sid):
    url = "https://io.zx.tcljd.com/v1/scene/execute"
    json_data = simplejson.dumps(copy.deepcopy({"sid": sid, "masterId": masterId}))
    r = requests.post(url, headers=headers, data=json_data)
    j = r.json()
    return j


# 获取设备属性状态
def status(deviceid):
    url = "https://io.zx.tcljd.com/v1/thing/status"
    json_data = simplejson.dumps(copy.deepcopy({"deviceId": deviceid}))
    r = requests.post(url, headers=headers, data=json_data)
    j = r.json()
    return j['data']['status']


# 计算时间差
def get_dur_time(start, end):
    return (end - start).seconds * 1000 + (end - start).microseconds / 1000


# 查看设备状态是否响应
def watch_status(model, device, status, start_time):
    if device == "空气净化器":
        if model == "回家模式":
            if status["clSwitch"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model == "离家模式":
            if status["clSwitch"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        else:
            remove_value(device_name, device)
    if "空调" in device:
        if model == "回家模式":
            if status["turnOn"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model == "离家模式":
            if status["turnOn"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        else:
            remove_value(device_name, device)
    if device == "电视插座":
        if model == "回家模式":
            if status["turnOn"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model == "离家模式":
            if status["turnOn"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        else:
            remove_value(device_name, device)
    if device == "书房开关面板":
        if model in off_model:
            if status["line1"] == "0" and status["line2"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model in open_model:
            if status["line1"] == "1" and status["line2"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
    if device == "客厅开关面板三":
        if model in ["离家模式"]:
            if status["line1"] == "0" and status["line2"] == "0" and status["line3"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model in ["回家模式", "观影模式", "起床模式"]:
            if status["line1"] == "1" and status["line2"] == "1" and status["line3"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        else:
            remove_value(device_name, device)
    if "开关" in device and device != "书房开关面板" and device != "客厅开关面板三":
        if model in off_model:
            if status["line1"] == "0" and status["line2"] == "0" and status["line3"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model in open_model:
            if status["line1"] == "1" and status["line2"] == "1" and status["line3"] == "1":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                time_list.append(get_dur_time(start_time, end_time))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
    if "窗帘" in device:
        if model in off_model:
            if status["cwCurrentPos"] == "0":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)
        if model in open_model:
            if status["cwCurrentPos"] == "10":
                end_time = datetime.datetime.now()
                write_text(path, cur_time() + "{}响应成功,".format(device) + "响应时间：{}ms\n".format(
                    get_dur_time(start_time, end_time)))
                print(cur_time() + "{}响应成功,".format(device))
                remove_value(device_name, device)


def main():
    for each_sence in sence:
        # 第一步 执行场景
        execute_scene(sence[each_sence])
        start_time = datetime.datetime.now()
        write_text(path, cur_time() + "{}开始执行\n".format(each_sence))
        print(cur_time() + "{}开始执行\n".format(each_sence))
        # 第二步 监测各设备响应时间
        i = 0
        while len(device_name) != 0:
            print(device_name)
            for each_device in device_name:
                status_data = status(device_status[each_device]["deviceId"])
                print(status_data)
                watch_status(each_sence, each_device, status_data, start_time)
            i += 1
            if i > 30:
                for each_device in device_name:
                    write_text(path, "{}设备响应超时\n".format(each_device))
                write_text(path, "{}执行出现异常\n".format(each_sence))
                device_name.clear()
                break
            time.sleep(1)
        total = 0
        for ele in range(0, len(time_list)):
            total = total + time_list[ele]
        print(time_list)
        print(total)
        print(total / len(time_list))
        write_text(path, "设备平均响应时间：{}\n".format(total / len(time_list)))
        time_list.clear()
        for each_key in device_status:
            device_name.append(each_key)
        time.sleep(5)


if __name__ == '__main__':
    main()
