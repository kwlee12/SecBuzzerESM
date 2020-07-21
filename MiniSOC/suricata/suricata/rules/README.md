# 規則檔案說明

### suricata
Suricata的預設規則 (執行規則更新後，每次更新後預設的規則應會有所不同)

### av_pro
由AlienVault商業版中取出的偵測規則

### csti_waf
由社群組建立的規則，主是由WAF規則改過來

### csti_verify
簡單的規則測試，用來測試Suricata是否可正常運作

### csti_pick
基於Suricata的預設規則以及AlienVault Pro中的規則，利用一些攻擊的工具進行測試，把一些有跳告警的規則挑出

### csti_detect
於實際場域中，在偵測出異常行為時有用到的規則

### csti_baseline
東杰團隊所提供的規則

### csti_reduction
以「csti_baseline」為基礎，在「資安所」的場域中，把不重要的規則disable，以減少告警量

### Miaoli
苗栗地政局

### csh
中山附醫


