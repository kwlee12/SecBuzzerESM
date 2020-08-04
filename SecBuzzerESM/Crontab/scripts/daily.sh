#/bin/bash

rm /suricata_log/eve-`date -d "-2 days" "+%Y-%m-%d"`.json 2>/dev/null
echo "[*] remove eve-`date -d "-2 days" "+%Y-%m-%d"`.json"