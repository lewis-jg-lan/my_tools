#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import os
import time
import sys
import mysql.connector
import csv

'''
脚本说明:
     1. 爬取天气信息
     2. 处理爬取信息
     3. 设定时间预报
     4. 存储天气信息
     5. 提取存储信息
'''

unit = '℃'
weather_url = 'http://www.weather.com.cn/weather1d/101020100.shtml#search'
tmp_file_path = os.path.dirname(sys.argv[0]) + '/tmp.csv'

# MySQL Info
IP = '127.0.0.1'
USER = 'root'
PASSWD = '88670211'
DATEBASE = 'ForScript'
TABLE = 'ForWeather'


def connect_mysql():
    config = {
        'host': IP,
        'user': USER,
        'password': PASSWD,
        'port': 3306,
        'database': DATEBASE,
        'charset': 'utf8'
    }
    try:
        cnn = mysql.connector.connect(**config)
        return cnn
    except mysql.connector.Error as a:
        print ('connect fails!{}'.format(a))


def insert_date(a, b, c, d, e, f):
    cnn = connect_mysql()
    cursor = cnn.cursor()

    try:
        # Step 1
        # sql_insert1 = "insert into ForWeather (Year_mouth, date_time, weather, temperature, wind_x, wind_d) values (1, 2, 3, 3, 4, 5)" # % (time_get, date_time, weather, temperature, wind_x, wind_d)
        # cursor.execute(sql_insert1)

        # Step 2
        sql_insert2 = "insert into ForWeather (Year_mouth, date_time, weather, temperature, wind_x, wind_d) values (%s, %s, %s, %s, %s, %s)"
        data = (a, b, c, d, e, f)
        cursor.execute(sql_insert2, data)

        # Step 3
        # sql_insert3 = "insert into ForWeather (Year_mouth, date_time, weather, temperature, wind_x, wind_d) values (%(time_get)s, %(date_time)s, %(weather)s, %(temperature)s, %(wind_x)s, %(wind_d)s)"
        # data = {'time_get': a, 'date_time': b, 'weather': c, 'temperature': d, 'wind_x': e, 'wind_d': f}
        # cursor.execute(sql_insert3, data)

        print "\t \t 数据加载成功."
    except mysql.connector.Error as e:
        print "\t \t 数据加载失败，请查看原因."
        print('insert datas error!{}'.format(e))

    finally:
        cursor.close()
        cnn.close()


def get_weather(url):
    '''
    :param url: 提供网络连接
    :return:    反回爬取到的信息
    '''

    req = urllib2.Request(url)

    for i in range(6):

        if i == 5:
            print "-> 网页爬取失败,请检查网络连接."
            os._exit(1)

        try:
            response = urllib2.urlopen(req, timeout=30).read()

        except:
            continue

        if re.findall(r'<script>\s*?var hour3data={(.*?)}\s*?</script>', response):
            more_info = re.findall(r'<script>\s*?var hour3data={(.*?)}\s*?</script>', response)
            break
    return more_info


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


def process_info(url):
    try:
        more_info = get_weather(url)

        # 多信息提取
        for i in more_info:
            for j in str(i).split('\"'):
                if "日" in j:
                    list_info = str(j).split(',')
                    if len(list_info) == 7:
                        time_get = time.strftime("%Y-%m-%d")
                        date_time = list_info[0]
                        weather = list_info[2]
                        temperature = list_info[3]
                        wind_x = list_info[4]
                        wind_d = list_info[5]

                        result = str(time_get) + ',' + str(date_time).split('日')[0] + ',' + str(date_time).split('日')[1].split('时')[0]\
                                 + ',' + str(weather) + ',' + str(temperature) + ',' + str(wind_x) + ',' + str(wind_d)

                        w = 0
                        if not os.path.isfile(tmp_file_path):
                            w_r = "Date" + ',' + 'Day' + ',' + 'Hour' + ',' + 'Weather' + ',' + 'temperature' + ',' + 'wind_x' + ',' + 'wind_d'
                            writefile(str(w_r), tmp_file_path)

                        with open(tmp_file_path) as b_j:
                            for line in b_j:
                                if result in line:
                                    w = 1
                        if w == 0:
                            writefile(result, tmp_file_path)

    except:
        pass


def current_hour():
    hour = time.strftime("%H")
    minute = time.strftime("%m")
    second = time.strftime("%S")

    return hour, minute, second


def speak_on_time(get_time,get_weather,get_temperature,get_wind,get_furture):
    # 报时
    os.system('say 现在时间：%s' % get_time)
    os.system('say 天气情况：%s' % get_weather)
    os.system('say 当前温度：%s' % get_temperature)
    os.system('say 风力情况：%s' % get_wind)
    os.system('say 未来几小时天气状况：%s' % get_furture)

def read_csv_tmp(file):
    try:
        csv_read = open(file,'r')
        reader = csv.DictReader(csv_read)
        print reader.fieldnames
        for i in reader:
            print i['Date'],i['Day'],i['Hour'],i['Weather'],i['temperature'],i['wind_x'],i['wind_d']

    except:
        pass


if __name__ == '__main__':
    #process_info(weather_url)
    #hour, minute, second = current_hour()
    #print hour, minute, second
    #read_csv_tmp(tmp_file_path)
    speak_on_time(1,2,3,4,5)
