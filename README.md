gogolook
========

This is a server side api service for gogolook

[環境設定]:
  * programming Language: Python
  * framework: Bottle
  * SQL: MySQL

[Python package]:
  * python-sqlalchemy
  * python-bottle
  * python-mysqldb
  * python-transaction

[MySQL table schema]:
  * owner_email (primary)
  * redeem_code (unique)
  * item_no
  * create_time
  * receiver_email (index)
  * receive_time
  * receive_ip  
  (時間和 ip 位置以後可以用來 mining 出很多資訊)

[界面 1]: 
  * INPUT & OUTPUT 說明: 
    應用程式可利用此界面用使用者輸入的 email 來取得一個 redeem code 

  * INPUT: 使用 HTTP GET METHOD 提供兩項參數: 
    1. email(註冊者信箱) 
    2. item_no(兌換商品編號)

  * 參考範例網址: 
    http://chientung.net:5566/GenRedeem?email=test@gogolook.com&item_no=100
    
  * OUTPUT: Your code here: XXXXXXXX

  * 補充說明: 
    1. redeem code 為八個英數字組合， 
    2. 同一個 email 取得的 redeem code 相同 
    3. redeem code 都不得重複， 
    4. 來索取的使用者數量無限制 (講得更明確就是程式邏輯至少允許上百萬使用者透過這個界面取得 redeem code) 

  * 程式邏輯:
    1. 判斷系統參數是否足夠
    2. 判斷是否為合法的 email 格式
    3. 檢查此 email 是否已經註冊過，如果是則傳回上次產生的 redeem code
    4. 檢查產生的 redeem code 是否有重複
    5. 回傳 redeem code

  * 額外說明:
    通常比較好的做法應該是將 redeem 寄回給使用者以確保使用者的信箱是正確的，避免使用假信箱申請

[界面 2]: 
  * INPUT & OUTPUT 說明: 
    應用程式可利用此界面拿使用者輸入的 redeem code 來兌換禮物並回應是否成功 

  * INPUT: 使用 HTTP GET METHOD 提供兩項參數:
    1. receiver_email (領獎人信箱)
    2. redeem_code (兌換號碼)

  * 參考範例網址:
    http://chientung.net:5566/RecRedeem?receiver_email=test@gogolook.com&redeem_code=kQcFhqTd

  * OUTPUT: Yout item here: item_no (兌換商品編號)
    == Notice == 
      a. 兌換碼不可以自己送給自己 
      b. 兌換碼只可使用一次

  * 補充說明:
    redeem code 兌換成功條件最小條件如下 
    1. redeem code 必須要存在於資料庫並且被應用程式利用界面 1 被使用者取用 
    2. 一個使用者只能使用同個 redeem code 一次 
    3. 一個使用者可以成功兌換三次 

  * 程式邏輯:
    1. 判斷系統參數是否足夠
    2. 判斷是否為合法的 email 格式
    3. 判斷兌獎者是否已經收超過三次兌換券
    4. 判斷兌換券是否是有效
    5. 判斷兌獎人和給獎人是否相同 (自己送給自己)
    6. 判斷兌換券是否已經使用過
    7. 回傳 兌換商品編號

[程式架構]:
  * 主程式為 server.py
  * 其中有三項資料夾
    1. module
      用來存放程式中所以需要用到的模組
    2. setting
      將程式運作所需要使用到的設定統一在此設定 (MySQL 和 HOST)
    3. sql
      SQLAlchemy 所需要用到的 DB 架構
  * 系統 log
    主程式運行後會再本地資料夾產生 error.log。因為 API Server 會有大量的 request，
    但無法確保程式在永遠的狀況下都沒有任何的錯誤機會，因此在程式中安插了 logger 用
    來做之後 debug 使用。目前是使用單一檔案，但之後應該要採用設定統一放 log 的位置
    ，並且使用 rotate 的方式定期將舊的 Log 紀錄丟掉才不會增加磁碟的負擔。










