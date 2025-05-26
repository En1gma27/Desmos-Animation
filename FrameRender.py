import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, 'FrameInput')
OUTPUT_DIR = os.path.join(BASE_DIR, 'FrameOutput')
BASE_URL = 'http://127.0.0.1:5000/frame/'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

frames = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.png')])

chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ẩn, không hiện cửa sổ trình duyệt
chrome_options.add_argument("--window-size=1920,1080")  # Đúng kích thước đồ thị

driver = webdriver.Chrome(options=chrome_options)

for frame in frames:
    url = BASE_URL + frame
    print(f"Đang render {frame} ...")
    driver.get(url)
    time.sleep(2)  # Chờ Desmos render xong, có thể tăng nếu mạng/chạy chậm
    # Chụp lại vùng đồ thị
    calculator = driver.find_element("id", "calculator")
    calculator.screenshot(os.path.join(OUTPUT_DIR, frame))
    print(f"Đã lưu {frame}")

driver.quit()
print("Đã chụp xong tất cả frame!")

# Ghép các frame trong thư mục FrameOutput thành video 
images = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
if images:
    first_frame = cv2.imread(os.path.join(OUTPUT_DIR, images[0]))
    height, width, _ = first_frame.shape
    video = cv2.VideoWriter(os.path.join(OUTPUT_DIR, 'output_video.avi'), cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    for img_name in images:
        img = cv2.imread(os.path.join(OUTPUT_DIR, img_name))
        video.write(img)
    video.release()
    print('Video created successfully!')
else:
    print('No images to create video.')
