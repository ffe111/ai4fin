import requests
from bs4 import BeautifulSoup
import js2py


def stock_price(symbol):
    try:
        url = "https://www.set.or.th/th/market/product/stock/quote/{name:s}/price"
        res = requests.get(url.format(name=symbol))
        res.encoding = "utf-8"

        if res.status_code == 200:
            print("Successful\n")
            soup = BeautifulSoup(res.text, 'html.parser')
            script_list = soup.find_all('script')
            # for index ,i in enumerate(script_list):
            #    print("\n", index)
            #    print(i)
            js2py_DataValue = js2py.eval_js(script_list[2].text)
            DataValue = js2py_DataValue['state']['quote']['info'].to_dict()
            # print(DataValue)
            #   print(f"ตลาด: {DataValue['marketName']}  หุ้น: {symbol}")
            #   print(f"TH {DataValue['nameEN']}\nEN {DataValue['nameTH']}")
            #   print("เฉลี่ย: ", DataValue['average'])
            #   print("สูงสุด: ", DataValue['high'])
            #   print("ต่ำสุด: ", DataValue['low'])
            #   print("เปิด: ", DataValue['open'])
            #   print("ล่าสุด: ", DataValue['last'])
            return DataValue
        elif res.status_code == 404:
            print("Error 404 page not found\n")
        else:
            print("Not both 200 and 404\n")
    except Exception as xcpn:
        print(xcpn)


if __name__ == "__main__":
    symbol = input("Enter symbol name: ")
    print(end="  ")
    stock_price(symbol)
"""
{
   "aomValue":536766,
   "aomVolume":1041800,
   "average":0.51523,
   "bids":[
      {
         "price":"0.51",
         "volume":128100
      }
   ],
   "ceiling":0.67,
   "change":-0.01,
   "dividendYield":"None",
   "exercisePrice":"None",
   "exerciseRatio":"1 : 1",
   "floor":0.37,
   "high":0.53,
   "high52Weeks":0.67,
   "inav":"None",
   "industryName":"PROPCON",
   "isNPG":false,
   "last":0.51,
   "lastTradingDate":"None",
   "low":0.51,
   "low52Weeks":0.36,
   "marketCap":708145314.76,
   "marketDateTime":"2024-03-05T14:01:22.450587891+07:00",
   "marketName":"SET",
   "marketStatus":"Pre-Open2",
   "maturityDate":"None",
   "nameEN":"POWER LINE ENGINEERING PUBLIC COMPANY LIMITED",
   "nameTH":"บริษัท เพาเวอร์ไลน์ เอ็นจิเนียริ่ง จำกัด (มหาชน)",
   "nvdrNetVolume":-182300,
   "offers":[
      {
         "price":"ATO",
         "volume":1000
      }
   ],
   "open":0.52,
   "par":1,
   "pbRatio":0.3,
   "percentChange":-1.923077,
   "prior":0.52,
   "sectorName":"CONS",
   "securityType":"S",
   "sign":"",
   "symbol":"PLE",
   "tickSize":0.01,
   "totalValue":536767.94,
   "totalVolume":1041803,
   "trValue":"None",
   "trVolume":"None",
   "underlying":""
}
"""
