import cv2
from pyzbar.pyzbar import decode
from PIL import Image
from pandas import DataFrame
import time
from functions import check_token 
from classes import Sesame
import os
import setting

# 地点コード
code = setting.POINT_CODE
cmd = 'python3 ' + os.getcwd() +'/back_process.py '+code+' &'
sesame = Sesame( code )
#print ( obj.sesame_id)
# カメラのキャプチャを開始 
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 10)

def check_qr (img):
        global cam
        data = DataFrame(decode(img))
        try:
                data = DataFrame(decode(img))
                qr_data = data["data"][0].decode()
                #ここでtokenチェックする
                if check_token(code , qr_data):
                        #一旦画像取得をやめる
                        cam.release()
                        #cv2.destroyAllWindows()
                        #ここでセサミ関数を打つ
                        if sesame.unlock()==0:
                                print("正常動作")
                                # 非同期にしてるが... ロックは別のプログラムが良いかも...
                                os.system(cmd)
                        else :
                                if sesame.state_check()=="ロックされていません":
                                        sesame.lock()
                        time.sleep(10)
                        cam = cv2.VideoCapture(0)
                        cam.set(cv2.CAP_PROP_FPS, 10)
                else:
                        print("不正利用はダメです！")

        except KeyError:
                pass
        except :
                print(" non read !!")


while True:
        # 画像取得
        x, img = cam.read()
        # ウィンドウに画像を表示
        #cv2.imshow('PUSH_ENTER_KEY', img)
        check_qr(img)
        # Enterキーが押されたら終了する
        if cv2.waitKey(1) == 13: break

cam.release()
cv2.destroyAllWindows()
