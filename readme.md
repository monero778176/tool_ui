### 整體大環境架構
採用 vue3/Fastapi 實現
目標:提供不聯網的功能 (資料上傳到批次剪裁都是在本地端執行)
概念參照: [Birme](https://www.birme.net/) 的批次圖片剪裁網站


### 執行
前端開啟
```
cd front
npm run serve
```

#### 後端
1.**安裝依賴 package** (需有安裝 node.js 環境)
```
cd front
npm install
```

2.**執行**
- Linux 環境在啟動虛擬環境需要加上 `conda` 前綴
- 建議 python 3.9

**環境中沒有虛擬環境** (電腦須具備python)
1. 創建並啟用虛擬環境
```
python -m venv ./venv
cd venv/Scripts
activate
```
2. 安裝 required package
```
pip install -r ../../requirements.txt
```
3. 運行 back end 後台
```
cd ../..
cd back_server
uvicorn main:app --host localhost --port 8081  --reload

```


### 未來規劃
- [ ] 一鍵docker部署

