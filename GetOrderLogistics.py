#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-

"""
************************************************************************************************************************
根据订单号获取订单信息
包括物流详情、订单的评价信息、订单状态等等
************************************************************************************************************************
"""

import requests, random, pymysql, re, json
from lxml import etree



class Get_order():
    def __init__(self, username, orderId):
        self.username = username

        self.orderId = orderId
        self.commentUrl = "https://rate.taobao.com/RateDetailBuyer.htm?parent_trade_id={}".format(self.orderId)
        self.tianmao_url = "https://trade.tmall.com/detail/orderDetail.htm?spm=a1z09.2.0.0.37a82e8dNYfgOp&bizOrderId={}".format(self.orderId)
        self.taobao_url = "https://trade.taobao.com/trade/detail/trade_order_detail.htm?biz_order_id={}".format(self.orderId)
        self.tradearchive_url = "https://tradearchive.taobao.com/trade/detail/trade_item_detail.htm?bizOrderId={}".format(self.orderId)


        self.taobao_con = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset='utf8'
        )

        self.taobao_cur = self.taobao_con.cursor()

        proxy_sql = "SELECT proxy FROM `proxy_table`"
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]

        select_sql = 'SELECT user_agent, cookie FROM cookie_table WHERE username="{}"'.format(self.username)

        try:
            self.taobao_cur.execute(select_sql)
        except Exception as e:
            print(e)

        ua_date = self.taobao_cur.fetchall()

        self.cookies = ua_date[0][1]
        self.ua = ua_date[0][0]


    def Get_logistics(self, logistics_url):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "detail.i56.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        logistics_json = requests.get(logistics_url, headers=headers, proxies=proxy)
        jsomDate = eval(str(logistics_json.text).replace('false', 'False').replace("true", "True"))
        try:
            expressageDict = {}
            expressageDict['mailNo'] = jsomDate['detailList'][0]['mailNo']
            expressageDict['cpName'] = jsomDate['detailList'][0]['cpName']

            expressage_list = []
            for logis_list in jsomDate['detailList'][0]['detail']:
                logis_dict = {}
                logis_dict['time'] = logis_list['time']
                logis_dict['desc'] = logis_list['desc']
                expressage_list.append(logis_dict)
            expressageDict['expressage'] = expressage_list
            return expressageDict
        except:
            return {}



    def taobao_logic(self, logistics_url):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "detail.i56.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        logistics_json = requests.get(logistics_url, headers=headers, proxies=proxy)
        jsomDate = eval(str(logistics_json.text).replace('false', 'False').replace("true", "True"))
        try:
            expressageDict = {}
            expressageDict['mailNo'] = jsomDate['detailList'][0]['mailNo']
            expressageDict['cpName'] = jsomDate['detailList'][0]['cpName']

            expressage_list = []
            for logis_list in jsomDate['detailList'][0]['detail']:
                logis_dict = {}
                logis_dict['time'] = logis_list['time']
                logis_dict['desc'] = logis_list['desc']
                expressage_list.append(logis_dict)

            expressageDict['expressage'] = expressage_list

            return expressageDict
        except:
            return {}



    def get_taobao_id(self, url):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "trade.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        reql_json = requests.get(url, headers=headers, proxies=proxy, allow_redirects=False)
        if reql_json.status_code == 200:
            a_json = str(re.findall("JSON.parse\('(.*?)'\);", reql_json.text, re.S)[0]).strip().replace('false', 'False').replace("true", "True").replace('\\"', '"').replace('\\\\"', '')
            json_date = eval(a_json)
            return json_date['baseSnapDO']['itemSnapDO']['itemId']

        if reql_json.status_code == 302:
            itemId = re.findall('id=(.*)', reql_json.headers['Location'])[0]
            return itemId




    def taobao_json(self):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "trade.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        params = {"biz_order_id": self.orderId}

        reql_json = requests.get(self.taobao_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)

        if reql_json.status_code == 200:
            a_json = str(re.findall("JSON.parse\('(.*?)'\);", reql_json.text, re.S)[0]).strip().replace('false', 'False').replace("true", "True").replace('\\"', '"').replace('\\\\"', '')
            json_date = eval(a_json)
            takegoodsaddress = str(json_date['deliveryInfo']['address']).split('，')
            takegoodsname = takegoodsaddress[0]
            phoneNum = takegoodsaddress[1]
            address = takegoodsaddress[2]
            if "asyncLogisticsUrl" in json_date['deliveryInfo']:
                expressageDict = self.taobao_logic(str("https:"+json_date['deliveryInfo']['asyncLogisticsUrl']).replace("\\", ''))
            else:
                expressageDict = {}

            detail_url = "https:" + str(json_date['mainOrder']['subOrders'][0]['itemInfo']['auctionUrl']).replace("\\", '')
            productPic = "https:" + str(json_date['mainOrder']['subOrders'][0]['itemInfo']['pic']).replace("\\", '')
            title = json_date['mainOrder']['subOrders'][0]['itemInfo']['title']
            itemIds = ''
            for i in json_date['mainOrder']['subOrders']:
                auctionUrl = "https:" + str(i['itemInfo']['auctionUrl']).replace("\\",  '')
                if "baoxian" not in auctionUrl:
                    itemIds = itemIds + str(self.get_taobao_id(auctionUrl)) + ','
            WangWang = json_date['mainOrder']['seller']['nick']

            price = json_date['mainOrder']['subOrders'][0]['priceInfo']
            trading_status = json_date['mainOrder']['statusInfo']['text'].replace("当前订单状态：", "").replace('，请查看页面下方物流信息了解宝贝寄送情况', '').replace("您已付款到支付宝，等待卖家发货；您可以通过阿里旺旺联系卖家确认发货时间", "买家已付款")

            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'], jsonDict['itemIds'], jsonDict['WangWang'],  = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status, itemIds[:-1], WangWang
            return jsonDict
        else:
            return False





    def tianmao_json(self):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "trade.tmall.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }
        params = {"bizOrderId": self.orderId}

        reql_json = requests.get(self.tianmao_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)
        if reql_json.status_code == 200:
            json_data = eval(str(re.findall("detailData = (.*?)</script>", reql_json.text, re.S)[0]).strip().replace('false', 'False').replace("true", "True"))
            takegoodsaddress = str(json_data['basic']['lists'][0]['content'][0]['text']).split(',')                                     #收货地址
            takegoodsname = takegoodsaddress[0]
            phoneNum = takegoodsaddress[1]
            address = takegoodsaddress[2]
            if "logistic" in json_data['orders']['list'][0]:
                expressageDict = self.Get_logistics("https:" + json_data['orders']['list'][0]['logistic']['content'][0]['url'])
            else:
                expressageDict = {}
            detail_url = "https:" + json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['itemUrl']
            productPic = "https:" + json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['pic']
            title = json_data['orders']['list'][0]['status'][0]['subOrders'][0]['itemInfo']['title']
            itemIds = json_data['ad']['salePromotion']['params']['itemIds']
            WangWang = re.findall("title=\'(.*?)\'", json_data['basic']['lists'][3]['content'][0]['text'], re.S)[0]
            price = json_data['orders']['list'][0]['status'][0]['subOrders'][0]['priceInfo'][0]['text']
            trading_status = json_data['orders']['list'][0]['status'][0]['statusInfo'][0]['text'].replace('，请查看页面下方物流信息了解宝贝寄送情况', '').replace("当前订单状态：", "")

            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'], jsonDict['itemIds'], jsonDict['WangWang'],  = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status, itemIds, WangWang
            return jsonDict
        else:
            return False




    def tradearchive_html(self):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "tradearchive.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }
        params = {"bizOrderId": self.orderId}

        reql_json = requests.get(self.tradearchive_url, headers=headers, params=params, proxies=proxy, allow_redirects=False)
        print(reql_json.status_code)
        print(reql_json.text)
        if reql_json.status_code == 200:
            html = etree.HTML(reql_json.text)
            takegoodsaddress = "".join(str(re.findall("收货地址：</td>(.*?)</tr>", reql_json.text, re.S)[0]).strip()).replace("<td>", "").replace("</td>", "").replace("\n\t\t\t\t\t\t\t\t\t\t\t", '').replace("\t\t\t\t\t\t", '').replace("\t\t\t\t\t\t", "").replace("\t\t\t\t\t\t", "").replace("\t\t\t\t\t\t\t\t\t\n", "").split("，")
            asdf = [i for i in takegoodsaddress if len(str(i).strip())>0]
            takegoodsname = asdf[0]
            phoneNum = asdf[1]
            address = asdf[2]
            expressageDict = {}
            detail_url = "https:" + html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[2]/div/span[1]/a//@href')[0]
            productPic = "https:" + html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[1]/div/a/img//@src')[0]
            title = html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[1]/div[2]/div/span[1]/a//text()')[0]
            itemIds = re.findall('p4p_itemIds = \"(.*?)\"', reql_json.text, re.S)[0]
            WangWang = html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[1]/tr[2]/td[1]/span[1]//text()')[0]
            price = html.xpath('//*[@id="J_TabView"]/div/div/div/table[1]/tbody[3]/tr[3]/td[7]//text()')[0].strip()
            trading_status = html.xpath('//*[@id="detail-panel"]/div[1]/div/div[1]/strong/span//text()')[0]

            jsonDict = {}
            jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'], jsonDict['itemIds'], jsonDict['WangWang']  = takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status, itemIds, WangWang
            return jsonDict
        else:
            return False




    def comment(self):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "rate.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua
        }

        reql_html = requests.get(self.commentUrl, headers = headers, proxies = proxy)

        commentstatus = re.findall("tb-rate-ico ico-(.*?)\"", reql_html.text, re.S)

        if len(commentstatus) == 0:
            msg = []
        else:
            msg, msgDice = [], {}
            if "good" == commentstatus[0]:
                msgDice['evaluateRank'] = "好评"
            elif "neutral" == commentstatus[0]:
                msgDice['evaluateRank'] = "中评"
            else:
                msgDice['evaluateRank'] = "差评"
            msgDice['commentText'] = re.findall("J_content\">(.*?)<", reql_html.text, re.S)[0]
            msg.append(msgDice)
        return msg



    def executesql(self, insertSql, expressageDict):
        try:
            self.taobao_cur.execute(insertSql)
            self.taobao_con.commit()
        except Exception as E:
            updateSql = """UPDATE order_logis_table SET expressageDict="{}" WHERE orderId='{}'""".format(expressageDict, self.orderId)
            try:
                self.taobao_cur.execute(updateSql)
                self.taobao_con.commit()
            except Exception as F:
                print("数据更改失败：", F)
        self.taobao_cur.close()
        self.taobao_con.close()




def main(username, orderId):
    getorder = Get_order(username, orderId)
    jsonDict = getorder.tianmao_json()
    if jsonDict is False:
        jsonDict = getorder.taobao_json()
        if jsonDict is False:
            jsonDict = getorder.tradearchive_html()
    if jsonDict:
        jsonDict["commentmsg"] = getorder.comment()
        insertSql = """INSERT INTO order_logis_table (username, orderId, takegoodsname, phoneNum, address, expressageDict, detail_url, productPic, title, price, trading_status, itemIds, WangWang, commentmsg) VALUES('{}', '{}', '{}', '{}', '{}', "{}", '{}', '{}', '{}', {}, '{}', '{}', '{}', "{}")""".format(username, orderId, jsonDict['takegoodsname'], jsonDict['phoneNum'], jsonDict['address'], jsonDict['expressageDict'], jsonDict['detail_url'], jsonDict['productPic'], jsonDict['title'], jsonDict['price'], jsonDict['trading_status'], jsonDict['itemIds'], jsonDict['WangWang'], str(jsonDict["commentmsg"]))
        getorder.executesql(insertSql, jsonDict['expressageDict'])
    return jsonDict


