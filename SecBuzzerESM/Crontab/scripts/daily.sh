#/bin/bash

# Auto remove eve-yyyy-mm-dd.json
rm /suricata_log/eve-`date -d "-2 days" "+%Y-%m-%d"`.json 2>/dev/null
echo "[*] remove eve-`date -d "-2 days" "+%Y-%m-%d"`.json"

# Call the Winlog AI module
WinlogIndex=winlogbeat_`date -d "-1 days" "+%Y%m%d"`
Daytime=`date -d "-1 days" "+%Y-%m-%d"`
curl -i "http://localhost:15000/winlog/api/v1.0?index=$WinlogIndex&start_time="$Daytime"T00:00:00&end_time="$Daytime"T23:59:59"
echo "[*] Exec Winlog AI module $WinlogIndex"