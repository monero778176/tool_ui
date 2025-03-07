### 建議環境及安裝
採用 vue3/Fastapi 實現類似批次處理圖片切割
目標:提供不聯網的功能 (資料上傳、執行都在本地端)
概念參照: Birme 的圖片切割網站

### 執行
前端開啟
```
cd front
npm run serve
```

#### 後端
1.**建立 venv 及安裝依賴 package**
```

```

2.**執行**
- Linux 環境在啟動虛擬環境需要加上 `conda` 前綴
- 建議 python 3.9
```
activate <venv>
cd back_server
uvicorn main:app --host localhost --port 8081  --reload

```



### 後續更新待做
**一鍵部屬**
包含使用 bash 啟動 docker 環境建立，提供直接使用。