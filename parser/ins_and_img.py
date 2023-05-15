import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

url = 'https://whattomine.com/asic'

response = requests.get(url)
page_content = response.content

soup = BeautifulSoup(page_content, 'html.parser')

asics = soup.find_all("div", {"class": "col-sm"})

asic_name = asics.find('SHA-256')


print(asics)

asic_type_option['selected'] = True

hashrate_input = form.find('input', {'id': 'hr'})

hashrate_input['value'] = '15000'

submit_button = form.find('button', {'class': 'btn-primary'})
response = driver.execute_script(
    "arguments[0].scrollIntoView(true);arguments[0].click();", submit_button)

driver.implicitly_wait(10)

page_content = driver.page_source

soup = BeautifulSoup(page_content, 'html.parser')

result_table = soup.find('table', {'class': 'table-sm'})

table_image = driver.find_element_by_xpath('//table').screenshot_as_png

with open('table.png', 'wb') as f:
    f.write(table_image)

driver.quit()
