import pymysql
import requests
import json
import time
import setting

class Sesame:
    def __init__(self, code):
        self.code = code
        self.sesame_getter()
        self.head = {"Authorization": setting.Authorization}

    def sesame_getter(self):
        db = pymysql.connect(
            host = setting.HOST,
            user= setting.USER,
            password = setting.PASS,
            db = setting.DBNAME,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = db.cursor()
        sql = "select sesame_id from  sesame  where point_code='"+self.code+"';"
        cur.execute(sql)
        data = cur.fetchall()
        db.close()
        if len(data)==0:
            self.sesame_id = "not found"
        else :
            self.sesame_id = data[0]["sesame_id"]

    def lock(self, check_flag=False):
        url = "https://api.candyhouse.co/public/sesame/" + self.sesame_id

        response = requests.get(url, headers= self.head)

        #now state
        status = response.json()["locked"]
        if status is True :
                return -1 #Error code

        payload_control = {"command":"lock"}
        response = requests.post( url, headers= self.head, data=json.dumps(payload_control))

        #Exception handling
        if check_flag is True:
                time.sleep(15)
                task_id = response.json()["task_id"]
                url = "https://api.candyhouse.co/public/action-result?task_id="+task_id
                response = requests.get(url, headers= self.head)
                if response.json()["successful"]==False :
                        return -2 #Error code Retry!!

        return 0 # OK

    def unlock(self, check_flag=False ):
        url = "https://api.candyhouse.co/public/sesame/" + self.sesame_id

        response = requests.get(url, headers= self.head)

        #now state
        status = response.json()["locked"]
        if status is  False:
                return -1 #Error code

        payload_control = {"command":"unlock"}
        response = requests.post( url, headers= self.head, data=json.dumps(payload_control))


        #Exception handling
        if check_flag is True:
                time.sleep(15)
                task_id = response.json()["task_id"]
                url = "https://api.candyhouse.co/public/sesame/action-result?task_id="+task_id
                response = requests.get(url, headers= self.head)
                if response.json()["successful"]==False :
                        return -2 #Error code Retry!!

        return 0 # OK   

    def state_check(self):
        url = "https://api.candyhouse.co/public/sesame/" + self.sesame_id

        response = requests.get(url, headers= self.head)

        #now state
        status = response.json()["locked"]
        
        if status is  True:
                        return "ロックされています"
                          
        elif status is False :
                        return "ロックされていません"   

    
