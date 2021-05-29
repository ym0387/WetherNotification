# coding:utf-8

# URL指定しデータ取得
import requests

# メール作成
from email.mime.text import MIMEText
from email.utils import formatdate

# Googleアカウントログインとメール送信
import smtplib

# get_weather関数での正規表現用(天気のサーチ)
import re

# 指定した時間に処理を開始する用
import time
import schedule

# メッセージ要素
BODY = '本日は雨または雪の予報です。傘を忘れずに持っていきましょう。'
SUBJECT = '本日は雨または雪の予報です。'
FROM_ADDRESS = '<差出人アドレス>'
TO_ADDRESS = '<宛先アドレス>'

# ログイン用
log_addr = '<ログインアドレス>'
log_pass = '<ログインパスワード>'


# 送信用メッセージを作成する関数
def create_massage(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


# 今日の天気を取得し、雨の場合はメッセージを送信
def get_weather():
    # ライブドアの天気予報結果のURL
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=130010'
    rg = requests.get(url).json() # Json形式で取得

    # 今日の天気を取得
    for weather in rg[ 'forecasts']:
        date = weather['date']
        weather_date = weather['dateLabel']
        weather_forecasts = weather['telop']
        if weather_date == '今日':

            # 今日の天気が雨の場合、メッセージをgmailに送付
            if re.search('雨', weather_forecasts):

                # create_massageで作成したメッセージを送信する関数
                def send_massage(from_addr, to_addr, msg):
                    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpobj.ehlo()
                    smtpobj.starttls()
                    smtpobj.ehlo()
                    smtpobj.login(log_addr, log_pass)
                    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
                    smtpobj.close()

                from_addr = FROM_ADDRESS
                to_addr = TO_ADDRESS
                body = BODY

                MSG = create_massage(FROM_ADDRESS, TO_ADDRESS, SUBJECT, BODY)

                send_massage(FROM_ADDRESS, TO_ADDRESS, MSG)


if __name__ == '__main__':
    get_weather()

# 毎朝6時になったら処理を起動
schedule.every().day.at("06:00").do(get_weather)
while True:
    schedule.run_pending()
    time.sleep(60)
