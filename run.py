import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def find_link(link_list):
    global email,website
    email = 'None'
    website = 'None'
    for link in link_list:
        if link.text == 'Email':
            email = link.get('href')
            email = email[7:]
        elif link.text == 'Website':
            website = link.get('href')


s = Service('C:\Program Files (x86)\chromedriver.exe')
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options=op,service=s)
URL = 'http://yellowpages.in/hyderabad/hotels/361872729'
browser.get(URL)
button_class_name = 'loadMoreBtn'
while True:
    try:
        WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, button_class_name))).click()
        time.sleep(3)
    except:
        break

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

list = soup.find_all('div',class_='eachPopular')
main_df = pd.DataFrame()

for l in list:
    name = l.find('div',class_='popularTitleTextBlock').text
    open = l.find('div',class_='openNow').text
    try:
        hotel_type = l.find('ul',class_='eachPopularTagsList').text
    except:
        hotel_type = 'None'
    link_list = l.find('div',class_='eachPopularLink')
    find_link(link_list)
    phone_number = l.find('a',class_='businessContact').text
    address = l.find('address', class_='businessArea').text
    df = pd.DataFrame({'Name': [name],
                       'Available': [open],
                       'Hotel Type':[hotel_type],
                       'Phone Number': [phone_number],
                       'Address': [address],
                       'Email':[email],
                       'Website': [website]})
    main_df = pd.concat([main_df, df])

main_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
browser.close()