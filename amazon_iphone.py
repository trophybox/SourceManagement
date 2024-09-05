#amazon 新品のiphoneの商品情報を取得　成功

# import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import csv

# wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# selenium 4.0 ↑
from selenium.webdriver.common.by import By
from time import sleep

chrome_options = Options()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

HREFS = []
product_data = []

# URL開く 
driver.get("https://www.amazon.co.jp/s?i=electronics&bbn=128187011&rh=n%3A128187011%2Cp_n_feature_eleven_browse-bin%3A2519089051%2Cp_123%3A110955%2Cp_n_condition-type%3A2249602051&dc&qid=1724678169&rnid=2249601051&ref=sr_nr_p_n_condition-type_2&ds=v1%3AjHuSqHp2Wh%2FHefXL22h8cN4OGwAohkGpja2UXzT2q74")
# 待機処理
# driver.implicitly_wait(10)
sleep(10)
wait = WebDriverWait(driver=driver, timeout=60)

while True:
    #待機処理
    wait.until(EC.presence_of_all_elements_located)
    #ブラウザのウインドウ高を取得
    win_height = driver.execute_script("return window.innerHeight")
    
    #スクロール開始位置の初期値（ページの先頭からスクロールを開始する）
    last_top = 1
    
    #ページの最下部までスクロールする無限ループ
    while True:
    
      #スクロール前のページの高さを取得
      last_height = driver.execute_script("return document.body.scrollHeight")
      
      #スクロール開始位置を設定
      top = last_top
    
      #ページ最下部まで、徐々にスクロールしていく
      while top < last_height:
        top += int(win_height * 0.8)
        driver.execute_script("window.scrollTo(0, %d)" % top)
        sleep(0.5)
    
      #１秒待って、スクロール後のページの高さを取得する
      sleep(1)
      new_last_height = driver.execute_script("return document.body.scrollHeight")
    
      #スクロール前後でページの高さに変化がなくなったら無限スクロール終了とみなしてループを抜ける
      if last_height == new_last_height:
        break

    #次のループのスクロール開始位置を設定
    last_top = last_height
    
    #商品URLの取得
    URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")
    
    for URL in URLS:
        URL = URL.get_attribute("href")
        # print("[INFO] URL :", URL)
        HREFS.append(URL)
    #待機処理
    wait.until(EC.presence_of_all_elements_located)

    # 次のページへ
    try:
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".s-pagination-next.s-pagination-separator")
            next_btn.click()
        except KeyboardInterrupt:
            break
    except:
        break
    
    #商品詳細の取得
for HREF in HREFS:
    driver.get(HREF)
    
    #uniqueID
    unique_id = f"AIP-{uuid.uuid4()}"
    
    #title
    try:
        title = driver.find_element(By.ID,"productTitle").text
    except NoSuchElementException:
        title = "NULL"
    #brand
    brand = "Apple"
    #condition
    condition = "new"
    #price
    try:
        price = driver.find_element(By.CSS_SELECTOR, '.a-price.a-text-price.a-size-medium span.a-offscreen').text
    except NoSuchElementException:
        try:
            price = driver.find_element(By.CSS_SELECTOR, '.a-price.a-text-price.a-size-medium span[aria-hidden="true"]').text
        except NoSuchElementException:
            price = "NULL"
    price = price.replace('￥', '').replace(' ', '')
    #img
    try:
        img = driver.find_element(By.XPATH,'//div[@id="imgTagWrapperId"]/img').get_attribute("src")
    except NoSuchElementException:
        try:
            img = driver.find_element(By.XPATH,'//img[@id="landingImage"]').get_attribute("src")
        except:
            img = "NULL"
    product_data.append([unique_id,title,brand,price,condition,img,URL])
        


# CSVファイルのヘッダーを定義
headers = ['ID', 'Title', 'Brand', 'Price', 'Condition', 'Image URL', 'Product URL']

# CSVファイルを書き込みモードで開く
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # ヘッダーを書き込む
    writer.writerow(headers)
    
    # product_dataの各行を書き込む
    for row in product_data:
        writer.writerow(row)

print("CSVファイルの出力が完了しました。")