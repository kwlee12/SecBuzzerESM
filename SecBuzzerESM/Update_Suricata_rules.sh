rm Suricata/suricata/dist/suricata.yaml
rm Suricata/suricata/rules/*

cp WEB/rules/*.rules Suricata/suricata/rules/
cp WEB/rules/suricata.yaml Suricata/suricata/dist/suricata.yaml
docker-compose --env-file SecBuzzerESM.env -f Suricata/docker-compose.yml restart