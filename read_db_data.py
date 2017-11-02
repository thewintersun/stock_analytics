#coding=utf-8
import MySQLdb
import traceback
import codecs
import os
import urllib,urllib2
import json
import utils
import datetime


def good_stock():
  '''
  找出来2个月平稳，最近2天有明显涨幅的股票
  '''
  now = datetime.datetime.now()

  now_str = utils.datetime2str(now)

  before_1day = utils.before_n_day(now, 1)
  before_1day_str = utils.datetime2str(before_1day)

  before_2day = utils.before_n_day(now, 2)
  before_2day_str = utils.datetime2str(before_2day)
  before_62day = utils.before_n_day(now, 62)
  before_62day_str = utils.datetime2str(before_62day)
  print("before 2 day is " + before_2day_str)
  print("before 62 day is " + before_62day_str)

  code_list = utils.read_stock_code()
  for code in code_list:
    avg_price, var_price = utils.get_one_stock_close_price_avg(code, before_62day_str, before_2day_str )
    if avg_price < 25 and var_price < 0.01:
      recent_data = utils.read_one_stock_data(code, before_1day_str, now_str)
      #print(recent_data)
      if len(recent_data) > 1:
        print(len(recent_data))
        if recent_data[0][6] > 1 and recent_data[1][6] > 1:
          print(code)

  


if __name__=="__main__":
  good_stock()
  '''
  now = datetime.datetime.now()
  print(now.strftime('%Y-%m-%d'))
  delta = datetime.timedelta(days=3)
  n_days = now + delta
  print (n_days.strftime('%Y-%m-%d %H:%M:%S')  )

  oneday = datetime.datetime.strptime("2017-10-10", '%Y-%m-%d')
  n_days = oneday + delta
  print (n_days.strftime('%Y-%m-%d %H:%M:%S')  )
  '''
  #d1,d2 = get_one_stock_close_price_avg("cn_600050", "2017-08-20", "2017-10-31")
  #print(d1, d2)