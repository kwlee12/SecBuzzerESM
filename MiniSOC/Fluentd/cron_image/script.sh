find /Logs/ -type f -ctime +3 | xargs tar zcvf `date +'%Y-%m-%d'`.tar.gz --remove-files
find /Logs/ -type d -empty -delete

chgrp 1000 /root/*
chown 1000 /root/*
echo [*] `date +'%Y-%m-%d'` exec ES index remove $LAST_DATE >> /var/log/cron.log