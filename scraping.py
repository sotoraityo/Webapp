# -*- coding: utf-8 -*-
import os
import datetime
import csv
import urllib.request
from bs4 import BeautifulSoup

def str2float(weather_data):
    try:
        return float(weather_data)
    except:
        return 0

def scraping(url, date):
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,"html.parser")
    trs = soup.find("table", { "class" : "data2_s" })

    data_list = []
    data_list_per_hour = []

    # table の中身を取得
    for tr in trs.findAll('tr')[2:]:
        tds = tr.findAll('td')

        if tds[1].string == None:
            break;

        data_list.append(date.date())
        data_list.append(tds[0].string)
        data_list.append(str2float(tds[1].string))
        data_list.append(str2float(tds[2].string))
        data_list.append(str2float(tds[3].string))
        data_list.append(str2float(tds[4].string))
        data_list.append(str2float(tds[5].string))
        data_list.append(str2float(tds[6].string))
        data_list.append(str2float(tds[7].string))
        data_list.append(str2float(tds[8].string))
        data_list.append(str2float(tds[9].string))
        data_list.append(str2float(tds[10].string))
        data_list.append(str2float(tds[11].string))
        data_list.append(str2float(tds[12].string))
        data_list.append(str2float(tds[13].string))

        data_list_per_hour.append(data_list)

        data_list = []

    return data_list_per_hour

def create_csv(start_date):
    # データ取得開始・終了日
    #start_date = datetime.straptime(sdate,'%Y-%m-%d')
    #start_date=datetime.strptime(sdate,'%Y-%m-%d')
    #end_date   = start_date+ datetime.timedelta(1)

    # CSV の列
    fields = ["年月日", "時間", "気圧（現地）", "気圧（海面）",
              "降水量", "気温", "露点湿度", "蒸気圧", "湿度",
              "風速", "風向", "日照時間", "全天日射量", "降雪", "積雪"]
    
    # CSV 出力先ディレクトリ
    output_dir = r"./static/csv"

    # 出力ファイル名
    output_file = "weather"+start_date.strftime("%Y-%m-%d")+".csv"

    with open(os.path.join(output_dir, output_file), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)

        date = start_date
        while date != start_date + datetime.timedelta(1):

            # 対象url
            url = "http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=52&block_no=47632&year=%d&month=%d&day=%d&view="%(date.year, date.month, date.day)

            data_per_day = scraping(url, date)

            for dpd in data_per_day:
                writer.writerow(dpd)

            date += datetime.timedelta(1)

if __name__ == '__main__':
    create_csv()