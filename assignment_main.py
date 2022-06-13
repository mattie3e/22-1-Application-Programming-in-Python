import requests
from bs4 import BeautifulSoup
import sqlite3
from custom import practice as p

# 로그인
url = 'https://learn.inha.ac.kr/login/index.php'
member_data = {
    'username': '12214180',
    'password': 'iohchick1@$'
}

s = requests.Session()

resp = s.post(url, data=member_data)

# 로그인한 뒤 페이지 내용 가져오기
info_url = 'https://learn.inha.ac.kr/'
resp = s.get(info_url)

# 과목 id와 과목명 출력 완료
soup = BeautifulSoup(resp.text, features="html.parser")
b = soup.find_all("a", "course_link")
c = soup.find_all("h3")

name = []
number = []

print(c[3].text)

for x in range(len(c)):  # 과목명
    if c[x].text[-1] == ']' or c[x].text[-1] == 'W':
        name.append(c[x].text.split('[')[0])

for x in b:  # 과목번호
    if len(number) == len(name):
        break
    number.append(x.attrs['href'][-5:])

print(name)
print(number)

# 과제 기한 가져오기! 퀴즈도 가져올...까?
# 필요한 것
# 과제 존재 여부
# 해당 주차, 과제명, 종료일시, 제출 여부

# 과제 페이지
assign_url = 'https://learn.inha.ac.kr/mod/assign/index.php?id='

resp = s.get(assign_url + str(number[3]))
soup = BeautifulSoup(resp.text, features="html.parser")
d = soup.find_all("tr")

print(d)
print(type(d))

# cell 정보로 파싱 - 제출완료는 무시하기
comp = soup.find_all('td', class_='cell c3')
print(comp)

index = []
cnt = 0

for x in comp:
    if x.text == "미제출":
        index.append(cnt)
    cnt += 1

print("미제출만")
ins = []

for i in index:
    print(d[i+1].text)
    temp = d[i+1].text.split('\n') # 2,3,4번째만 필요
    assign_name = temp[2]
    assign_date = temp[3][-11:-9] + temp[3][-8:-6]
    print(assign_date)

    if assign_date[0] == '0':
        month = assign_date[1]
    else:
        month = assign_date[:1]

    if assign_date[2] == 0:
        day = assign_date[3]
    else:
        day = assign_date[2:]

    print(month)
    print(day)

    ins.append([month, day, name[3] + ' ' + assign_name])


for x in ins:
    conn = sqlite3.connect('E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db')
    cur = conn.cursor()

    cur.execute('INSERT INTO m' + x[0] + ' (date, schedule) VALUES (?, ?)', (x[1], x[2]))

    conn.commit()
    conn.close()

