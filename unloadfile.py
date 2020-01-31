#引入包
import pandas as pd
import requests,json,time,os


# headers
header={
    "HOST":'www.joinquant.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
    # "Referer": "https://www.joinquant.com/research?target=research&url=/user/22486821351/view/Data/idx-img-zj.png",
    # "Accept-Encoding": "gzip, deflate, br"
    }

# cookies
def get_cookies():
    cookies_str='user-22486821351=2|1:0|10:1580441327|16:user-22486821351|48:Yzk1NDUyMDMtODA1NC00MzhlLTk0ZDEtMTAzMmQxNDBjM2Y2|c239f118b6ff961da39a5c94c9f9d6d3797d7e2e307e3ed767133cc5fd9d5205; uid=CiyeXF4nFB6RJwVGnDP3Ag==; gr_user_id=4888dc93-fdda-4579-9b6b-143b29e085cf; UM_distinctid=16fc8a6addf102-00f87b01990676-34564a7c-144000-16fc8a6ade242c; _xsrf=2|5696dfdb|22d9f82efd1303fd8b35829e891bdc2e|1579619405; hideBanner=1; token=2de71b6063fdf241fd25b2afc0ffca4bb2fdedc0; Hm_lvt_aab1c038280787bd3547c63800577e6b=1580390254,1580391292,1580399696,1580441364; PHPSESSID=vv3k6p9gcfkpgnmilh0ug5smf2; gr_cs1_6a7c9d65-f791-4b11-88c3-150d8e0f047b=user_id%3A70c77a62964c3cfcac500ba608f87373; CNZZDATA1256107754=189823841-1579616418-https%253A%252F%252Fwww.baidu.com%252F%7C1580445163; gr_session_id_949f6a566feb9b09=cbda1960-8812-4436-a793-42f421deab59; Hm_lpvt_aab1c038280787bd3547c63800577e6b=1580445902; gr_session_id_949f6a566feb9b09_cbda1960-8812-4436-a793-42f421deab59=true; gr_cs1_cbda1960-8812-4436-a793-42f421deab59=user_id%3A70c77a62964c3cfcac500ba608f87373'
    
    #cookies_str="user-22486821351=2|1:0|10:1580441327|16:user-22486821351|48:Yzk1NDUyMDMtODA1NC00MzhlLTk0ZDEtMTAzMmQxNDBjM2Y2|c239f118b6ff961da39a5c94c9f9d6d3797d7e2e307e3ed767133cc5fd9d5205; uid=CiyeXF4nFB6RJwVGnDP3Ag==; gr_user_id=4888dc93-fdda-4579-9b6b-143b29e085cf; UM_distinctid=16fc8a6addf102-00f87b01990676-34564a7c-144000-16fc8a6ade242c; _xsrf=2|5696dfdb|22d9f82efd1303fd8b35829e891bdc2e|1579619405; hideBanner=1; token=2de71b6063fdf241fd25b2afc0ffca4bb2fdedc0; Hm_lvt_aab1c038280787bd3547c63800577e6b=1580390254,1580391292,1580399696,1580441364; PHPSESSID=vv3k6p9gcfkpgnmilh0ug5smf2; CNZZDATA1256107754=189823841-1579616418-https%253A%252F%252Fwww.baidu.com%252F%7C1580451493; gr_cs1_16f2fe78-9132-4f2c-b14c-aa75e2cc96d3=user_id%3A70c77a62964c3cfcac500ba608f87373; gr_session_id_949f6a566feb9b09=2e33008c-b12f-4700-936f-21423c836203; Hm_lpvt_aab1c038280787bd3547c63800577e6b=1580455307; gr_cs1_2e33008c-b12f-4700-936f-21423c836203=user_id%3A70c77a62964c3cfcac500ba608f87373; gr_session_id_949f6a566feb9b09_2e33008c-b12f-4700-936f-21423c836203=true"
    #cookies_str转换为字典格式
    cookies_str=cookies_str.split('; ')
    cookies={}
    for item in cookies_str:
        temp=item.split('=')
        cookies[temp[0]]=temp[1]  
    return cookies


file_list=['stk_sz_002415.csv',
'mcr_u10y.csv',
'cmm_value.csv',
 'idx_sh_000977.csv',
 'idx_sz_399976.csv',
 'mcr_u5y.csv',
 'stk_bank_change.csv',
 'cmm_gsr.csv',
 'idu_sw1_801130.csv',
 'stk_sz_002807.csv',
 'stk_pool_gw300.csv',
 'stk_pool_gwcyb.csv',
 'stk_sh_600036.csv',
 'idx_sh_000931.csv',
 'idu_sw1_change.csv',
 'idx_relevance.csv',
 'idu_sw1_801110.csv',
 'idx-img-qscpe.png',
 'idu_sw1_801180.csv',
 'mcr_bdi.csv',
 'msg_xqwz_4776750571.csv',
 'stk_sh_600887.csv',
 'msg_blog_60278066.csv',
 'stk_sh_600566.csv',
 'idu_sw1_801080.csv',
 'stk_sh_601166.csv',
 'idx-img-kj.png',
 'stk_sh_601818.csv',
 'msg_xqwz_5941996397.csv',
 'stk_pool_gw1000.csv',
 'idx_sh_000989.csv',
 'idx_data.db',
 'mcr_udi.csv',
 'idu_sw1_801150.csv',
 'idu_sw1_801760.csv',
 'idx_sh_000015.csv',
 'idx_sh_000990.csv',
 'idx_hw_spx.csv',
 'idx_sz_399106.csv',
 'idx_hw_n225.csv',
 'idx_sz_399550.csv',
 'stk_sh_600015.csv',
 'msg_weixin_长赢指数投资.csv',
 'idu_sw1_801710.csv',
 'mcr_vix.csv',
 'idu_sw1_801880.csv',
 'stk_roe20_value.csv',
 'mcr_scn.csv',
 'idx_sz_399812.csv',
 'msg_weibo_1254381361.csv',
 'plt_sha.csv',
 'idx_relevance.png',
 'stk_sh_600660.csv',
 'mcr_c5y.csv',
 'idx_sh_000991.csv',
 'msg_weixin_梧桐拾贝社.csv',
 'idx_hw_hsi.csv',
 'idu_sw1_801210.csv',
 'stk_sh_601877.csv',
 'idx_change.csv',
 'idx_hw_ftse.csv',
 'stk_sh_600016.csv',
 'idx_sz_399989.csv',
 'idx_pool.csv',
 'stk_sh_601229.csv',
 'stk_sz_002294.csv',
 'stk_pool_roe20.csv',
 'stk_sh_600926.csv',
 'idx_sh_000922.csv',
 'idx_sh_000068.csv',
 'idx_sz_399975.csv',
 'stk_pool_gw500.csv',
 'stk_sh_600919.csv',
 'idx_sz_399811.csv',
 'idu_sw1_801770.csv',
 'idx_sz_399986.csv',
 'idx_hw_fchi.csv',
 'stk_sz_002236.csv',
 'stk_sz_002714.csv',
 'idx-img-pbs.png',
 'stk_sh_601939.csv',
 'mcr_pmi.csv',
 'mcr_uch.csv',
 'stk_sz_000661.csv',
 'idu_sw1_801890.csv',
 'idu_sw1_801120.csv',
 'stk_bank_value.csv',
 'idx_sh_000010.csv',
 'idu_sw1_801050.csv',
 'mcr_cpi.csv',
 'idx_sh_000827.csv',
 'idx_sh_000906.csv',
 'msg_weixin_码农滚雪球.csv',
 'stk_sh_600816.csv',
 'idu_sw1_801200.csv',
 'idx_sh_000841.csv',
 'idx-img-qscpb.png',
 'idu_sw1_801740.csv',
 'stk_pool_bank.csv',
 'stk_roe20_change.csv',
 'idx_sz_399001.csv',
 'stk_sz_000688.csv',
 'cmm_oil.csv',
 'stk_sh_601988.csv',
 'idu_sw1_801030.csv',
 'idx_hw_hscei.csv',
 'idx_sh_000016.csv',
 'stk_sz_000333.csv',
 'stk_sz_000001.csv',
 'stk_sz_000538.csv',
 'msg_weibo_1669616825.csv',
 'plt_value.csv',
 'fnd_pool_index.csv',
 'cmm_xau.csv',
 'idx_sz_399101.csv',
 'idx_sz_399324.csv',
 'idx_hw_sx5e.csv',
 'idu_sw1_801750.csv',
 'idu_sw1_801780.csv',
 'mcr_ms.csv',
 'idx_sh_000902.csv',
 'stk_sz_002142.csv',
 'stk_sh_600908.csv',
 'stk_sh_601398.csv',
 'idx_sh_000993.csv',
 'stk_sz_002081.csv',
 'idu_sw1_value.csv',
 'cmm_gor.csv',
 'stk_sz_000651.csv',
 'mcr_pool.csv',
 'stk_sh_600000.csv',
 'idx_sh_000300.csv',
 'idu_sw1_801140.csv',
 'stk_sh_601997.csv',
 'idx_sz_399967.csv',
 'stk_sh_601288.csv',
 'idx_hw_ndaq.csv',
 'idx-img-zj.png',
 'stk_sh_601998.csv',
 'msg_weixin_股市药丸.csv',
 'stk_sh_603288.csv',
 'stk_sh_600690.csv',
 'idx_sz_399005.csv',
 'plt_cyb.csv',
 'mcr_shibor.csv',
 'cmm_pool.csv',
 'idu_sw1_801020.csv',
 'idx_sh_000009.csv',
 'stk_sh_601169.csv',
 'stk_sh_603323.csv',
 'stk_sh_600201.csv',
 'idx_sh_000001.csv',
 'mcr_c10y.csv',
 'plt_sza.csv',
 'idx_sh_000998.csv',
 '.ipynb_checkpoints',
 'idu_sw1_801170.csv',
 'stk_pool_edticket.csv',
 'idx_sh_000807.csv',
 'stk_sh_603898.csv',
 'idx_sh_000992.csv',
 'stk_sz_000423.csv',
 'plt_zxb.csv',
 'idx_sz_399997.csv',
 'idx_sz_399624.csv',
 'cmm_xag.csv',
 'idx_sz_399006.csv',
 'idx_sh_000905.csv',
 'stk_sh_601515.csv',
 'mcr_ppi.csv',
 'stk_sz_000963.csv',
 'plt_hsa.csv',
 'idx_sh_000932.csv',
 'msg_weixin_阿甘数量化2.csv',
 'idx_sz_399808.csv',
 'idx_sz_399673.csv',
 'idx_sh_000925.csv',
 'stk_sh_601128.csv',
 'stk_sz_002271.csv',
 'idu_sw1_801790.csv',
 'msg_weibo_5687069307.csv',
 'idx_sh_000904.csv',
 'plt_szb.csv',
 'plt_pool.csv',
 'mcr_nfc.csv',
 'msg_xqft_4776750571.csv',
 'stk_sz_002508.csv',
 'idu_sw1_801010.csv',
 'stk_sz_002032.csv',
 'idx_sh_000903.csv',
 'idu_pool_sw1.csv',
 'stk_sh_600276.csv',
 'idu_sw1_801730.csv',
 'idx_sh_000852.csv',
 'idx_sh_000986.csv',
 'stk_sh_600340.csv',
 'cmm_change.csv',
 'idx_sh_000988.csv',
 'idx_sh_000978.csv',
 'idx_sz_399396.csv',
 'stk_sh_600519.csv',
 'stk_sz_000049.csv',
 'idx_hw_djia.csv',
 'idx_sz_399971.csv',
 'idx_sz_399102.csv',
 'idu_sw1_801230.csv',
 '网格-交易A.xlsm',
 'mcr_gdp.csv',
 'idx_sh_000985.csv',
 'stk_sz_002372.csv',
 'idx_sz_399806.csv',
 'stk_sz_002304.csv',
 'idx_sz_399330.csv',
 'stk_sh_601009.csv',
 'stk_sh_600612.csv',
 'stk_sz_000002.csv',
 'mcr_ucy.csv',
 'idx-img-pes.png',
 'idx_hw_gdaxi.csv',
 'idu_sw1_801040.csv',
 'plt_change.csv',
 'idx_sz_399814.csv',
 'idu_sw1_801160.csv',
 'idx_value.csv',
 'idu_sw1_801720.csv']

cookies=get_cookies()

for fn in file_list:

    

    try:
        print(fn)
        if fn.endswith("png"):
            url="https://www.joinquant.com/user/22486821351/view/Data/%s"%(fn)
            # r=requests.get(url,cookies=cookies,headers=header)
            # print(r)
            # data=r.content
            # # print(data)
            # with open('Data/%s'%(fn), "wb") as f:
            #     f.write(data)
        elif fn.endswith("csv"):
            url="https://www.joinquant.com/user/22486821351/api/contents/Data/%s?type=file&format=text&_=1580445911713"%(fn)
            r=requests.get(url,cookies=cookies,headers=header)
            data=json.loads(r.text).get('content')
            print(fn)
            with open('Data/%s'%(fn), "w", encoding='utf-8') as f:
                f.write(data)

        
    except:
        print(fn)


# url="https://www.joinquant.com/user/22486821351/notebooks/Project/%E5%95%86%E5%93%81-%E4%BB%B7%E5%80%BC%E5%88%86%E6%9E%90.ipynb"
# r=requests.get(url,cookies=cookies,headers=header)    
# print(r)
# data=r.text
# print(data)
# with open('Data/%s'%("fn"), "wb") as f:
#     f.write(data)        