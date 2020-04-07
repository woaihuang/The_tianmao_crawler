#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-
"""
************************************************************************************************************************
使用pyppeteer来获取登陆时用的cookie
************************************************************************************************************************
author: huanghaoran
************************************************************************************************************************
使用扫码的方式登陆淘宝，各种验证方式的验证方法
"""




import time, random, pymysql, requests
from pyppeteer.launcher import launch
from lxml import html
etree = html.etree






user_agent_list_2 = [
        # Opera
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        # 360
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 淘宝浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        # 猎豹浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        # QQ浏览器
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        # sogou浏览器
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        # maxthon浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        # UC浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    ]
codenum = 0





def get_token_h5():
    """
    增加淘宝cookies的token字段
    :return:
    """
    url = "https://acs.m.taobao.com/h5/mtop.taobao.social.feed.aggregate/1.0/"
    appKey = '12574478'
    # 获取当前时间戳
    t = str(int(time.time() * 1000))

    data = '{"params":"{\\"nodeId\\":\\"\\",\\"sellerId\\":\\"50852803\\",\\"pagination\\":{\\"direction\\":\\"1\\",\\"hasMore\\":\\"true\\",\\"pageNum\\":\\"' + str(2) + '\\",\\"pageSize\\":\\"' + str(20) + '\\"}}","cursor":"' + str(2) + '","pageNum":"' + str(2) + '","pageId":5703,"env":"1"}'
    params = {'appKey': appKey, 'data': data}
    # 请求空获取cookies
    html = requests.get(url, params=params)

    _m_h5_tk = html.cookies['_m_h5_tk']
    _m_h5_tk_enc = html.cookies['_m_h5_tk_enc']

    token_h5 = "_m_h5_tk" + '=' + _m_h5_tk + ';' + "_m_h5_tk_enc" + "=" + _m_h5_tk_enc
    return token_h5




async def click_input(page, uniqueidentifier, lgToken):
    """
    从数据中台获取手机短信验证码，输入、确认登录
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    global codenum
    pollnum, verification = 0, True
    while pollnum <= 50:
        pollnum += 1
        reql_json = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10009", "msg": "请输入手机验证码", "username": "", "lgtoken": lgToken})
        verificationcode = eval(str(reql_json.text).replace("false", "False").replace("true", "True"))
        time.sleep(1)
        if verificationcode['code'] == 200:
            if codenum != verificationcode['data']['code']:
                codenum = verificationcode['data']['code']
                if verification:
                    reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10010", "msg": "正在验证", "username": "", "lgtoken": lgToken})
                    verification = False
                await page.frames[1].type('#J_Phone_Checkcode', verificationcode['data']['code'], {'delay': input_time_random() - 80})
                time.sleep(1)
                await page.frames[1].click("#submitBtn")  # 点击确认
                print("跳出循环")
                break




async def phone_code(page, uniqueidentifier, lgToken):
    """
    点击获取手机验证码，并模拟点击、输入确认登录
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    print("手机验证码验证")
    time.sleep(3)
    await page.frames[1].click("#J_GetCode")                            #点击获取手机验证码
    await click_input(page, uniqueidentifier, lgToken)                  #并模拟点击、输入确认登录




async def code_error(page, uniqueidentifier, lgToken):
    """
    手机验证码错误
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    print("手机验证码错误")
    reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10011", "msg": "手机验证码错误", "username": "", "lgtoken": lgToken})
    await click_input(page, uniqueidentifier, lgToken)                      #并模拟点击、输入确认登录




async def Checkcodefailure(page, uniqueidentifier, lgToken):
    """
    校验码失效，请重新获取
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    print("校验码失效，请重新获取")
    reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10012", "msg": "校验码失效，请重新获取", "username": "", "lgtoken": lgToken})
    await phone_code(page, uniqueidentifier, lgToken)  # 调取获取手机验证码方法




async def clickproductlogin(page, uniqueidentifier, lgToken):
    """
    点击曾经购买过的商品验证登陆
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    print("点击曾经购买过的商品")
    await page.frames[1].click(".ui-form-other")                          #点击更多验证方式
    time.sleep(2)
    for i in range(1, 5):
        elements = await page.frames[1].xpath('//*[@id="content"]/div/ol/li[{}]/a'.format(i))
        link = await (await elements[0].getProperty("href")).jsonValue()  # 获取连接
        if 'tag=8' in link:
            await elements[0].click()
            time.sleep(2)
            reql_scan_login_state = requests.post("http://api.lieyingdata.com/api/scan_login_state/", data={"id": uniqueidentifier, 'taobaocode': "10009", "msg": "请输入手机验证码", "username": "", "lgtoken": lgToken})
            await phone_code(page, uniqueidentifier, lgToken)               #调取获取手机验证码方法
            break




async def secondcode(page, uniqueidentifier, lgToken, codeerrnum, numberofretries):
    """
    验证码输入错误及失效时调取的函数
    :param page:
    :param uniqueidentifier:
    :param lgToken:
    :param codeerrnum:
    :param numberofretries:
    :return:
    """
    Secondaryconfir_mation = await page.frames[1].content()  # 获取iframe页面源码
    if "手机验证码错误" in Secondaryconfir_mation:
        while codeerrnum < 3:
            await code_error(page, uniqueidentifier, lgToken)
            Secondaryconfir_mation = await page.frames[1].content()
            if "手机验证码错误" in Secondaryconfir_mation:
                await code_error(page, uniqueidentifier, lgToken)
            elif "校验码失效，请重新获取" in Secondaryconfir_mation:
                await Checkcodefailure(page, uniqueidentifier, lgToken)
            codeerrnum += 1
        if codeerrnum >= 3:
            reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10013", "msg": "验证失败", "username": "", "lgtoken": lgToken})

    elif "校验码失效，请重新获取" in Secondaryconfir_mation:
        while numberofretries < 3:
            await Checkcodefailure(page, uniqueidentifier, lgToken)
            Secondaryconfir_mation = await page.frames[1].content()
            if "手机验证码错误" in Secondaryconfir_mation:
                await code_error(page, uniqueidentifier, lgToken)
            elif "校验码失效，请重新获取" in Secondaryconfir_mation:
                await Checkcodefailure(page, uniqueidentifier, lgToken)
            numberofretries += 1
        if numberofretries >= 3:
            reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10013", "msg": "验证失败", "username": "", "lgtoken": lgToken})
    else:
        time.sleep(2)
        print('到这里')




async def main(url, loop, uniqueidentifier, lgToken):
    """
    执行扫码登录主体函数
    :param url: 扫描二维码之后淘宝网站返回的地址
    :param loop: 异步实例
    :param uniqueidentifier: 用户唯一标识
    :param lgToken: 用户lgtoken
    :return:
    """
    ua = random.choices(user_agent_list_2)[0]
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({"headless":False, "args":["--no-sandbox"]})
    page = await browser.newPage()
    await page.setUserAgent(ua)
    await page.goto(url)  # 访问登录页面

    """以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。"""
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    starttime = time.time()
    aginnum = 0
    printflag, verificationflag, inputflag, code_error_flag, Checkfailureflag, numberofretries, codeerrnum, getphonecode, Secondary_confirmation = True, True, True, True, True, 0, 0, True, True
    while True:
        endtime = time.time()
        try:
            title = await  page.title()
            try:
                Secondaryconfirmation = await page.frames[1].content()
                if "请打开手机淘宝点击确认" in str(Secondaryconfirmation):
                    Secondary_confirmation = False
                    aaaaa = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10007", "msg": "请二次授权", "username": "", "lgtoken": lgToken})
                if "为确认是你本人操作，请选择验证方式完成身份验证：" in Secondaryconfirmation and not Secondary_confirmation:
                    while True:
                        try:
                            await page.close()
                            await browser.close()
                            break
                        except OSError as reason:
                            print("reason: ", reason)
                    aaaaa = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10003", "msg": "已取消", "username": "", "lgtoken": lgToken})

                if "立即摆脱繁琐短信验证" in str(Secondaryconfirmation):
                    time.sleep(3)
                    await page.frames[1].click(".J_SendCodeBtn")
                    pollnum = 0
                    while pollnum <= 50:
                        reql_json = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10009", "msg": "请输入手机验证码", "username": "", "lgtoken": lgToken})
                        if inputflag:
                            reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10009", "msg": "请输入手机验证码", "username": "", "lgtoken": lgToken})
                            inputflag = False
                        pollnum += 1
                        verificationcode = eval(str(reql_json.text).replace("false", "False").replace("true", "True"))
                        time.sleep(1)
                        if verificationcode['code'] == 200:
                            if verificationflag:
                                reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10010", "msg": "正在验证", "username": "", "lgtoken": lgToken})
                                verificationflag = False
                            await page.frames[1].type('.J_SafeCode', verificationcode['data']['code'], {'delay': input_time_random() - 80})
                            time.sleep(1)
                            await page.frames[1].click("#J_FooterSubmitBtn")  # 点击确认
                            printflag = False
                            break

                if "手机验证码验证" in str(Secondaryconfirmation):
                    if getphonecode:
                        reql_scan_login_state = requests.post("", data={"id": uniqueidentifier, 'taobaocode': "10009", "msg": "请输入手机验证码", "username": "", "lgtoken": lgToken})
                        await phone_code(page, uniqueidentifier, lgToken)                   #调取获取手机验证码方法
                        getphonecode = False
                    await secondcode(page, uniqueidentifier, lgToken, codeerrnum, numberofretries)                      #验证码输入错误及失效

                if "请点击你近期购买过的物品" in str(Secondaryconfirmation):
                    await clickproductlogin(page, uniqueidentifier, lgToken)
                    await secondcode(page, uniqueidentifier, lgToken, codeerrnum, numberofretries)                      #验证码输入错误及失效

            except Exception as Gh:
                print("Gh: ", Gh)
            try:
                time.sleep(2)
                content = await  page.content()
                html = etree.HTML(content)
                username = html.xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a[1]//text()')
                if username and username[0] != "undefined":
                    username = username[0]
                    cookies = await get_cookie(page)
                    while True:
                        try:
                            await page.close()
                            await browser.close()
                            break
                        except OSError as reason:
                            print("reason: ", reason)
                    insert_cookies(username, cookies, ua)
                    return username
            except:
                pass
            if endtime-starttime > 20:
                await page.close()
                await browser.close()
                return "10010"
        except Exception as F:
            print("Execution context was destroyed, most likely because of a navigation.: ", F)
            try:
                print("访问主页")
                while True:
                    await page.goto("https://www.taobao.com/")
                    """以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。"""
                    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
                    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
                    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
                    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
                    content = await  page.content()
                    html = etree.HTML(content)
                    username = html.xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a[1]//text()')
                    print("username: ", username)
                    # naughtyvalue = html.xpath('')
                    if username and username[0] != "undefined":
                        username = username[0]
                        cookies = await get_cookie(page)
                        while True:
                            try:
                                await page.close()
                                await browser.close()
                                break
                            except OSError as reason:
                                print(reason)
                        insert_cookies(username, cookies, ua)
                        return username
            except Exception as E:
                print("E: ", E)
                print("重试")
                if aginnum == 5:
                    print("重试结束")
                    await page.close()
                    await browser.close()
                    break
                aginnum += 1




def input_time_random():
    return random.randint(150, 201)




def insert_cookies(username, cookies, ua):
    """
    向数据库存储cookies信息
    :param username:
    :param cookies:
    :param ua:
    :return:
    """
    taobao_con = pymysql.connect(host='', user="", password="", database="", charset='utf8')
    taobao_cur = taobao_con.cursor()
    execute_sql = """"""
    try:
        taobao_cur.execute(execute_sql)
        taobao_con.commit()
        taobao_cur.close()
        taobao_con.close()
    except Exception as E:
        print(execute_sql)
        print("数据库插入错误：{}".format(E))




async def get_cookie(page):
    """
    获取登陆之后的cookies
    :param page:
    :return:
    """
    token_h5 = get_token_h5()
    cookies_list = await page.cookies()
    cookies = ''
    cookie_dict = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        cookie_dict = cookie_dict + str(cookie) + ";"
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    cookies = cookies+token_h5
    return cookies




def start_func(loop, url, uniqueidentifier, lgToken):
    """
    启动函数
    :param loop:
    :param url:
    :param uniqueidentifier:
    :param lgToken:
    :return:
    """
    try:
        username = loop.run_until_complete(main(url, loop, uniqueidentifier, lgToken))  # 将协程注册到事件循环，并启动事件循环
        return username
    except Exception as E:
        print(E)
        return "10004"



