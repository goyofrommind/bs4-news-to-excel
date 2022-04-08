from itertools import count
from matplotlib.pyplot import title
from pytz import HOUR
import requests
from bs4 import BeautifulSoup
import openpyxl
import time

def gy_soup(url):  #res url ,headers 함수로 만들기
    headers = ({'User-Agent':'Mozilla/5.0'})        # 매크로로 막을 수가 있어서 헤더를 조금이라도 넣어서 피함.
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

time = time.strftime('%I')          # 현재 시간 표시

# 파일이 있으면 그 파일에 저장 / 없으면 새로 파일 생성
## 추가 수정할사항 :  시간으로 가져오기때문에 시트에 시간에따른 추가를 해볼예정.
try:            
    wb = openpyxl.load_workbook("{}시 많이본 뉴스_.xlsx".format(time))      
    sheet = wb.active 
    sheet.title ='뉴스'
    
    print("파일 갱신 완료")
except :
    wb = openpyxl.Workbook()
 
    sheet = wb.active
    sheet.title = '뉴스'
    sheet.append(["제목", "링크",])
    sheet
   
    print("새로운 파일 생성 완료")


def gy_news():     ##뉴스 가져오는 항목.
    url = "https://news.naver.com/main/officeList.naver"
    soup = gy_soup(url)

    news_title = soup.find("h4").get_text()                                 #h4태그를 이용하는 곳에 텍스트를 가져옴
    news_time = soup.find("p", attrs ={"class":"section_sub_txt"}).get_text()
    # news = soup.find_all("div", attrs = {"class":"list_text_inner"})       #아래랑 같음
    news = soup.find_all("div", attrs = {"class":"list_text"},limit=50)       #"class":"list_text"를 3개로 제한. 랭킹85까지 있어서 limit 안하면 85까지 출력

    #뉴스 출력
    print("[{}]".format(news_title))                #언론사별 가장 많이 본 뉴스 글자타이틀
    print(">>{}<<".format(news_time))               #집계된 뉴스 시간
    print()                                         #빈줄 하나 추가
    for index, news in enumerate(news):             #12345 순서대로 출력하기 위해 enumerate ,index 사용
        title = news.a.get_text()                   #news에서 텍스트만 가져옴
        link = "https://news.naver.com/" + news.a["href"]      #href가 들어간 태그를 가져옴
        # print(index, title, link)
        print("{}. {}".format(index+1, title))
        print("   (링크 : {})".format(link))
        sheet.append([title,link])
    print("-"*100) # 줄긋기


if __name__ == "__main__":
    gy_news()

wb.save("{}시 많이본 뉴스.xlsx".format(time))