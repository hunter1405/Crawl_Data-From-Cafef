# Các bước cài đặt môi trường và thư viện để chạy demo code crawl dữ liệu chứng khoán từ web cafef.vn

**Bước 1**: Tạo một thư mục ảo để cài đặt các thư viện cần thiết. Các thư viện được cài trong thư mục này
sẽ hoàn độc lập so với các thư viện đã cài trên máy.

- Thực hiện lệnh với máy tính windows (cửa sổ Terminal đứng tại thư mục crawl_cafef):
    `python -m venv venv_name` (venv_name là tên thư mục ảo)
- Lúc này máy tính sẽ tạo ra một thư mục, ví dụ: `D:\Code\software_project\gitlab.com\ecodata2m\ecodata2m\training\nguyenquocvuong@gmail.com\crawl_cafef\venv_name`

- Kích hoạt môi trường ảo này bằng lệnh:
    `venv_name/Scripts/Activate`
- Thoát khỏi môi trường này bằng lệnh deactivate

Tham khảo thêm: https://docs.python.org/3/library/venv.html

**Bước 2**: cài đặt thư viện, webdriver (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

 - Webdriver: Download ChromeDriver (https://chromedriver.chromium.org/home), giải nén và đặt file tại thư mục `crawl_cafef` (nếu đặt ở thư mục khác thì Set đường dẫn trong PATH)
 - Các thư viện cần thiết: selenium, bs4, psycopg2, yaml, lxml,..
 - Trước tiên, upgrade python pip lên bản mới nhất: 
	`python -m pip install --user --upgrade pip`
 - Cài thư viện đã được list trong file requirements.txt
	`python -m pip install -r requirements.txt`

**Bước 3**: Sau khi cài đặt xong thư viện, thì có thể chạy code bằng lệnh `python crawl_cafef_to_DB.py`
Lưu ý:
 - Đổi lại thông tin kết nối Database trong file `connect_infor.yml` theo đúng cấu hình trên máy khi cài đặt Postgresl.
 - Dự án dùng Postgresql Database nên cần cài đặt phần mềm này và thiết lập port là 5439 để không xung đột sau này khi chạy Prefect ETL (yêu cầu PORT mặc định 5432).
Có thể đổi PORT mặc định từ 5432 thành 5439 bằng cách sửa lại Port trong file postgresql.conf, sau đó reset lại Postgresql.
Search Services trong mục tìm kiếm của Windows, sau đó tìm Postgresl và Restart.
Hoặc tham khảo cách cài đặt Postgresql bằng file Binary của anh Thạch tại (https://thachln.github.io/ebooks/cham-toi-GO-trong-10-ngay/chia-se/PostgreSQL_20210807.pdf?fbclid=IwAR2AcdHIHOLK04BO3vy52naOI-2Gl1Wt0U-7mR8bwkc-04GigAYG373w58I)
