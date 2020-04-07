#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


"""
*******************************************************************************************************************************************************
获取个人评论信息
*******************************************************************************************************************************************************
"""


import requests, pymysql, random, re, time
from lxml import etree



class get_person_msg():
    def __init__(self, username):
        self.username = username
        self.taobao_con = pymysql.connect(host='', user="", password="", database="", charset='utf8')
        self.taobao_cur = self.taobao_con.cursor()

        proxy_sql = "SELECT proxy FROM `proxy_table`"
        try:
            self.taobao_cur.execute(proxy_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        aa = self.taobao_cur.fetchall()
        self.iplist = [i[0] for i in aa]

        self.person_url = "https://rate.taobao.com/user-myrate-UvCIWvF8WMmvuvGxYMQTT--buyerOrSeller%7C3--receivedOrPosted%7C1.htm"



    def preson_fun(self, cookie):
        proxy = eval(random.choice(self.iplist))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "rate.taobao.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }

        reql = requests.get(self.person_url, headers=headers, proxies=proxy, allow_redirects=False)

        html = etree.HTML(reql.text)

        comment_list1 = {}
        comment_num_dict = {}                   #评价数字典
        for i in range(1, 5):
            one_dict = {}
            tr_list = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[{}]//text()'.format(i))
            tr_list = [i for i in tr_list if i != '\n\t\t\t\t']
            tr_list = [i for i in tr_list if i != '\n\t\t\t']
            tr_list = [i for i in tr_list if i != '\n\t\t']
            comment_num_dict[tr_list[0]] = []
            one_dict["最近1周"] = tr_list[1]
            one_dict["最近1个月"] = tr_list[2]
            one_dict["最近6个月"] = tr_list[3]
            one_dict["6个月前"] = tr_list[4]
            one_dict["总计"] = tr_list[5]
            comment_num_dict[tr_list[0]].append(one_dict)
        insert_comment_sql = """INSERT INTO comment_num_table (username, comment_num) VALUES('{}', "{}")""".format(self.username, comment_num_dict)

        comment_list1["username"] = self.username
        comment_list1["comment_num"] = comment_num_dict
        try:
            self.taobao_cur.execute(insert_comment_sql)
        except Exception as df:
            if "PRIMARY" in str(df):
                updata_sql = """UPDATE comment_num_table SET comment_num="{}" WHERE username='{}'""".format(comment_num_dict, self.username)
                try:
                    self.taobao_cur.execute(updata_sql)
                except Exception as df1:
                    print(df1)

        presonl_comment = []
        link_num = 1
        while True:
            try:
                comment_dict = {}
                comment_list = []
                product_url = html.xpath('//*[@id="J_RateList"]/tbody/tr[{}]/td[4]/a//@href'.format(link_num))[0]

                product_num = re.findall("[1-9]\d*$", product_url)[0]

                comment = html.xpath('//*[@id="J_RateList"]/tbody/tr[{}]/td[2]/p[1]//text()'.format(link_num))

                add_comment = html.xpath('//*[@id="J_RateList"]/tbody/tr[{}]/td[2]/div/p[1]//text()'.format(link_num))

                if len(comment) != 1:
                    come_comment = {}
                    come_comment['来源'] = [str(ig).strip() for ig in comment if len(str(ig).strip()) > 1][0]
                    come_comment['评论'] = [str(ig).strip() for ig in comment if len(str(ig).strip()) > 1][1]
                    comment_dict['评论'] = come_comment
                else:
                    come_comment = {}
                    come_comment['来源'] = []
                    come_comment['评论'] = str(comment[0]).strip()
                    comment_dict['评论'] = come_comment

                if add_comment:
                    comment_dict['追加评论'] = str(add_comment[2]).strip()
                else:
                    comment_dict['追加评论'] = []
                print(link_num, product_num, comment_dict)

                link_num += 1

                insert_sql = """INSERT INTO comment_table (username, productid, comment, createtime) VALUES('{}', '{}', "{}", NOW())""".format(self.username, product_num, comment_dict)

                try:
                    self.taobao_cur.execute(insert_sql)
                    self.taobao_con.commit()
                except Exception as df:
                    if "PRIMARY" in str(df):
                        update_sql = "UPDATE comment_table SET createtime=NOW() WHERE productid='{}'".format(product_num)
                        try:
                            self.taobao_cur.execute(update_sql)
                            self.taobao_con.commit()
                        except Exception as EF:
                            print("数据更改失败：", EF)

                comment_list.append(self.username)
                comment_list.append(product_num)
                comment_list.append(comment_dict)
                presonl_comment.append(comment_list)

            except Exception as DF:
                print(DF)
                break

        return presonl_comment, comment_list1



    def main(self):
        select_sql = "SELECT cookie FROM `cookie_table` WHERE username='{}'".format(self.username)
        try:
            self.taobao_cur.execute(select_sql)
        except Exception as E:
            print("查询错误！{}".format(E))

        cookie = self.taobao_cur.fetchall()

        presonl_comment, comment_num_list = self.preson_fun(cookie[0][0])

        return presonl_comment, comment_num_list





def start_func(username):
    get_person_msgs = get_person_msg(username)
    return get_person_msgs.main()




