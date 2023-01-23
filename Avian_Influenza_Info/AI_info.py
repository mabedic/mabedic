import requests
from bs4 import BeautifulSoup
from selenium import webdriver

webdriver_options = webdriver.ChromeOptions()
webdriver_options .add_argument('headless')

chromedriver = 'C:\web_driver/chromedriver.exe'
driver = webdriver.Chrome(chromedriver, options=webdriver_options)

req1 = requests.get('https://www.mafra.go.kr/FMD-AI2/2179/subview.do') #URL 불러오기
html1 = req1.text #URL HTML 텍스트만 불러오기
soup1 = BeautifulSoup(html1, 'html.parser')
post = soup1.find("tr") #html <tr> 부분만 불러오기
post_num = post.find("td", { "class" : "tbl_num" }).text #post에서 <td>안의 숫자중 텍스트만 불러오기

name = post.find("td", { "class" : "tbl_title" }).text #새 글 이름
link = 'https://www.mafra.go.kr/' +post.find("td", { "class" : "tbl_title" }).find("a").attrs['href'] #새 글 링크

req2 = requests.get(link)
html2 = req2.text
soup2 = BeautifulSoup(html2, 'html.parser')
look_view = 'https://www.mafra.go.kr' +soup2.find('a', id='fileview').attrs['href']

driver.get(look_view)
driver.switch_to.frame('innerWrap')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.close()

title1 = soup.select_one('#table_2').text
fn_title = title1()

print(title1)
