from selenium import webdriver
from datetime import date, timedelta
import sys
import psycopg2
import yaml
from config import days_off

holidays = days_off


def date_check_and_format_date(current_day):

    while current_day.weekday() > 4 or (str(current_day.day) + '/' + str(current_day.month)) in holidays[str(current_day.year)]:
        current_day += timedelta(days=1)
 
    if current_day.day < 10:
        day = '0' + str(current_day.day)
    else:
        day = str(current_day.day)
    if current_day.month < 10:
        month = '0' + str(current_day.month)
    else:
        month = str(current_day.month)
    formated_date = day + '/' + month + '/' + str(current_day.year)

    return current_day, formated_date       


def main(begin_day, ending_day):
    """Crawling data from cafef.vn webpage, loading data each day into database."""

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')                         
    options.add_argument('--ignore-ssl-errors')                                
    options.add_experimental_option('excludeSwitches', ['enable-logging'])      
    driver = webdriver.Chrome(options=options)

    date_miss = []
    while begin_day < ending_day:
        
        begin_day, formated_date = date_check_and_format_date(begin_day)
        print("Crawling transactions data on " + formated_date + ".")

        url = f"https://s.cafef.vn/Lich-su-giao-dich-{stocks_code}-6.chn?date={formated_date}"
        driver.get(url=url)

        all_data = []
        try:
            table = driver.find_element_by_id("tblData")
            data = table.text
            all_data = data.split("\n")            
            print("Crawling success!")

        except:
            date_miss.append(formated_date)           
            print("No transaction on weekend and holiday!")
        
        for oneday in all_data:
            line = oneday.split(" ")
            try:
                tp = (stocks_code, formated_date, line[0], line[1], line[2], line[3], line[4], line[5], line[6])
            except IndexError:
                print(formated_date)
                date_miss.append(formated_date)
                break
            query = f"INSERT INTO transaction VALUES {tp}"
            cur.execute(query=query)
        conn.commit()
        print("Loading data successfully!")        

        begin_day += timedelta(days=1)

    driver.quit()
    # print(date_miss)
    f = open("date_missed_data.txt", "a")
    #f.write("Missing data on days:")
    for date in date_miss:
        f.write("- " + date + "\n")
    f.close()

if __name__=="__main__":
    stocks_code = sys.argv[1]
    begin_day = date.fromisoformat(sys.argv[2])

    try:
        ending_day = date.fromisoformat(sys.argv[3])
    except:
        ending_day = date.today()
    with open(r'connect_infor.yml') as file:
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

    main(begin_day,ending_day)

    conn.close()


# Ignore ERROR:ssl_client_socket_impl.cc - https://github.com/Richard-Barrett/ITDataServicesInfra/issues/30
# Selenium summary: https://www.fatalerrors.org/a/a-complete-collection-of-commonly-used-api-s-for-selenium.html