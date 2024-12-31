import base64
import requests
from datetime import datetime

def upload_to_github(image_data):
    repo_name = "YOUR_REPO_NAME"  # 替換為你的Repository名稱
    token = "YOUR_GITHUB_TOKEN" # 替換為你的 GitHub 存取權杖
    filename = "photo.jpg" 

    # 生成唯一的圖片路徑
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"images/{timestamp}_{filename}"

    encoded_image = base64.b64encode(image_data).decode()

    url = f"https://api.github.com/repos/{repo_name}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Upload {filename}",
        "content": encoded_image
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 201:
        # 獲取上傳圖片的原始 URL
        raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/{path}"
        return raw_url
    else:
        raise Exception(f"Failed to upload image to GitHub. Status code: {response.status_code}")


if __name__ == "__main__":
    filename = "photo.jpg" 
    # 打開圖片檔案並上傳
    with open(filename, "rb") as image_file:
        image_data = image_file.read()  
        raw_url = upload_to_github(image_data)
        print(f"圖片已成功上傳，網址為：{raw_url}")
