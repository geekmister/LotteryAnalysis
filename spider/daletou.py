import requests
import time

import utils.dbmanager as dbmanager
import utils.filemanager as filemanager
import logging

BASE_URL = f"https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo="
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
DB_MANAGER = dbmanager.DBManager()


def init_drawing():
    current_page = 0
    total_page = 1

    while current_page < total_page:
        time.sleep(2)

        current_page += 1

        response = requests.get(url=BASE_URL + str(current_page), headers=HEADERS)
        data = response.json()

        if data["errorCode"] != "0":
            print("Response Error: ", data["errorMessage"])
            break

        if total_page == 1:
            total_page = data["value"]["pages"]

        for item in data["value"]["list"]:
            write_data(item)


def append_drawing():
    latest_issue_number_in_database = DB_MANAGER.queryone(
        "select issue from t_bus_daletou order by issue desc limit 1")
    logging.info(
        f"latest_issue_number_in_database is: {latest_issue_number_in_database}")
    if latest_issue_number_in_database is None:
        logging.warning(
            "Database is empty, need to call init_drawing() first.")
        init_drawing()
        return

    current_page = 0
    total_page = 1

    while current_page < total_page:
        time.sleep(2)

        current_page += 1

        response = requests.get(url=BASE_URL + str(current_page), headers=HEADERS)
        data = response.json()

        if data["errorCode"] != "0":
            print("Response Error: ", data["errorMessage"])
            break

        if total_page == 1:
            total_page = data["value"]["pages"]

        for item in data["value"]["list"]:
            if int(item["lotteryDrawNum"]) > latest_issue_number_in_database[0]:
                write_data(item)
            else:
                return


def write_data(item):
    time.sleep(2)
    try:
        open_prize_numbers = item["lotteryDrawResult"].split(" ")
        sql = f"""
            insert into t_bus_daletou (
                issue,
                open_prize_date,
                oprfs_first_number,
                oprfs_second_number,
                oprfs_third_number,
                oprfs_fourth_number,
                oprfs_fifth_number,
                oprbs_first_number,
                oprbs_second_number,
                fp_base_betting_number,
                fp_base_prize_monney,
                fp_append_betting_number,
                fp_append_prize_monney,
                sp_base_betting_number,
                sp_base_prize_monney,
                sp_append_betting_number,
                sp_append_prize_monney,
                salary,
                prize_pool_monney
            ) values (
                {item['lotteryDrawNum']},
                '{item['lotteryDrawTime']}',
                {open_prize_numbers[0]},
                {open_prize_numbers[1]},
                {open_prize_numbers[2]},
                {open_prize_numbers[3]},
                {open_prize_numbers[4]},
                {open_prize_numbers[5]},
                {open_prize_numbers[6]},
                {item['prizeLevelList'][0]
                 ['stakeCount'].replace(',', '')},
                {item['prizeLevelList'][0]['stakeAmountFormat'].replace(
                     ',', '') if item['prizeLevelList'][0]['stakeAmountFormat'] != "" else 0},
                {item['prizeLevelList'][1]
                 ['stakeCount'].replace(',', '')},
                {item['prizeLevelList'][1]['stakeAmountFormat'].replace(
                     ',', '') if item['prizeLevelList'][1]['stakeAmountFormat'] != "" else 0},
                {item['prizeLevelList'][2]
                 ['stakeCount'].replace(',', '')},
                {item['prizeLevelList'][2]['stakeAmountFormat'].replace(
                     ',', '') if item['prizeLevelList'][2]['stakeAmountFormat'] != "" else 0},
                {item['prizeLevelList'][3]
                 ['stakeCount'].replace(',', '')},
                {item['prizeLevelList'][3]['stakeAmountFormat'].replace(
                     ',', '') if item['prizeLevelList'][3]['stakeAmountFormat'] != "" else 0},
                {item['totalSaleAmount'].replace(
                         ',', '') if item['totalSaleAmount'] != "" else 0},
                {item['poolBalanceAfterdraw'].replace(
                             ',', '') if item['poolBalanceAfterdraw'] != "" else 0}
            )"""
        logging.info(f"The sql is: {sql}")

        DB_MANAGER.insert(sql)
        filemanager.download_file(
            item["drawPdfUrl"], f"{filemanager.get_project_root() + '/open_prize_result/daletou/' + item['lotteryDrawNum']}.pdf")
    except KeyError as e:
        logging.error(f"数据缺失: {e}")
    except Exception as e:
        logging.error(f"插入数据失败: {e}")


if __name__ == "__main__":
    append_drawing()
