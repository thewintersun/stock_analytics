#coding=utf-8
import MySQLdb
import traceback
import codecs
import os
import urllib,urllib2
import json
import utils



def read_one_stock_data(code, start_day, end_day):
  conn,cur = utils.reconnect_mysql()
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
  d1,d2 = get_one_stock_close_price_avg("cn_600000", "2017-10-20", "2017-10-31")
  print(d1, d2)