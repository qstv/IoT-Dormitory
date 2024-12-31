from picamera import PiCamera
import base64
import requests
from get_image_url import upload_to_github
from send_to_discord import send_message



def take_photo(file_path='photo.jpg', resolution=(1024, 768)):
    """
    拍攝一張照片並返回照片路徑
    :param file_path: 儲存照片的檔案路徑 (預設為 'photo.jpg')
    :param resolution: 照片的解析度 (預設為 1024x768)
    :return: 照片的檔案路徑
    """
    camera = PiCamera()
    camera.rotation = 180 # 旋轉
    try:
        # 設置相機解析度
        camera.resolution = resolution
        # 拍攝照片
        camera.capture(file_path)
        print(f"照片已保存至: {file_path}")
    finally:
        # 關閉相機
        camera.close()
    
    return file_path


if __name__ == "__main__":
    take_photo()
    
    