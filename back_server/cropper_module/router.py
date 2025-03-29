from fastapi import APIRouter
from cropper_module.models import *
from fastapi import File, UploadFile,HTTPException
import time
from cropper_module.test_model import *


'''多工並行處理'''
import threading
import queue

router = APIRouter()



@router.post("/upload")
async def get_upload_data(image: UploadFile = File(...)):
    '''上傳用以回傳給前端顯示圖片使用'''
    try:
        # if image is None:
        #     raise HTTPException(status_code=400, detail="No file uploaded")
        # content = await image.read()
        # return {"filename": image.filename, "size": len(content)}
        print(f'上傳的 file type:{type(image)}')
        return {'name':image.filename}

    except Exception as e:
        print(f'500 error code')
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/cropper/model_detect")
async def model_detect_object(ig_list:ImageRequest):

    start_t= time.time()
    get_list = ig_list.images  # 從前端獲得到所有資料的 list
    print(f'接收到的list 長度:{len(get_list)}')

    # for imageURL in images:
    #     cv_img = cv2.imread(imageURL,3)
    #     print(f'圖片大小:{cv_img.shape}')
    # reader = BlobReader()  # 創建讀取 blob 器
    # cv2_img = cv2.imread(images)
    xyxy_list = []
    for image in get_list:
        # 将 base64 数据解码并保存
        # print(f'從前端接收到的string:{image}')

        # blob_data = reader.read_blob(image)
        # if blob_data is not None:
        #     print(f'成功讀取到 blob 數據')
        # else:
        #     print(f'讀取到 blob 數據失敗')
        array_img = base64_to_img(image)  # 將 base64 轉換成 np
        array_img = cv2.cvtColor(array_img,cv2.COLOR_RGB2BGR)
        print(f'解碼獲得的np:',type(array_img))
        print(f'解碼獲得的np:',(array_img.shape))
        _,detection = inference(array_img)


        print(f'打印:{detection.xyxy}')
        print(f'對應 xyxy 的屬性:{type (detection.xyxy)}')
        
        x1,y1,x2,y2 = None,None,None,None
        if (detection.xyxy.size!=0):
            x1,y1,x2,y2 = detection.xyxy[0].astype('int32').tolist()
            print(f'偵測成功回傳 xyxy:',x1,y1,x2,y2)

        else:
            print(f'模型沒有判斷')

        xyxy_list.append([x1,y1,x2,y2])

    print(f'模型偵測資料長度:{len(get_list)} , 處理完的資料長度:{len(xyxy_list)}')
    end_t= time.time()

    print(f'多緒的處理時間:{end_t-start_t}')

    return xyxy_list


target_dir = '../save_img2/'

@router.post("/model_detect_th")
async def model_detect_object_th(ig_list:ImageRequestwithID):
    '''使用 multi-thread 處理 model detection 的任務'''

    print(f'執行多緒的 function')
    start_t = time.time()
    task_queue = queue.Queue()
    result_queue = queue.Queue()  # 具優先順序的 queue

    
    get_list = ig_list.images  # 從前端獲得到所有資料的 list

    # 接收前端資料 加入到 Q 使用 worker
    for idx,item in enumerate(get_list):
        idd = item.index
        itt = item.bs64
        # cv2.cvtColor(array_img,cv2.COLOR_RGB2BGR)
        # cv2.imwrite(target_dir+f'origin_{idd}.jpg',array_img)
        task_queue.put([idd,itt])
    print(f'接收到的list 長度:{len(get_list)}')

    # for imageURL in images:
    #     cv_img = cv2.imread(imageURL,3)
    #     print(f'圖片大小:{cv_img.shape}')
    # reader = BlobReader()  # 創建讀取 blob 器
    # cv2_img = cv2.imread(images)
    
    '''創建 threads'''
    threads = []
    for _ in range(3):
        t = threading.Thread(target=worker(task_queue,result_queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    sorted_results = []  # final sort of Q by result
    while not result_queue.empty():
        sorted_results.append(result_queue.get())
    sorted_results.sort(key=lambda x: x[0])
    end_t = time.time()

    sort_list = []
    for item in sorted_results:
        idx,i_item = item
        sort_list.append(i_item)
        print(f'回傳的按鈕:{i_item}, 執行 index:{idx}')

    print(f'多緒的處理時間:{end_t-start_t}')

    return sort_list


def worker(task_que:queue.Queue,result_que:queue.Queue):
    '''定義多緒的工作內容'''
    while not task_que.empty():
        idx, image = task_que.get() # get front item from Q
        image = base64_to_img(image)  # 將 base64 轉換成 np
        # object detect processing
        _,detection = inference(image)

        # 判斷 model detection 的結果
        if (detection.xyxy.size!=0):
            xyxy = detection.xyxy[0].astype('int32').tolist()
            x1,y1 = xyxy[:2]
            x2,y2 = xyxy[2:]

            # draw_img = cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0) ,2)

            # cv2.imwrite(target_dir+f'/img_{idx}.jpg',draw_img)
            
            print(f'偵測成功回傳 xyxy:',x1,y1,x2,y2)

            result_que.put((idx,[x1,y1,x2,y2]))   # save detection result
        else:
            print(f'沒有被檢測到的詳情資訊:{detection.xyxy} 其所對應到的 index:{idx}')
            result_que.put((idx,[0,0,512,512]))   # save detection result

        task_que.task_done()
