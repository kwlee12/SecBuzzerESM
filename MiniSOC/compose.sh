#!/bin/bash
if [ "$1" = "up" -o "$1" = "u" ]
then
    cmd="up -d"
elif [ "$1" = "down" -o "$1" = "d" ]
then
    cmd="down"
fi

docker-compose --env-file MiniSOC.env -f ES/docker-compose.yml $cmd
docker-compose --env-file MiniSOC.env -f Fluentd/docker-compose.yml $cmd
docker-compose --env-file MiniSOC.env -f WEB/docker-compose.yml $cmd
docker-compose --env-file MiniSOC.env -f suricata/docker-compose.yml $cmd
docker-compose --env-file MiniSOC.env -f Crontab/docker-compose.yml $cmd