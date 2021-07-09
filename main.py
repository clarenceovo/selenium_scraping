from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule
pd.set_option('display.max_columns', None)


def get_transaction_fb():
    try:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("debuggerAddress", "127.0.0.1:9888")
        chromeOptions.add_argument(r"")
        chrome_driver = "C:\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chromeOptions)
        driver.get("https://pro.nansen.ai/smart-money?segment=Flash%20Boy")
        time.sleep(30) #it takes so long to load the fucking webpage lol
        data_collection_dict = {}
        #html = driver.execute_script("return document.documentElement.outerHTML;")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result_list = []
        body_extract = soup.find('article').find_all()
        for item in body_extract:
            column = item.find_all("div")
            for div in column:
                if div and div.get("data-idx"):
                    if int(div.get("data-idx")) not in data_collection_dict.keys():
                        data_collection_dict[int(div.get("data-idx"))] = []
                    tmp = []
                    tmp.append(int(div.get("data-idx")))
                    for data in div.find_all(["div","a"]):
                        if (data.get("data-column")):
                            #print(data.get('data-column'))
                            #print(data.get_text())
                            if (int(data.get('data-column'))  in [2,5]):
                                if (data.get("href")):
                                    tmp.append(data.get_text())
                                    url = data.get("href")

                                    tmp.append(url.split('=')[1])
                                else:
                                    tmp.append(data.get_text())
                                    tmp.append(0)
                            else:
                                tmp.append(data.get_text())
                            #if (int(data.get("data-idx")) is in [])
                    tmp.append(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
                    result_list.append(tmp)

        ret_df = pd.DataFrame(result_list,columns=['ID','Dex','Time','Taker','Taker Address','Taker Amount','Taker Token','Maker','Maker Address','Maker Amount','Maker Token','Tx','Create TS'])

        ret_df.drop_duplicates(subset="ID", inplace=True)
        ret_df.sort_values("ID",ascending=True, inplace=True)
        ret_df.to_csv(r"G:\Shared drives\Trading\Nansen Data\result_flashbot.csv",header=False,index=False,mode='a')
        print("Finished")
    except Exception as e:
        print(f"Error:{e}")


def get_transaction_fund():
    try:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("debuggerAddress", "127.0.0.1:9888")
        chromeOptions.add_argument(r"")
        chrome_driver = "C:\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chromeOptions)
        driver.get("https://pro.nansen.ai/smart-money?segment=Fund")
        time.sleep(30) #it takes so long to load the fucking webpage lol
        data_collection_dict = {}
        #html = driver.execute_script("return document.documentElement.outerHTML;")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result_list = []
        body_extract = soup.find('article').find_all()
        for item in body_extract:
            column = item.find_all("div")
            for div in column:
                if div and div.get("data-idx"):
                    if int(div.get("data-idx")) not in data_collection_dict.keys():
                        data_collection_dict[int(div.get("data-idx"))] = []
                    tmp = []
                    tmp.append(int(div.get("data-idx")))
                    for data in div.find_all(["div","a"]):
                        if (data.get("data-column")):
                            #print(data.get('data-column'))
                            #print(data.get_text())
                            if (int(data.get('data-column'))  in [2,5]):
                                if (data.get("href")):
                                    tmp.append(data.get_text())
                                    url = data.get("href")
                                    tmp.append(url.split('=')[1])
                                else:
                                    tmp.append(data.get_text())
                                    tmp.append(0)
                            else:
                                tmp.append(data.get_text())
                            #if (int(data.get("data-idx")) is in [])
                    tmp.append(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
                    result_list.append(tmp)

        ret_df = pd.DataFrame(result_list,columns=['ID','Dex','Time','Taker','Taker Address','Taker Amount','Taker Token','Maker','Maker Address','Maker Amount','Maker Token','Tx','Create TS'])

        ret_df.drop_duplicates(subset="ID", inplace=True)
        ret_df.sort_values("ID",ascending=True, inplace=True)

        ret_df.to_csv(r"G:\Shared drives\Trading\Nansen Data\result_Fund.csv",header=False,index=False,mode='a')
        print("Finished")


    except Exception as e:
        print(f"Error:{e}")


def get_token_transfer():
    try:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("debuggerAddress", "127.0.0.1:9888")
        chromeOptions.add_argument(r"")
        chrome_driver = "C:\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chromeOptions)
        driver.get("https://pro.nansen.ai/smart-money")
        print("Calling API")
        time.sleep(15) #it takes so long to load the fucking webpage lol
        data_collection_dict = {}
        print("Finished")
        #html = driver.execute_script("return document.documentElement.outerHTML;")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result_list = []
        body_extract = soup.find('article',attrs={"id":"sm_tokens_txs_24"})
        target = body_extract.find_all("div")
        for item in target:
            #print(item.get_text())
            if item.get("data-idx"):
                tmp = item.find_all(["a","div"])

                for code in tmp:
                    if code.get("href"):
                        addr = code.get("href").split("=")
                        if len(addr)>1:
                            addr = addr[1]
                            if code.get_text() != addr:
                                result_list.append({"account":code.get_text(),"address":addr})
        df = pd.DataFrame(result_list)
        df.to_csv(r"G:\Shared drives\Trading\Nansen Data\token_transfer_tag.csv", header=False, index=False, mode='a')
    except Exception as e:
        print(f"Error:{e}")


if __name__ =='__main__':
    get_token_transfer()
    get_transaction_fb()
    get_transaction_fund()
    schedule.every(10).minutes.do(get_token_transfer)
    schedule.every(30).minutes.do(get_transaction_fb)
    schedule.every(30).minutes.do(get_transaction_fund)
    while True:
        try:
            schedule.run_pending()
        except:
            print("Error")
        time.sleep(10)
