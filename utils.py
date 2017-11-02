#coding=utf-8

import pymysql
import traceback
import codecs
import os

import urllib.parse
import urllib.request
import json
import datetime

def reconnect_mysql():
  conn= pymysql.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='root',
        db ='stock',
        charset="utf8",)
  cur = conn.cursor()
  return conn,cur

def get_sohu_stock_data(code, start_day, end_day):
  '''获取sohu的stock数据''' 
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
  headers = { 'User-Agent' : user_agent }
  url='http://q.stock.sohu.com/hisHq'
  param = "code="+code+"&end="+end_day+"&start="+start_day
  url += "?"+param
  req  = urllib.request.Request(url)
  res = urllib.request.urlopen(req)

  res = res.read().decode('utf-8')
  print(res)
  if len(res)< 30:
    return ""
  resj = json.loads(res)
  print(resj)
  if resj[0]['status'] != 0:
    return ""
  return resj[0]

def get_all_stock_code():
  '''获取大概所有的 股票的代码，写入到文件'''
  start="20171024" 
  end="20171024"
  code_list = []
  for c in range(1000):
    code = "cn_000" + "%03d"%c
    print(code)
    result = get_sohu_stock_data(code, start, end)
    if result != "":
      code_list.append(code)
    code = "cn_002" + "%03d"%c
    print(code)
    result = get_sohu_stock_data(code, start, end)
    if result != "":
      code_list.append(code)

    code = "cn_300" + "%03d"%c
    print(code)
    result = get_sohu_stock_data(code, start, end)
    if result != "":
      code_list.append(code)

    code = "cn_600" + "%03d"%c
    print(code)
    result = get_sohu_stock_data(code, start, end)
    if result != "":
      code_list.append(code)

    code = "cn_601" + "%03d"%c
    print(code)
    result = get_sohu_stock_data(code, start, end)
    if result != "":
      code_list.append(code)

  with codecs.open("code.txt", 'w', 'utf-8') as fw:
    for c in code_list:
      fw.write(c + "\n")

def read_stock_code():
  ''' 读取股票code，返回list'''
  result_list = []
  with codecs.open("code.txt", 'r', 'utf-8') as fr:
    for line in fr:
      result_list.append(line.strip())
  return result_list




def str2datetime(date_str):
  ''' 
  将字符串，转换成datetime，
  字符串格式需要是2017-10-10格式类型的
  '''
  oneday = datetime.datetime.strptime("date_str", '%Y-%m-%d')
  return oneday

def before_n_day(date, before_n):
  '''
  某个日期之前的n天，返回datetime类型的
  '''
  before_datetime = datetime.timedelta(days=before_n)
  oneday = date - before_datetime
  return oneday

def after_n_day(date, after_n):
  '''
  某个日期之后的n天，返回datetime类型的
  '''
  after_datetime = datetime.timedelta(days=after_n)
  oneday = date - after_datetime
  return oneday

def datetime2str(date):
  '''
  datetime转换成字符串
  '''
  return date.strftime('%Y-%m-%d')

def read_one_stock_data(code, start_day, end_day):
  '''
  读取一个股票的某个时间段的数据
  '''

  conn,cur = reconnect_mysql()
  '''
  sql = "select Id,name,day,open,close, change_price, change_ratio, low, high, " + \
    "unknow1, unknow2, unknow3 from dayinfo where name='" + code + "' and day>='"+start_day+"' and day<='"+end_day+"' order by day asc"
  '''
  sql = "select * from dayinfo where name='" + code + "' and day>='"+start_day+"' and day<='"+end_day+"' order by day asc"
  try:
    cur.execute(sql)
    result = cur.fetchall()
  except :
    print("error %s" % sql)
    return ""
  return result

def get_one_stock_close_price_avg(code, start_day, end_day):
  '''
  得到某个股票，某个时间段内，收盘价格的均值和方差
  '''
  stock_data_list = read_one_stock_data(code, start_day, end_day)
  all_price = 0 
  for stock_data in stock_data_list:
    close_price = stock_data[4]
    all_price += float(close_price)
  avg_price = all_price/len(stock_data_list)

  # 方差
  squre_sum = 0
  for stock_data in stock_data_list:
    close_price = stock_data[4]
    squre_sum += (close_price - avg_price) * (close_price - avg_price)
  var_price = squre_sum/ len(stock_data_list)
  return avg_price, var_price


if __name__=="__main__":
  get_all_stock_code()