import time

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def math(user_name, currency, cost_electricity, hash, potreb, komm, coin):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://ultramining.com/crypto-calc/{coin}/")

    if currency == 'USD $':
        driver.find_element(By.CLASS_NAME, 'input-group-append').click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='content']/div[2]/div[2]/div[1]/div/div/div/div[1]").click()
        time.sleep(1)
    else:
        pass

    price = driver.find_element(By.XPATH, "//*[@id='input-electricity']", )
    price.clear()
    price.send_keys(cost_electricity)

    price = driver.find_element(By.XPATH, "//*[@id='input-electricity']", )
    price.clear()
    price.send_keys(cost_electricity)

    price = driver.find_element(By.XPATH, "//*[@id='input-hashrate']")
    price.clear()
    price.send_keys(hash)

    price = driver.find_element(By.XPATH, "//*[@id='input-consumption']")
    price.clear()
    price.send_keys(potreb)

    price = driver.find_element(By.XPATH, "//*[@id='input-commission']")
    price.clear()
    price.send_keys(komm)

    time.sleep(1)

    rows = driver.find_element(By.CLASS_NAME, 'dataTables_scrollBody')

    row_body = rows.find_element(By.TAG_NAME, 'tbody')
    row_name = row_body.find_elements(By.TAG_NAME, 'tr')

    bable = []

    for row in row_name:
        row_text = row.text
        median_text = row_text.split()
        median_text[2] = str("{0:.10f}".format(float(median_text[2])))
        pre_fi = [median_text[0] + ' ' + median_text[1], median_text[2] + ' ' +
                  median_text[3], median_text[4], median_text[5] + median_text[6], median_text[7]]
        bable.append(pre_fi)

    df = pd.DataFrame(bable, columns=['Period', 'Reward', 'Income', 'Expenses', 'Profit'])

    columns = ['Period', 'Reward', 'Income', 'Expenses', 'Profit']
    data = df[columns].values.tolist()

    font = ImageFont.truetype('arial.ttf', 22)
    cell_size = (270, 130)

    num_rows = len(data)
    num_cols = len(columns)
    table_size = (num_cols * cell_size[0], (num_rows + 1) * cell_size[1])

    im = Image.new('RGB', table_size, (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for i, col in enumerate(columns):
        draw.rectangle((i * cell_size[0] + 100, 100, (i + 1) * cell_size[0] + 100, cell_size[1] + 100),
                       fill=(255, 255, 255), outline=(255, 255, 255))
        draw.text((i * cell_size[0] + 48, 90), col, font=font, fill=(0, 0, 0))

    for i in range(num_rows):
        for j in range(num_cols):
            draw.rectangle(
                ((j * cell_size[0], (i + 1) * cell_size[1]), ((j + 1) * cell_size[0], (i + 2) * cell_size[1])),
                fill=(255, 255, 255), outline=(255, 255, 255))
            draw.text((j * cell_size[0] + 50, (i + 1) * cell_size[1] + 50), str(data[i][j]), font=font, fill=(0, 0, 0))

    filename = fr"C:\Users\37533\PycharmProjects\parser-v2\logo_new.png"

    with Image.open(filename) as img:
        img.load()
    im.paste(img, (10, 10), mask=img.convert('RGBA'))
    im.save(fr"C:\Users\37533\PycharmProjects\parser-v2\photos\{user_name}.png")

    driver.quit()

    filename = fr"C:\Users\37533\PycharmProjects\parser-v2\photos\{user_name}.png"

    return filename
