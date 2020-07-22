#Variable setting
createDay="$(date +'%Y-%m-%d')"
createMonth="$(date +'%Y-%m')"

#Increase shard maximum
curl -X PUT "localhost:19200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "transient": {
    "cluster": {
      "max_shards_per_node":50000
    }
  }
}
'

#Create policy 
curl -X PUT "localhost:19200/_ilm/policy/test_policy?pretty" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "30gb"
          }
        }
      }
    } 
  } 
}
'

#Cteate today template
curl -X PUT "localhost:19200/_template/lm-$createDay?pretty" -H 'Content-Type: application/json' -d'
{
        "index_patterns": ["lm-'$createDay'-*"],
        "settings":{
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "test_policy",
          "index.lifecycle.rollover_alias": "lm-'$createDay'",
          "refresh_interval": "30s"
        }
}
'

#Cteate today index
curl -X PUT "localhost:19200/lm-$createDay-000001?pretty" -H 'Content-Type: application/json' -d'
{
  "aliases": {
    "lm-'$createDay'": {
      "is_write_index": true
    }
  }
}
'

#Cteate template
curl -X PUT "localhost:19200/_template/suricata-$createMonth?pretty" -H 'Content-Type: application/json' -d'
{
        "index_patterns": ["suricata-'$createMonth'-*"],
        "settings":{
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "test_policy",
          "index.lifecycle.rollover_alias": "suricata-'$createMonth'",
          "refresh_interval": "30s"
        }
}
'

#Cteate index
curl -X PUT "localhost:19200/suricata-$createMonth-000001?pretty" -H 'Content-Type: application/json' -d'
{
  "aliases": {
    "suricata-'$createMonth'": {
      "is_write_index": true
    }
  }
}
'
