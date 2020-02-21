# -*- coding: utf-8 -*-

# 引入包
import pandas as pd
import requests
import json
import http.cookiejar as cookielib
import io  
import sys 

#改变标准输出的默认编码 
#utf-8中文乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='UTF-8')

# session代表某一次连接
jqSession = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
jqSession.cookies = cookielib.LWPCookieJar(filename = "jqSessionCookies.txt")



# headers
header = {
    "Referer":
    'https://www.joinquant.com/user/login/index?reason=logout',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
}

# 模仿 登录
def jqLogin(account, password):
    print("开始模拟登录")
    postUrl = "https://www.joinquant.com/user/login/index?type=login"
    postData = {
        "passport":account,
        "password":password,
    }
    # 使用session直接post请求
    responseRes = jqSession.post(postUrl, data = postData, headers = header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    # print(f"text = {responseRes.text}",)
    # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
    jqSession.cookies.save()


# 通过访问个人中心页面的返回状态码来判断是否为登录状态
def isLoginStatus():
    routeUrl = "https://www.joinquant.com/view/user/floor?type=mainFloor"
    # 下面有两个关键点
    # 第一个是header，如果不设置，会返回500的错误
    # 第二个是allow_redirects，如果不设置，session访问时，服务器返回302，
    # 然后session会自动重定向到登录页面，获取到登录页面之后，变成200的状态码
    # allow_redirects = False  就是不允许重定向
    responseRes = jqSession.get(routeUrl, headers = header, allow_redirects = False)
    print(f"isLoginStatus = {responseRes.status_code}")
    if responseRes.status_code != 200:
        return False
    else:
        return True



# cookies
def get_cookies():
    cookies_str = 'user-22486821351=2|1:0|10:1582197132|16:user-22486821351|48:ZjFlNTliNjQtMzQxNy00NWIyLTk0ZGQtYzEwZTYwOWI0NjUw|4a2e7a6d2062b5b5bbe93e19e14433bc3dfb546280cc97c8bb09768a071d0af1; uid=CiyeXF4nFB6RJwVGnDP3Ag==; gr_user_id=4888dc93-fdda-4579-9b6b-143b29e085cf; UM_distinctid=16fc8a6addf102-00f87b01990676-34564a7c-144000-16fc8a6ade242c; _xsrf=2|5696dfdb|22d9f82efd1303fd8b35829e891bdc2e|1579619405; hideBanner=1; getStrategy=1; CNZZDATA1256107754=189823841-1579616418-https%253A%252F%252Fwww.baidu.com%252F%7C1582167452; token=aef1ba701609dc1fe922b51275b78a615ae33dd2; Hm_lvt_aab1c038280787bd3547c63800577e6b=1581481602,1582091702,1582171814,1582197121; Hm_lpvt_aab1c038280787bd3547c63800577e6b=1582197121; gr_session_id_949f6a566feb9b09=09f57b8d-85c9-41d9-90ff-a0a211150f3c; gr_session_id_949f6a566feb9b09_09f57b8d-85c9-41d9-90ff-a0a211150f3c=true; PHPSESSID=2mk8e2qpg386afie2pspvd0hk4'
    # cookies_str转换为字典格式
    cookies_str = cookies_str.split('; ')
    cookies = {}
    for item in cookies_str:
        temp = item.split('=')
        cookies[temp[0]] = temp[1]
    return cookies


file_list = [
    'stk_sz_002415.csv', 'mcr_u10y.csv', 'cmm_value.csv', 'idx_sh_000977.csv',
    'idx_sz_399976.csv', 'mcr_u5y.csv', 'stk_bank_change.csv', 'cmm_gsr.csv',
    'idu_sw1_801130.csv', 'stk_sz_002807.csv', 'stk_pool_gw300.csv',
    'stk_pool_gwcyb.csv', 'stk_sh_600036.csv', 'idx_sh_000931.csv',
    'idu_sw1_change.csv', 'idx_relevance.csv', 'idu_sw1_801110.csv',
    'idx-img-qscpe.png', 'idu_sw1_801180.csv', 'mcr_bdi.csv',
    'msg_xqwz_4776750571.csv', 'stk_sh_600887.csv', 'msg_blog_60278066.csv',
    'stk_sh_600566.csv', 'idu_sw1_801080.csv', 'stk_sh_601166.csv',
    'idx-img-kj.png', 'stk_sh_601818.csv', 'msg_xqwz_5941996397.csv',
    'stk_pool_gw1000.csv', 'idx_sh_000989.csv', 'idx_data.db', 'mcr_udi.csv',
    'idu_sw1_801150.csv', 'idu_sw1_801760.csv', 'idx_sh_000015.csv',
    'idx_sh_000990.csv', 'idx_hw_spx.csv', 'idx_sz_399106.csv',
    'idx_hw_n225.csv', 'idx_sz_399550.csv', 'stk_sh_600015.csv',
    'msg_weixin_长赢指数投资.csv', 'idu_sw1_801710.csv', 'mcr_vix.csv',
    'idu_sw1_801880.csv', 'stk_roe20_value.csv', 'mcr_scn.csv',
    'idx_sz_399812.csv', 'msg_weibo_1254381361.csv', 'plt_sha.csv',
    'idx_relevance.png', 'stk_sh_600660.csv', 'mcr_c5y.csv',
    'idx_sh_000991.csv', 'msg_weixin_梧桐拾贝社.csv', 'idx_hw_hsi.csv',
    'idu_sw1_801210.csv', 'stk_sh_601877.csv', 'idx_change.csv',
    'idx_hw_ftse.csv', 'stk_sh_600016.csv', 'idx_sz_399989.csv',
    'idx_pool.csv', 'stk_sh_601229.csv', 'stk_sz_002294.csv',
    'stk_pool_roe20.csv', 'stk_sh_600926.csv', 'idx_sh_000922.csv',
    'idx_sh_000068.csv', 'idx_sz_399975.csv', 'stk_pool_gw500.csv',
    'stk_sh_600919.csv', 'idx_sz_399811.csv', 'idu_sw1_801770.csv',
    'idx_sz_399986.csv', 'idx_hw_fchi.csv', 'stk_sz_002236.csv',
    'stk_sz_002714.csv', 'idx-img-pbs.png', 'stk_sh_601939.csv', 'mcr_pmi.csv',
    'mcr_uch.csv', 'stk_sz_000661.csv', 'idu_sw1_801890.csv',
    'idu_sw1_801120.csv', 'stk_bank_value.csv', 'idx_sh_000010.csv',
    'idu_sw1_801050.csv', 'mcr_cpi.csv', 'idx_sh_000827.csv',
    'idx_sh_000906.csv', 'msg_weixin_码农滚雪球.csv', 'stk_sh_600816.csv',
    'idu_sw1_801200.csv', 'idx_sh_000841.csv', 'idx-img-qscpb.png',
    'idu_sw1_801740.csv', 'stk_pool_bank.csv', 'stk_roe20_change.csv',
    'idx_sz_399001.csv', 'stk_sz_000688.csv', 'cmm_oil.csv',
    'stk_sh_601988.csv', 'idu_sw1_801030.csv', 'idx_hw_hscei.csv',
    'idx_sh_000016.csv', 'stk_sz_000333.csv', 'stk_sz_000001.csv',
    'stk_sz_000538.csv', 'msg_weibo_1669616825.csv', 'plt_value.csv',
    'fnd_pool_index.csv', 'cmm_xau.csv', 'idx_sz_399101.csv',
    'idx_sz_399324.csv', 'idx_hw_sx5e.csv', 'idu_sw1_801750.csv',
    'idu_sw1_801780.csv', 'mcr_ms.csv', 'idx_sh_000902.csv',
    'stk_sz_002142.csv', 'stk_sh_600908.csv', 'stk_sh_601398.csv',
    'idx_sh_000993.csv', 'stk_sz_002081.csv', 'idu_sw1_value.csv',
    'cmm_gor.csv', 'stk_sz_000651.csv', 'mcr_pool.csv', 'stk_sh_600000.csv',
    'idx_sh_000300.csv', 'idu_sw1_801140.csv', 'stk_sh_601997.csv',
    'idx_sz_399967.csv', 'stk_sh_601288.csv', 'idx_hw_ndaq.csv',
    'idx-img-zj.png', 'stk_sh_601998.csv', 'msg_weixin_股市药丸.csv',
    'stk_sh_603288.csv', 'stk_sh_600690.csv', 'idx_sz_399005.csv',
    'plt_cyb.csv', 'mcr_shibor.csv', 'cmm_pool.csv', 'idu_sw1_801020.csv',
    'idx_sh_000009.csv', 'stk_sh_601169.csv', 'stk_sh_603323.csv',
    'stk_sh_600201.csv', 'idx_sh_000001.csv', 'mcr_c10y.csv', 'plt_sza.csv',
    'idx_sh_000998.csv', '.ipynb_checkpoints', 'idu_sw1_801170.csv',
    'stk_pool_edticket.csv', 'idx_sh_000807.csv', 'stk_sh_603898.csv',
    'idx_sh_000992.csv', 'stk_sz_000423.csv', 'plt_zxb.csv',
    'idx_sz_399997.csv', 'idx_sz_399624.csv', 'cmm_xag.csv',
    'idx_sz_399006.csv', 'idx_sh_000905.csv', 'stk_sh_601515.csv',
    'mcr_ppi.csv', 'stk_sz_000963.csv', 'plt_hsa.csv', 'idx_sh_000932.csv',
    'msg_weixin_阿甘数量化2.csv', 'idx_sz_399808.csv', 'idx_sz_399673.csv',
    'idx_sh_000925.csv', 'stk_sh_601128.csv', 'stk_sz_002271.csv',
    'idu_sw1_801790.csv', 'msg_weibo_5687069307.csv', 'idx_sh_000904.csv',
    'plt_szb.csv', 'plt_pool.csv', 'mcr_nfc.csv', 'msg_xqft_4776750571.csv',
    'stk_sz_002508.csv', 'idu_sw1_801010.csv', 'stk_sz_002032.csv',
    'idx_sh_000903.csv', 'idu_pool_sw1.csv', 'stk_sh_600276.csv',
    'idu_sw1_801730.csv', 'idx_sh_000852.csv', 'idx_sh_000986.csv',
    'stk_sh_600340.csv', 'cmm_change.csv', 'idx_sh_000988.csv',
    'idx_sh_000978.csv', 'idx_sz_399396.csv', 'stk_sh_600519.csv',
    'stk_sz_000049.csv', 'idx_hw_djia.csv', 'idx_sz_399971.csv',
    'idx_sz_399102.csv', 'idu_sw1_801230.csv', '网格-交易A.xlsm', 'mcr_gdp.csv',
    'idx_sh_000985.csv', 'stk_sz_002372.csv', 'idx_sz_399806.csv',
    'stk_sz_002304.csv', 'idx_sz_399330.csv', 'stk_sh_601009.csv',
    'stk_sh_600612.csv', 'stk_sz_000002.csv', 'mcr_ucy.csv', 'idx-img-pes.png',
    'idx_hw_gdaxi.csv', 'idu_sw1_801040.csv', 'plt_change.csv',
    'idx_sz_399814.csv', 'idu_sw1_801160.csv', 'idx_value.csv',
    'idu_sw1_801720.csv'
]

# cookies = get_cookies()




if __name__ == "__main__":
    # 第一步：尝试使用已有的cookie登录
    jqSession.cookies.load()
    isLogin = False#isLoginStatus()
    print(f"is login = {isLogin}")
    if isLogin == False:
        # 第二步：如果cookie已经失效了，那就尝试用帐号登录
        print(f"cookie失效，用户重新登录...")
        jqLogin("13695683829", "ssk741212")

    fn = "idx_value.csv"
    # try:
    print(fn)
    url = "https://www.joinquant.com/user/22486821351/api/contents/Data/%s?type=file&format=text&_=1580445911713" % (
        fn)
    r = jqSession.get(url)
    r.encoding = 'UTF-8'
    print(url)
    # print(r.text)

    data = json.loads(r.text).get('content')
    
    with open('%s' % (fn), "w", encoding='utf-8') as f:
        f.write(data)
    df = pd.read_csv(fn)
    df=df[df['aid']==10]
    df=df.sort_values("pe_e")
    print(df)
    # except Exception as e:
    #     print(e)