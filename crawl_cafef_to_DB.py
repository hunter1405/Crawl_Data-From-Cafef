from selenium import webdriver      # Thư viện giả lập trình duyệt Web - Chrome
from bs4 import BeautifulSoup       # Thư viện Parser html sau khi chạy Web
import psycopg2                     # Thư viện kết nối database POSTGRESQL
import yaml                         # Thư viện đọc file .yml
import time
from selenium.webdriver.chrome.options import Options   # Module Options để tùy chọn ẩn Web khi chạy


def extract():
    chrome_options = Options()    
    chrome_options.binary_location = "C:/Users/ACER/AppData/Local/Google/Chrome SxS/Application/chrome.exe"     # Ẩn Web - Chạy nền
    driver = webdriver.Chrome(chrome_options = chrome_options, executable_path='C:/Users/ACER/Downloads/crawl_cafef/chromedriver.exe') # Đường dẫn đến chromedriver (Đã set PATH)
    driver.get('https://liveboard.cafef.vn/')       # Load trang bản điện tử của Website cafef
    time.sleep(7)                   # Delay để load toàn bộ data

    soup = BeautifulSoup(driver.page_source, "lxml" )                   # Parser html từ trang web đã load
    contents = soup.find("tbody", {"role": "alert"}).find_all('tr')     # Tìm đến ô chứa bảng dữ liệu - Có được data dưới dạng Tree
    driver.quit()                   # Đóng website và trả về dữ liệu cần thiết
    return contents


def transform(contents):
    '''Hàm chuyển đổi dữ liệu dạng Tree từ hàm extract() và trả về dưới dạng tuple để dễ load vào database'''
    tp = ()
    for content in contents:
        item = content.find_all('td')
        stock = ((item[0].text, item[1].text, item[2].text, item[3].text,\
             item[4].text, item[5].text, item[6].text, item[7].text, \
                 item[8].text, item[9].text, item[10].text, item[11].text,\
                      item[12].text, item[13].text, item[14].text, \
                          item[15].text, item[16].text, item[17].text, \
                              item[18].text, item[19].text, item[21].text, \
                                  item[22].text, item[23].text),)
        tp += stock
    return tp


def load(data):
    '''Hàm load() load dữ liệu đã chuyển đổi vào database PostgreSQL'''

    with open(r'connect_infor.yml') as file:    # Mở file connect_infor.yml để lấy thông tin kết nối tới database.
        connect_infor = yaml.full_load(file) 
    
    conn = psycopg2.connect(
        host = connect_infor["host_name"],
        database = connect_infor["database"],
        user = connect_infor["user_name"],
        password = connect_infor["password"],
        port = connect_infor["port"],
        connect_timeout = 3
    )

    cur = conn.cursor()
    for eco in data:
        query = f"""
        INSERT INTO cafef_hose VALUES {eco};"""
        cur.execute(query=query)
    
    conn.commit()
    conn.close()

if __name__=='__main__':
    contents = extract()
    data = transform(contents)
    load(data)



# https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver