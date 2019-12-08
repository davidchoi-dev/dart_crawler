import requests as rq
from bs4 import BeautifulSoup
import time

BASE_URL = "http://dart.fss.or.kr/corp/searchCorpL.ax"

searchIndex = 0 # ㄱ~ㅎ, A~Z 검색, 0: ㄱ, 1: ㄴ, ...
currentPage = 1 # pagination

while searchIndex < 17:
  currentPage = 1
  is_last_page = False

  while not is_last_page:
    res = rq.post(BASE_URL, data={"currentPage": currentPage, "searchIndex": searchIndex})
    soup = BeautifulSoup(res.content, 'lxml')

    table_rows = soup.select('.table_scroll table tbody tr')
    for table_row in table_rows:
      
      office_info1 = table_row.select('td')
      if len(office_info1) < 3: 
        is_last_page = True
      else: 
        office_info2 = table_row.select('input')
        
        admin_name = office_info1[0].text.strip()
        description = office_info1[3].text.strip()
        category = office_info1[1].text.strip()
        code = office_info2[1].get('value', '').strip()
        
        print('대표자: %s, 종목: %s, 코드: %s, 설명: %s'%( admin_name, category, code, description))
    print('search index: %d, current page: %d, row count: %d, is_last: '%(searchIndex, currentPage, len(table_rows)), is_last_page)
    currentPage = currentPage + 1
    time.sleep(1.5)

  searchIndex = searchIndex + 1