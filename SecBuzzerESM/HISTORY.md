# Release History
## V0.2.13
- 修正 Update_Suricata_rules.sh 檔案路徑

## V0.2.12
- Suricata 資料新增 dump_status 欄位

## V0.2.11
- 上傳初版 Suricata 更新腳本

## V0.2.10
- 修改 eve.json rotate 的區間
 
## V0.2.9
- 修正 Suricata 讀取不到網卡

## V0.2.8
- 修正 Fluentd 沒將規則送到 ES
- 修正 Cron 腳本不會自動重啟

## V0.2.7
- 新增離線安裝腳本 & 打包腳本

## V0.2.6
- 修正 Top Suricata Rules 因檔案名稱相同覆蓋狀況

## V0.2.5
- 修改 Suricata 設定檔, 避免 Windows 無法存取 Log
- 將 Suricata Image 上傳到 Docker hub

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
