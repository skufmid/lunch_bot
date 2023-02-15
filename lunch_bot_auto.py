import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import schedule
import time

def updateMenu():
    todayMenu = requests.request('GET','https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx=6442')
    todayMenuLunch = json.loads(todayMenu.text)['data']['2']
    menu = [0] * 5
    for i in range(5):
        menu[i] = {
            'name':todayMenuLunch[i]['name'],
            'side':todayMenuLunch[i]['side'],
            'corner':todayMenuLunch[i]['corner'],
            'kcal':todayMenuLunch[i]['kcal'],
            'thumbnailurl':todayMenuLunch[i]['thumbnailUrl']
        }
    return menu

def getRenderString(menu):
    renderstring = ''
    renderstring += '### ' + date.today().strftime("%Y-%m-%d") + ' 오늘의 점심\n'
    for i in range(5):
        renderstring += '**' + str(i+1) + '. ' + menu[i]['corner'] + '**\n'
        renderstring += '##### ' + menu[i]['name'] + '\n'
        renderstring += menu[i]['side'] + '\n'
        renderstring += str(int(menu[i]['kcal'])) + 'kcal\n'
        renderstring += '![' + menu[i]['name'] + '](' + menu[i]['thumbnailurl'] + ' =300)\n'
        if i < 4:
            renderstring += '***\n'
    return renderstring

def post(menu, url_hook):
    headers = {'Content-Type':'application/json'}
    data = {'text':'bot'}
    response = requests.post(url_hook,
                             headers=headers,
                             data=json.dumps({"text":menu}))
    
def dailyUpdateAndPost(url_hook):
    post(getRenderString(updateMenu()), url_hook)

def dailyMenuUpdate():
    url_hook = 'https://meeting.ssafy.com/hooks/r8st8df36jbffyiaykwrdkyjuy'
    dailyUpdateAndPost(url_hook)

if __name__ == '__main__':
    localtime = "11:00"
    schedule.every().monday.at(localtime).do(dailyMenuUpdate)
    schedule.every().tuesday.at(localtime).do(dailyMenuUpdate)
    schedule.every().wednesday.at(localtime).do(dailyMenuUpdate)
    schedule.every().thursday.at(localtime).do(dailyMenuUpdate)
    schedule.every().friday.at(localtime).do(dailyMenuUpdate)

    while(True):
        schedule.run_pending()
        time.sleep(20)
print(getRenderString(updateMenu()))
'''
# 가동 방법
1. 적당한 24시간 가동 가능한 파이썬 환경이 필요합니다.
저는 GCP 무료 설정 찾아서 그거 대로 설정했어요.
2. 매터모스트 왼쪽 위
ㅁㅁㅁ
ㅁㅁㅁ
ㅁㅁㅁ
아이콘 > 통합 > 전체 Incoming Webhook > Incoming Webhook 추가해주세요.
채널은 봇이 있는 채널 선택하면 됩니다.

3. URL을 dailyMenuUpdate함수 url_hook에 붙여넣기 해주세요.

4. pip로 requests, bs4, json, schedule중 설치가 되지 않은 라이브러리가 있다면 설치해주세요.

5. 프로그램을 실행시킵니다.

# 동작 원리
https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx=6442
에서 json을 긁어와서 메터모스트 메시지로 바꾸어 보내는 방식입니다.

# localtime
서버 시간이랑 한국 시간이 다를 수 있어서
서버 시간 계산해서 알람 띄우고 싶은 시간을 계산해야 됩니다
저는 원하는 시간 -9시간으로 지정하면 맞던데 실제로도 그런지 확인은 해봐야 합니다.
datetime.datetime.now() 실행하면 서버 시간 확인할 수 있을 거에요.

#
그리고 schedule 실행 코드를 안 넣었었는데
못본 척 하고 이걸로 한번 실행해주세요 ㅎㅎ;
혹시 또 모르니까 일단 임시로 채널 파서 거기서 테스트 해보고

# 제약
일단 dailyMenuUpdate() 몇 번 실행시켜봐서 문제 없는건 확인 했는데
며칠 더 돌려봐야 진짜 잘 돌아가는지 알 수 있어요
안되면 왜 안되는지는 저도 찾아봐야됩니다.
'''