#mercari 新品のiphoneの商品情報を取得　成功

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
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException


# wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# selenium 4.0 ↑
from selenium.webdriver.common.by import By
from time import sleep

# chrome_options.add_argument('--headless')
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

HREFS = []
product_data = []

# URL開く 
driver.get("https://jp.mercari.com/search?brand_id=3272&category_id=859&status=on_sale")
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
    URLS = driver.find_elements(By.XPATH,"//a[starts-with(@href, '/item/') and @data-testid='thumbnail-link']")
    
    for URL in URLS:
        URL = URL.get_attribute("href")
        # print("[INFO] URL :", URL)
        HREFS.append(URL)
    #待機処理
    wait.until(EC.presence_of_all_elements_located)

    # 次のページへ
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="pagination-next-button"] > a'))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        sleep(5)
    except KeyboardInterrupt:
        break
    except TimeoutException:
        print("次のページボタンが見つからないか、クリックできませんでした。")
        break
    except ElementClickInterceptedException:
        print("次のページボタンがクリックできません。他の要素に遮られている可能性があります。")
        break
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        break
    
    #商品詳細の取得
for HREF in HREFS:
    driver.get(HREF)
    sleep(3)
    #uniqueID
    unique_id = f"MIP-{uuid.uuid4()}"
    
    #title
    try:
        title = driver.find_element(By.XPATH, "//h1[contains(@class, 'heading__a7d91561') and contains(@class, 'page__a7d91561')]").text
    except NoSuchElementException:
        title = "NULL"
    #brand
    brand = "Apple"
    #condition
    try:
        condition = driver.find_element(By.XPATH, "//*[@data-testid='商品の状態']").text
    except NoSuchElementException:
        condition = "NULL"
    #price
    try:
        price = driver.find_element(By.CSS_SELECTOR, '[data-testid="price"] span:not(.currency)').text
        price = price.replace('￥', '').replace(' ', '')
    except NoSuchElementException:
        price = "NULL"
    #img
    try:
        img_elements = driver.find_elements(By.XPATH, "//figure[contains(@class, 'itemThumbnail__a6f874a2')]//img")
        img = img_elements[0].get_attribute("src") if img_elements else "NULL"
    except NoSuchElementException:
        img = "NULL"
    #produc_dataリストに変数を格納
    product_data.append([unique_id,title,brand,price,condition,img,URL])
        
# CSVファイルのヘッダーを定義
headers = ['ID', 'Title', 'Brand', 'Price', 'Condition', 'Image URL', 'Product URL']

# CSVファイルを書き込みモードで開く
with open('mercari_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # ヘッダーを書き込む
    writer.writerow(headers)
    
    # product_dataの各行を書き込む
    for row in product_data:
        writer.writerow(row)

print("CSVファイルの出力が完了しました。")