#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""淘宝个人商品收藏爬虫"""


import requests, pymysql, random, time, re
from lxml import etree


class collect_product():
    def __init__(self, username, passworld):
        self.taobao_con = pymysql.connect(host='', user="", password="", database="", charset='utf8')

        self.taobao_cur = self.taobao_con.cursor()

        self.username = username
        self.passworld = passworld

        proxy_sql = ""
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]

        self.url = "https://shoucang.taobao.com/nodejs/item_collect_chunk.htm"


    def Get_html(self, cookies, ua):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": cookies,
            "Host": "shoucang.taobao.com",
            "Referer": "https://shoucang.taobao.com/item_collect.htm",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": ua,
            "X-Requested-With": "XMLHttpRequest",
        }

        pageNum = 0
        productList = []
        while True:
            params = {
                "ifAllTag": "0",
                "tab": "0",
                "tagId": "",
                "categoryCount": "0",
                "type": "0",
                "tagName": "",
                "categoryName": "",
                "needNav": "false",
                "startRow": "{}".format(30*pageNum),
                "t": "{}".format(int(time.time()*1000)),
            }
            pageNum += 1
            reql = requests.get(self.url, headers=headers, proxies=proxy, params=params)

            if len(str(reql.text).strip()) == 0:
                break

            else:
                html = etree.HTML(reql.text)
                for i in range(1, len(html.xpath("/html/body/li"))+1):
                    product_list = []
                    productImg = "https:" + html.xpath("/html/body/li[{}]/div[1]/div[1]/a/img//@src".format(i))[0]
                    storeUrl = "https:" + html.xpath("/html/body/li[{}]/div[1]/a[2]//@href".format(i))[0]
                    productUrl = "https:" + html.xpath("/html/body/li[{}]/div[2]/a//@href".format(i))[0]
                    productTitle = html.xpath("/html/body/li[{}]/div[2]/a//text()".format(i))[0]

                    prictList = html.xpath("/html/body/li[12]/div[3]/div".format(i))
                    if len(prictList) > 1:
                        price = html.xpath("/html/body/li[{}]/div[3]/div/div[2]/strong//text()".format(i))
                    else:
                        if html.xpath("/html/body/li[{}]/div[3]/div/div/strong//text()".format(i)):
                            price = html.xpath("/html/body/li[{}]/div[3]/div/div/strong//text()".format(i))[0]
                        else:
                            price = html.xpath("/html/body/li[{}]/div[3]/span//text()".format(i))[0]

                    productid = re.findall("id=(.*?)&", productUrl)[0]
                    product_list.append(productImg)
                    product_list.append(productid)
                    product_list.append(storeUrl)
                    product_list.append(price)
                    product_list.append(productUrl)
                    product_list.append(productTitle)
                    productList.append(product_list)
                    insert_sql = ""

                    try:
                        self.taobao_cur.execute(insert_sql)
                        self.taobao_con.commit()
                    except Exception as EF:
                        print(EF)

        return productList




    def main(self):
        select_sql = ""
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        productList = self.Get_html(cookie[0][0], cookie[0][1])

        self.taobao_cur.close()
        self.taobao_con.close()

        return productList



def main(username, passworld):
    collectPproduct = collect_product(username, passworld)
    productList = collectPproduct.main()

    return productList



if __name__ == '__main__':
    username = ""
    passworld = ""
    main(username, passworld)





