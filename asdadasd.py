#https://blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221305144464&categoryNo=81&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView
from urllib.request import urlopen, Request
import urllib
import bs4

#어떤 위치의 날씨를 찾을지 정함
location = '장기동'
enc_location = urllib.parse.quote(location + '+날씨')

#검색주소를 찾음 
url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

#검색한다
req = Request(url)
page = urlopen(req)
html = page.read()

#검색결과
soup = bs4.BeautifulSoup(html,'html5lib')

#출력
print('현재 ' + location + ' 날씨는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
print(soup.find('ul', class_='info_list').text)
