<template>
  <div id="app">
    <h1>BIRME Clone with Vue 3</h1>
    <input type="file" multiple accept="image/*" @change="onFilesChange" />

    <div v-if="images.length > 0">
      <label>
        寬度:
        <input type="number" v-model.number="resizeWidth" />
      </label>
      <label>
        高度:
        <input type="number" v-model.number="resizeHeight" />
      </label>
      <label>
        邊框寬度:
        <input type="number" v-model.number="borderWidth" />
      </label>
      <label>
        邊框顏色:
        <input type="color" v-model="borderColor" />
      </label>
      <button @click="processImages">處理圖片</button>
      <button @click="downloadAll">下載所有圖片</button>
    </div>

    <div class="image-list" v-if="processedImages.length > 0">
      <div v-for="(image, index) in processedImages" :key="index" class="image-item">
        <img :src="image" alt="Processed Image" />
      </div>
    </div>
  </div>
</template>

<script>
import JSZip from "jszip";
// import { saveAs } from "file-saver";

export default {
  data() {
    return {
      images: [], // 原始圖片文件
      processedImages: [], // 處理後的圖片 Base64
      resizeWidth: 300, // 預設縮放寬度
      resizeHeight: 300, // 預設縮放高度
      borderWidth: 10, // 預設邊框寬度
      borderColor: "#000000", // 預設邊框顏色
    };
  },
  methods: {
    onFilesChange(event) {
      this.images = Array.from(event.target.files); // 讀取多張圖片
    },
    processImages() {
      this.processedImages = [];
      this.images.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            // 建立 canvas
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");

            // 計算縮放比例
            const aspectRatio = img.width / img.height;
            canvas.width = this.resizeWidth;
            canvas.height = this.resizeHeight || this.resizeWidth / aspectRatio;

            // 繪製圖片
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            // 添加邊框
            ctx.lineWidth = this.borderWidth;
            ctx.strokeStyle = this.borderColor;
            ctx.strokeRect(
              0,
              0,
              canvas.width,
              canvas.height
            );

            // 獲取處理後的圖片 Base64
            this.processedImages.push(canvas.toDataURL("image/png"));
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(file);
      });
    },
    async downloadAll() {
      const zip = new JSZip();
      this.processedImages.forEach((image, index) => {
        const base64Data = image.split(",")[1];
        zip.file(`image${index + 1}.png`, base64Data, { base64: true });
      });

      // 壓縮並下載
      // const blob = 
      await zip.generateAsync({ type: "blob" });
      // saveAs(blob, "processed_images.zip");
    },
  },
};
</script>

<style>
#app {
  text-align: center;
}
.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}
.image-item img {
  max-width: 300px;
  border: 1px solid #ccc;
}
</style>
