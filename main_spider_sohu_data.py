#http://q.stock.sohu.com/hisHq?code=cn_601390&start=20171016&end=20171020
#coding=utf-8


import MySQLdb
import traceback
import codecs
import os
import urllib,urllib2
import json
import utils




def write2db(data):
  print(data)
  conn,cur = utils.reconnect_mysql()
  if data['status'] == 0:
    for hq in data['hq']:
      sql = "insert into dayinfo (name, day, open, close, change_price, change_ratio, low, high, unknow1, unknow2, unknow3) values ('" + data['code'] + \
            "', '"+ hq[0] + "', "+ hq[1] + ", " + hq[2] + ", " + hq[3] + ", " + hq[4][:-1] + ", " +  hq[5] + ", " + hq[6] + ", " + hq[7] + ", " +hq[8] + ", " +hq[9][:-1] + ")"
      try:
        cur.execute(sql)
      except :
        print("error %s" % sql)

  conn.commit()
  cur.close()
  conn.close()

def main():
  start="20160101" 
  end="20171101"
  code_list = utils.read_stock_code()
  for code in code_list:
    result = utils.get_sohu_stock_data(code, start, end)
    if result != "":
      write2db(result)

      
if __name__=="__main__":
  main()
