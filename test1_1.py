import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
url = "https://sso1.mju.ac.kr/login.do?redirect_uri=https://myiweb.mju.ac.kr/index_Myiweb.jsp"
target_url = "https://myiweb.mju.ac.kr/servlet/su/suh/suh03/Suh03Svl02studentGradeList"

# id, passwrd
user = '60141929'
password = 'Ekgus!35790'


args = ["hide_console", ]
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# driver = webdriver.Chrome('chromedriver.exe')
driver = webdriver.Chrome('chromedriver.exe', service_args=args, chrome_options=options) # Run chromedriver.exe

driver.get(url)

driver.find_element_by_name('id').send_keys(user)
driver.find_element_by_name('passwrd').send_keys(password)
driver.find_element_by_xpath('//*[@id="loginButton"]').click()

driver.get(target_url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
data = soup.find_all("table",{"class":"board_list"})
table_html = str(data)
table_df_list = pd.read_html(table_html)
df = table_df_list[-1]

target = (df.loc[df['이수구분'].str.contains('전공')])
# print(target)
df_test = target[['이수구분', '연도', '교과목명', '학점', '성적']]
# print(target)
# print(df_test)
score_list = df_test.values.tolist()
print(score_list)