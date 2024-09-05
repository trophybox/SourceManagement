#上手くいったコード　販売中のものに絞る必要あり。

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:23:14 2022

@author: Tomita
"""

# import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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

# URL開く
driver.get("https://auctions.yahoo.co.jp")
# 待機処理
# driver.implicitly_wait(10)
sleep(10)
wait = WebDriverWait(driver=driver, timeout=60)

# 閉じるボタンを見つけてクリック
close_button = driver.find_element(By.CSS_SELECTOR, 'a.Close-sc-uncojt.UslsY')
close_button.click()

#検索窓
Word = "チ。―地球の運動について"
driver.find_element(By.XPATH, '//*[@id="sbn"]/div/div[1]/div/input').send_keys(Word)
#driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
    
sleep(1)
driver.find_element(By.XPATH,'//*[@id="acHdSchBtn"]').click()

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
    URLS = driver.find_elements(By.CSS_SELECTOR,"a.Product__imageLink")
    
    for URL in URLS:
        URL = URL.get_attribute("href")
        print("[INFO] URL :", URL)
        HREFS.append(URL)
        
    #待機処理
    wait.until(EC.presence_of_all_elements_located)

    # 次のページへ
    try:
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a.Pager__link[data-cl-params*='_cl_link:next']")
            next_btn.click()
        except KeyboardInterrupt:
            break
    except:
        break
    