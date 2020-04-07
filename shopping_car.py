#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""
获取购物车信息
"""




import requests, pymysql, random, re, json




class shopping_trolley():
    def __init__(self, username, passworld):
        self.taobao_con = pymysql.connect(
            host='',
            user="",
            password="",
            database="",
            charset='utf8'
        )

        self.taobao_cur = self.taobao_con.cursor()

        self.username = username
        self.passworld = passworld

        proxy_sql = "SELECT proxy FROM `proxy_table`"
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]

        self.url = "https://cart.taobao.com/cart.htm"
        self.json_url = "https://cart.taobao.com/json/asyncGetMyCart.do"

        self.dateDict = {"status": None, "msg": None}



    def Get_message(self, cookies, ua):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookies,
            "Host": "cart.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ua
        }

        try:
            reql = requests.get(self.url, headers=headers, proxies=proxy)

            responseDate = reql.text

            datedict = eval(str(re.findall("firstData = (.*?)catch", responseDate, re.S)[0]).replace(";}", "").replace("true", "True").replace("false", "False"))

            product_list = datedict['list']

            endTime = datedict['globalData']["startTime"]

            lastList = []
            for i in product_list:
                for j in i["bundles"][0]["orders"]:
                    productDict = {}
                    productDict['id'] = j["id"]
                    productDict['productImg'] = "https:" + j["pic"]                                                  #商品图片
                    productDict['seller'] = j["seller"]                                                              #店家旺旺名称
                    productDict['shopName'] = j['shopName']                                                          #店铺名称
                    productDict['shopUrl'] = "https:" + j['shopUrl']                                                 #店铺链接
                    productDict['title'] = j['title']                                                                #商品名称
                    productDict['toBuy'] = j["toBuy"]                                                                #商品来源
                    productDict['productUrl'] = "https:" + j["url"]                                                  #商品详情链接
                    productDict['productPrice'] = j['price']['now']/100                                              #商品价格
                    if "codeMsg" in j:
                        productDict['status'] = "宝贝失效"
                    else:
                        productDict['status'] = "宝贝有效"

                    if 'skus' in j:
                        skus = {}
                        for key, val in j['skus'].items():
                            skus[key] = val
                    else:
                        skus = {}
                    productDict['skus'] = skus

                    lastList.append(productDict)

            lastList = self.get_json_data(cookies, ua, 2, endTime, lastList)

            return lastList

        except Exception as EF:
            print("错误：", EF)
            return str(EF)





    def get_json_data(self, cookies, ua, pagenum, endTime, lastList):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": cookies,
            "Host": "cart.taobao.com",
            "Referer": "https://cart.taobao.com/cart.htm",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": ua,
            "X-Requested-With": "XMLHttpRequest",
        }

        while True:
            try:
                params = {
                    "isNext": "true",
                    "endTime": endTime,
                    "page": pagenum,
                    "_thwlang": "zh_CN",
                    "_tb_token_": re.findall("_tb_token_=(.*?);", cookies)[0],
                    "_ksTS": "1573797002551_532",
                    "callback": "asyncGetMyCart"
                }

                reql = requests.get(self.json_url, headers=headers, proxies=proxy, params=params)

                responseDate = reql.text

                product_dict = json.loads(re.findall("asyncGetMyCart\((.*)", responseDate, re.S)[0][:-1])

                endTime = product_dict['globalData']['startTime']

                pagenum += 1

                for i in product_dict['list']:
                    for j in i["bundles"][0]["orders"]:
                        productDict = {}
                        productDict['id'] = j["id"]
                        productDict['productImg'] = j["pic"]                                        #商品图片
                        productDict['seller'] = j["seller"]                                         #店家旺旺名称
                        productDict['shopName'] = j['shopName']                                     #店铺名称
                        productDict['shopUrl'] = "https:" + j['shopUrl']                            #店铺链接
                        productDict['title'] = j['title']                                           #商品名称
                        productDict['toBuy'] = j["toBuy"]                                           #商品来源
                        productDict['productUrl'] = "https:" + j["url"]                             #商品详情链接
                        productDict['productPrice'] = j['price']['now']/100                         #商品价格
                        if "codeMsg" in j:
                            productDict['status'] = "宝贝失效"
                        else:
                            productDict['status'] = "宝贝有效"

                        if 'skus' in j:
                            skus = {}
                            for key, val in j['skus'].items():
                                skus[key] = val
                        else:
                            skus = {}
                        productDict['skus'] = skus

                        lastList.append(productDict)


            except:
                break

        for product in lastList:
            inster_sql = """INSERT INTO shopping_car (username, pwd, id, productImg, seller, shopName, shopUrl, title, toBuy, productUrl, productPrice, status, skus, createtime) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', "{}", NOW())""".format(self.username, self.passworld, product['id'], product['productImg'], product['seller'], product['shopName'], product['shopUrl'], product['title'], product['toBuy'], product['productUrl'], product['productPrice'], product['status'], product['skus'])

            try:
                self.taobao_cur.execute(inster_sql)
                self.taobao_con.commit()
            except Exception as DF:
                if "PRIMARY" in str(DF):
                    updata_sql = "UPDATE shopping_car SET createtime=NOW() WHERE id='{}'".format(product['id'])
                    try:
                        self.taobao_cur.execute(updata_sql)
                        self.taobao_con.commit()
                    except Exception as df:
                        print("数据更改失败：", df)

        return lastList




    def main(self):
        select_sql = "SELECT cookie, user_agent FROM `cookie_table` WHERE username='{}' AND pwd='{}'".format(self.username, self.passworld)
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        lastList = self.Get_message(cookie[0][0], cookie[0][1])

        return lastList




def start_func(username, passworld):
    shoppingTrolley = shopping_trolley(username, passworld)
    lastList = shoppingTrolley.main()

    return lastList


if __name__ == '__main__':
    username = "金骆驿"
    passworld = "jly1314yy1207"
    start_func(username, passworld)

