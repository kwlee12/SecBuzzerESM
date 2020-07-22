# Release History
## V0.2.4
- 將 MiniSOC 改為 SecBuzzerESM

## V0.2.3
- 修改 Suricata docker-compose.yml, 修正 Build 後讀不到網卡

## V0.2.2
- 更新 Top Suricata Rules (20200721)

## V0.2.1
- 將 WEB 需要的 API KEY 加入到 MiniSOC.env
- 移除 POC 用不到的檔案 (Fluentd cron 備份 raw log)
- 
## V0.2.0
- 調整 sucicata, 不會輸出 fast.log, suricata.log
- 移除 POC 用不到的檔案

## V0.1.0
- Init, Base on MiniSOC 1.0.8
- Install.sh 腳本加上防呆
- 移除 Fluentd raw log 輸出
- 移除 prepare.sh & 舊版 install.sh
- 將 WEB 服務讀取的網卡加MiniSOC.env