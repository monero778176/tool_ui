from ast import main
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
import cv2
import base64
import numpy as np


# model_path = hf_hub_download(
#     repo_id = "pitangent-ds/YOLOv8-human-detection-thermal",
#     filename = "model.pt"
# )

model_path = './models/yolov8n.pt'

print(f'模型下載位置:{model_path}')
model = YOLO(model_path)


def inference(image_path):
    if isinstance(image_path,str):
        image_path = cv2.imread(image_path)
    model_output = model(image_path, conf=0.45, verbose=False)
    detections = Detections.from_ultralytics(model_output[0])
    return image_path,detections


def inferenceBystring(image_path):
    if isinstance(image_path,str):
        cv_image = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
    model_output = model(image_path, conf=0.6, verbose=False)
    detections = Detections.from_ultralytics(model_output[0])
    return cv_image,detections

def draw_rect(cv_image,detection:Detections):

    # print(f'偵測結果:{detection.xyxy}')
    xyxy=detection.xyxy[0].astype('int32')
    print(f'只偵測檢查一個:{xyxy}')
    x1,y1 = xyxy[:2]
    x2,y2 = xyxy[2:]
    draw_img = cv2.rectangle(cv_image,(x1,y1),(x2,y2),(0,255,0) ,2)

    return draw_img


def base64_to_img(base64_str):
    byte_data = base64.b64decode(base64_str)
    img_array = np.asarray(bytearray(byte_data),dtype="uint8")
    img_array = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
    # img_array = cv2.cvtColor(img_array,cv2.COLOR_BGR2RGB)

    return img_array



# 獨語 blob 檔案
import requests    
class BlobReader:
    def read_blob(self,blob_path:str)-> bytes:
        response = requests.get(blob_path)
        if response.status_code==200:
            blob_data = response.content
            return blob_data
        return None


# image_path=r"C:\Users\syaun\OneDrive\Pictures\Saved Pictures\GOOyf28bQAA-fTn.jpg"
# img, detect_result = inference(image_path)

# draw_img = draw_rect(img,detect_result)

# cv2.imshow('result',draw_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(f'偵測結果 :{(detect_result)}')



if __name__=='__main__':
    import os
    import glob


    all_glob = glob.glob('../test_img/*')
    target_dir = '../save_img/'


    for src_path in all_glob:
        src_path = src_path.replace('\\','/')
        # print(f'輸入圖片的 src 內容:{src_path}')
        filename = src_path.split('/')[-1]
        img,detection = inference(src_path)


        if detection.xyxy.size!=0:
        # print(f'圖片的type:{type(img)}')
        # print(f'圖片的內容:{img}')
            draw_result = draw_rect(img,detection)

        cv2.imwrite(target_dir+filename,img)


        
    # _,detection = inference(img)

    # print(f'偵測結果:{detection.xyxy}')

    # draw_result = draw_rect(img,detection)
    # cv2.imshow('test',draw_result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


