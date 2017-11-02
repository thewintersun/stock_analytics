#coding=utf-8

import MySQLdb
import traceback
import codecs
import os
import urllib,urllib2
import json

def reconnect_mysql():
  conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='stock',
        charset="utf8",)
  cur = conn.cursor()
  return conn,cur

def get_sohu_stock_data(code, start_day, end_day):
  '''获取sohu的stock数据''' 
  url='http://q.stock.sohu.com/hisHq'
  textmod={'code': code,'start': start_day, 'end': end_day}
  textmod = urllib.urlencode(textmod)
  req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
  res = urllib2.urlopen(req)
  res = res.read()
  print(res)
  if len(res)< 30:
    return ""
  resj = json.loads(res)
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

if __name__=="__main__":
  get_all_stock_code()