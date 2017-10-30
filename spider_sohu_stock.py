#http://q.stock.sohu.com/hisHq?code=cn_601390&start=20171016&end=20171020
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


def getdata(code, start, end):
  url='http://q.stock.sohu.com/hisHq'
  textmod={'code': code,'start': start, 'end': end}
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

def write2db(data):
  print(data)
  conn,cur = reconnect_mysql()
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
  start="20171023" 
  end="20171023"
  for c in range(999):
    code = "cn_00" + "%04d"%c
    print(code)
    result = getdata(code, start, end)
    if result != "":
      write2db(result)

    code = "cn_30" + "%04d"%c
    print(code)
    result = getdata(code, start, end)
    if result != "":
      write2db(result)

    code = "cn_60" + "%04d"%c
    print(code)
    result = getdata(code, start, end)
    if result != "":
      write2db(result)



if __name__=="__main__":
  main()
