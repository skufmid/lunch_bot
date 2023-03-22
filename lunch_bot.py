import requests
import datetime

print(f'### {datetime.date.today()} 오늘의 점심')
url = 'https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx=6442'
r = requests.get(url).json().get('data').get('2')
for num in range(5):
    if num: print('***')
    data = r[num]
    corner = data['corner']
    name = data['name']
    side = data['side']
    kcal = int(data['kcal'])
    carb = int(data['carb'])
    protein = int(data['protein'])
    fat = int(data['fat'])
    salt = int(data['salt'])
    thumb_url = data['thumbnailUrl']

    print(f'**{num+1}. {corner}**')
    print(f'##### {name}')
    print(side)
    # print(f'탄수화물 {carb}g  단백질 {protein}g  지방 {fat}g') # 나트륨 {salt}mg')
    print(f'{kcal}kcal')
    print(f'![{name}]({thumb_url} =300)')
