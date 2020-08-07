#/bin/bash

# Call the Winlog AI module
WinlogIndex=winlogbeat_`date -d "-1 days" "+%Y%m%d"`
hourtime=`date -d "-1 hour" +"%Y-%m-%dT%H"`
curl -i "http://localhost:5000/winlog/api/v1.0?index=$WinlogIndex&start_time="$hourtime":00:00&end_time="$hourtime":59:59"
echo "[*] `date +"%Y-%m-%d %H:%M"` Exec Winlog AI module"