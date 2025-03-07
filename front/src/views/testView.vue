<template>




    <!-- 側視圖片使用 -->
    <!-- <div style="width: 450px;">
        <cropper :src="img" @change="change" ref="cropper" />
    </div> -->



    <div class="row">
        <h2> Image uploder</h2>



        <!-- 待 crop 的圖片們顯示 -->
        <div class="grid-container col-8" style="margin-left: 5%;">
            <div v-for="(med, index) in media" :key="med.url">
                <!-- 將 upload 的圖片進行顯示 -->

                <div>

                    <!-- <cropper :src="med.url" @change="change" ref="cropper" /> -->
                    <cropper :src="med.url" @change="change" :ref="origin_croppers[index]" />
                    <!-- <cropper :src="med.url" @change="change" :ref="(el)=>setOriginCrop(el)" /> -->
                    <!-- <p>{{ origin_croppers[index] }}</p> -->
                </div>
            </div>
        </div>

        <div class="col-3" style="margin: 10px;">
            <!-- <uploadComponent></uploadComponent> -->
            <div class="flex" style="margin: 10px;">
                <!-- 操作控制台 -->
                <div>
                    <label for="exampleInputEmail1" class="form-label mt-4 ">設定圖片大小</label>
                    <input type="number" class="form-control col-3" id="exampleInputEmail1" aria-describedby="emailHelp"
                        v-model="new_test_size">
                    <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone
                        else.</small>
                </div>

                <!-- 是否使用模型進行偵測大致的位置 -->
                <fieldset style="background-color: 	#F5F5F5; padding-left: 15px;">
                    <legend class="mt-4">Checkboxes</legend>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" :checked="use_model_dection"
                            v-model="use_model_dection" id="flexCheckDefault">
                        <label class="form-check-label" for="flexCheckDefault">
                            使用 model 預先偵測可能框選的點
                        </label>
                    </div>

                    <br>
                </fieldset>

                <button @click="getCrop" class="btn btn-primary">剪裁</button>
                <button @click="handleAllCanvases" class="btn btn-primary">一次剪裁所有</button>
                <h4>crop method</h4>
                <button @click="unified_resize" class="btn btn-info"> 使用無判斷</button>
                <button @click="model_detect_go" class="btn btn-info"> 使用模型判斷</button>
                <h4>download result</h4>
                <button @click="package_download" class="btn btn-secondary"> Download as .Zip</button>
            </div>
            <div>
                <!-- 上傳照片元素 -->
                <h4>點選圖片上傳</h4>
                <Uploader server="http://localhost:8081/api/upload" @change="changeMedia" />
            </div>



        </div>




        <label for="">輸出顯示影像</label>


    </div>




    <div class="show_result">

        <canvas ref="resultCanvas"></canvas>
    </div>

    <div v-for="(med, index) in media" :key="med.url">

        <!-- <p>參考標籤:{{ result_croppers[index] }}</p> -->
        <canvas :ref="result_croppers[index]"></canvas>
        <!-- <canvas :ref="(el)=>setResultCrop(el)"></canvas> -->
    </div>



</template>

<script>
// import { ref } from 'vue';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
// import ImageUpload from 'image-upload-vue'
import Uploader from "vue-media-upload";

import '@/assets/css/bootstrap.min.css'
// import "bootstrap"
import 'jquery'
import { nextTick, ref } from 'vue';
import JSZip from 'jszip';
import axios from 'axios';



// const resultCanvas = ref(null)


// const mediaCropResult = ref([]) // 儲存 用來喜善的 canvas
export default {
    components: {
        Cropper,
        Uploader

    },
    data() {
        return {
            img: 'https://images.pexels.com/photos/4323307/pexels-photo-4323307.jpeg',
            media: [],
            redrawCanvas: [], // 顯示
            test_size: 100,
            origin_croppers: [],
            result_croppers: [],   // 用以儲存
            new_origin: [],
            new_target: [],
            dataList: []
        };
    },

    setup() {
        const new_test_size = ref(512)
        const use_model_dection = ref(true)

        async function urlContentToDataUri(url) {
            // 應該是會回傳 bases64
            return await fetch(url)
                .then(response => response.blob())
                .then(blob => new Promise(callback => {
                    let reader = new FileReader();
                    reader.onload = function () { callback(this.result) };
                    reader.readAsDataURL(blob);

                    console.log('讀取 reader :', reader)
                }));
        }



        return {
            new_test_size,
            use_model_dection,
            urlContentToDataUri,

        }
    },

    methods: {
        change({ coordinates, canvas }) {
            console.log(coordinates, canvas);

        },

        getCrop() {
            // 剪裁當前圖片並檢視


            const cropperCanvas = this.$refs.cropper.getResult().canvas;  // 獲得剪裁結果
            const resultCanvas = this.$refs.resultCanvas  // 獲取 目標 canvas
            // 將裁剪結果繪製到目標 canvas
            const ctx = resultCanvas.getContext("2d");

            console.log('繪製的畫布大小:', cropperCanvas.width, cropperCanvas.height)
            // 設定剪裁的相關影像大小
            resultCanvas.width = cropperCanvas.width;
            resultCanvas.height = cropperCanvas.height;

            // 計算目標縮放比例
            // const getScale = Math.min(targetWidthShow.value / resultCanvas.width, targetWidthShow.value / resultCanvas.height)
            const getScale = Math.min(this.test_size / resultCanvas.width, this.test_size / resultCanvas.height)


            ctx.scale(getScale, getScale);  // 可以指定比例進行縮放  用來顯示
            console.log('縮放之後的圖片大小比例', resultCanvas.width, resultCanvas.height)
            ctx.drawImage(cropperCanvas, 0, 0);  // 繪製剪裁結果

            // console.log('image', image)
            // console.log('coordinates', coordinates)
            // console.log('visibleArea', visibleArea)
            // console.log('canvas', canvas)
        },
        handleAllCanvases() {
            // 一次剪裁按鈕啟動

            console.log('查看當前的 ref list:', this.new_origin)
            // 從原本的 canvas 列


            this.origin_croppers.forEach((canvas_item, index) => {

                this.$nextTick(() => {
                    const get_canvas = this.$refs[`myCanvas_${index}`][0].getResult().canvas // 原始圖像
                    const get_result_canvas = this.$refs[`towardCanvas_${index}`][0]


                    console.log('畫布剪裁大小:', get_canvas.width, get_canvas.height)

                    // add: 新增長短邊評估、 藉以以最小比例進行圖片縮放
                    const small_ = Math.max(get_canvas.width, get_canvas.height)
                    console.log('原圖片的長寬:', get_canvas.width, get_canvas.height)
                    const new_scale = this.new_test_size / small_     // 獲得比例
                    console.log('圖片縮放比例:', new_scale)



                    // 對剪裁的圖片進行縮放
                    const ctx = get_result_canvas.getContext("2d");
                    get_result_canvas.width = get_canvas.width * new_scale
                    get_result_canvas.height = get_canvas.height * new_scale



                    console.log('等比縮小前，畫布的大小:', get_result_canvas.width, get_result_canvas.height)
                    ctx.scale(new_scale, new_scale);  // 可以指定比例進行縮放  用來顯示
                    console.log('等比縮小後，畫布的大小:', get_result_canvas.width, get_result_canvas.height)
                    // ctx.drawImage(get_canvas, 0, 0);  // 繪製剪裁結果
                    // ctx.drawImage(get_canvas, 0, 0,get_canvas.width*new_scale,get_canvas.height*new_scale,0,0,get_canvas.width,get_canvas.height);  // 繪製剪裁結果
                    ctx.drawImage(get_canvas, 0, 0, get_canvas.width, get_canvas.height)
                })


            });
        },
        changeMedia(media) {

            // this.dataList = []

            this.media = media

        },

        async model_detect_go() {
            console.log('觸發模型判斷按鈕')

            let get_len = this.media.length

            this.origin_croppers = Array.from({ length: get_len }, (_, index) => `myCanvas_${index}`);
            this.result_croppers = Array.from({ length: get_len }, (_, index) => `towardCanvas_${index}`);
            console.log('創建對應的 target canvas list:', this.origin_croppers.length)
            // define resultCanvas with index
            console.log('資料產生異動:', this.use_model_dection)

            await nextTick(); // 很重要的等待異步執行完畢 否則會抱錯

            this.get_list_bs64()
        }
        ,
        async get_list_bs64() {

            console.log('當前的 origin list 數量:', this.origin_croppers)
            this.dataList = [];

            const gogo = async () => {
                this.dataList = [];

                const promises = [];
                this.origin_croppers.forEach((item, index) => {
                    // const get_blobURL = this.$refs[`myCanvas_${index}`][0].src; // 獲得 blob URL
                    const get_blobURL = this.$refs[`myCanvas_${index}`][0].src; // 獲得 blob URL
                    const get_bs64 = this.urlContentToDataUri(get_blobURL);
                    promises.push(
                        get_bs64.then((res) => {
                            this.dataList.push({
                                'index':index, 'bs64':res.slice(res.indexOf(',') + 1)
                            }); // 提取 Base64 部分
                        })
                    );
                });

                // 等待所有 Promise 完成
                return Promise.all(promises).then(() => {
                    console.log('查看 datalist list:', this.dataList.length);
                });
            };
            // await Promise.all()


            // 調用 gogo 函數
            gogo().then(() => {
                // console.log('最後紀錄的 datalist:', dataList.length)
                // console.log('res goog:', this.dataList)
                axios.post("http://localhost:8081/api/model_detect_th",
                    { 'images': this.dataList },
                    { headers: { 'Content-Type': 'application/json' } }
                ).then((result) => {
                    // result = Object.values(result)
                    // console.log('獲得的標點結果來自 post:', result.data)
                    console.log('獲得的標點結果來自 post:', typeof result.data)

                    this.origin_croppers.forEach((item, r_index) => {
                        const r_item = result.data[r_index]
                        this.$refs[`myCanvas_${r_index}`][0].setCoordinates({
                            // x1 y1 x2 y2
                            width: r_item[2] - r_item[0],
                            height: r_item[3] - r_item[1],
                            left: r_item[0],
                            top: r_item[1],
                        })
                    })
                }).catch(error => {
                    // 處理錯誤
                    console.error(error);
                })
            })


        }

        ,
        unified_resize() {
            this.media.forEach((canva, index) => {
                this.$refs[`myCanvas_${index}`][0].setCoordinates({
                    width: this.new_test_size,
                    height: 1000,
                    left: 102,
                    top: 74

                })
            })
        },
        package_download() {
            // btn event: 將資料打包並且自動下載

            const zip = new JSZip()
            this.origin_croppers.forEach((item, index) => {
                // const get_canvas = this.$refs[`myCanvas_${index}`][0].getResult().canvas
                const get_canvas = this.$refs[`towardCanvas_${index}`][0]
                const imageData = get_canvas.toDataURL('image/png')
                const b64 = imageData.slice(imageData.indexOf(',') + 1);
                zip.file(`image_${index}.png`, b64, { base64: true });
            })


            // 產生一個類似連結的功能 並且 download
            zip.generateAsync({ type: "blob" })
                .then(content => {
                    // 生成一個 a 標籤
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(content);
                    link.download = 'my_images.zip';
                    link.click();
                });
        },
    }
};

</script>


<style>
.show_result {
    width: 500px;
}


.grid-container {
    /* 網格排列，必須要檢查再 for 迴圈以外 */
    border: 2px dotted #708090;
    /* max-width: 1200px; */
    width: 1000px;
    height: auto;
    display: grid;
    grid-template-columns: repeat(3, minmax(300px, 300px));
    /* grid-template-rows: repeat(auto-fill,minmax(300px,300px)); */
    /* grid-template-rows: repeat(auto-fill, minmax(100px,auto)); */
    gap: 10px;
    /* 間距 */
    margin: 10px;
    padding: 15px;
    /* 容器內間距 */
}

.btn {
    margin-left: 5px;
    margin-top: 5px;
}
</style>