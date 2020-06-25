import pymysql
from datetime import datetime ,timedelta
import hashlib
import setting

def check_token(code ,input_token): 
  db = pymysql.connect(
      host = setting.HOST ,
      user = setting.USER,
      password = setting.PASS,
      db = setting.DBNAME,
      charset='utf8',
      cursorclass=pymysql.cursors.DictCursor
  )
  #今の時間を取得
  tm = datetime.now()
  tm = tm - timedelta(minutes=tm.minute % 30, seconds=tm.second,microseconds=tm.microsecond)
  s_date = tm.strftime('%Y-%m-%d %H:%M:%S')
  print(s_date)
  cur = db.cursor()
  sql = "select token from "+code+' where s_date="'+s_date+'"'
  cur.execute(sql)
  data = cur.fetchall()
  db.close()
  try: 
        true_token = data[0]["token"]
        return true_token == input_token
  except:
        return False

def sesame_getter(code):
  db = pymysql.connect(
      host = setting.HOST ,
      user = setting.USER,
      password = setting.PASS,
      db = setting.DBNAME,
      charset='utf8',
      cursorclass=pymysql.cursors.DictCursor
  )
    cur = db.cursor()
    sql = "select sesame_id from  sesame  where point_code='"+code+"';"
    cur.execute(sql)
    data = cur.fetchall()
    db.close()
    if len(data)==0:
        return "not found"
    else :
        return data[0]["sesame_id"]



  
