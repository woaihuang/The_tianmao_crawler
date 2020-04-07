#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-





"""
************************************************************************************************************************
收藏店铺信息抓取
************************************************************************************************************************
"""



import requests, time, random, pymysql
from lxml import etree


class StoreCollect():
    def __init__(self, username, passworld):
        self.url = "https://shoucang.taobao.com/nodejs/shop_collect_list_chunk.htm"
        self.username = username
        self.passworld = passworld

        self.taobao_con = pymysql.connect(host='', user="", password="", database="", charset='utf8')

        self.taobao_cur = self.taobao_con.cursor()

        proxy_sql = ""
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]

    def Get_html(self, cookies, ua):
        proxy = eval(random.choice(self.iplist))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookies,
            "Host": "shoucang.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ua
        }

        pageNum = 0
        productList = []
        while True:
            params = {
                "ifAllTag": "0",
                "tab": "0",
                "categoryCount": "0",
                "tagName": "",
                "type": "0",
                "categoryName": "",
                "needNav": "false",
                "startRow": "{}".format(6 * pageNum),
                "t": "{}".format(int(time.time() * 1000))
            }

            reql = requests.get(self.url, headers=headers, proxies=proxy, params=params)

            if len(str(reql.text).strip()) == 0:
                break

            else:
                html = etree.HTML(reql.text)

                for i in range(1, len(html.xpath("/html/body/li")) + 1):
                    product_list = []
                    shopnames = html.xpath("/html/body/li[{}]/div[1]/div[2]/div[1]/a[2]//text()".format(i))  # 店铺名字
                    if len(shopnames) != 0:
                        shopname = str(shopnames[0]).strip()
                        shopUrl = str("https:" + html.xpath("/html/body/li[{}]/div[1]/div[2]/div[1]/a[2]//@href".format(i))[0]).strip()  # 店铺链接
                    else:
                        shopname = str(html.xpath("/html/body/li[{}]/div[1]/div[2]/div[1]/a//text()".format(i))[0]).strip()  # 店铺名字
                        shopUrl = str("https:" + html.xpath("/html/body/li[{}]/div[1]/div[2]/div[1]/a//@href".format(i))[0]).strip()

                    wangwangnice = str(html.xpath("/html/body/li[{}]/div[1]/div[2]/div[2]/a//@title".format(i))[0]).strip()  # 旺旺昵称
                    NewArrival = str(html.xpath("/html/body/li[{}]/div[2]/div[1]/div/div[1]/em//text()".format(i))[0]).strip()  # 本周上新
                    discounts = str(html.xpath("/html/body/li[{}]/div[2]/div[1]/div/div[2]/em//text()".format(i))[0]).strip()  # 优惠
                    hotsell = str(html.xpath("/html/body/li[{}]/div[2]/div[1]/div/div[3]/em//text()".format(i))[0]).strip()  # 热销
                    Forsale = str(html.xpath("/html/body/li[{}]/div[2]/div[1]/div/div[4]/em//text()".format(i))[0]).strip()  # 即将上架
                    collectionNum = str(
                        html.xpath("/html/body/li[{}]/div[4]/div[3]//text()".format(i))[0]).strip()  # 收藏人数

                    product_list.append(shopname)
                    product_list.append(shopUrl)
                    product_list.append(wangwangnice)
                    product_list.append(NewArrival)
                    product_list.append(discounts)
                    product_list.append(hotsell)
                    product_list.append(Forsale)
                    product_list.append(collectionNum)
                    productList.append(product_list)

                    insert_sql = ""
                    try:
                        self.taobao_cur.execute(insert_sql)
                        self.taobao_con.commit()
                    except Exception as EF:
                        print(EF)

            pageNum += 1

        return productList

    def main(self):
        select_sql = ""
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        productList = self.Get_html(cookie[0][0], cookie[0][1])

        return productList


def main(username, passworld):
    Storecollect = StoreCollect(username, passworld)
    productList = Storecollect.main()

    return productList


if __name__ == '__main__':
    username = ""
    passworld = ""
    main(username, passworld)
