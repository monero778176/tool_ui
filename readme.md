### 整體大環境架構
採用 vue3/Fastapi 
目的: 整合一些方便本地端可運行的便利工具

### 初步完成進度
- [x] **批次處理剪裁工具**
    實現類似批次處理圖片切割
    目標:提供不聯網的功能 (資料上傳、執行都在本地端)
    概念參照: [Birme](https://www.birme.net/) 的圖片切割網站
- [ ] **圖片上傳轉文字翻譯**
    預計實現目標: 
    - 可以頁面剪裁後的結果直接貼上
    - 拖曳檔案至頁面區域中完成自動上傳
### 執行
前端開啟
```
cd front
npm run serve
```

#### 後端
1.**建立 venv 及安裝依賴 package**
```
cd front
npm install
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
- [ ] **一鍵部屬** 包含使用 bash 啟動 docker 環境建立，提供直接使用。
- [ ] **優化後端邏輯部署** : 採用 APIrouter 程式碼優化、梳理邏輯