#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request
import re



import urllib.parse
import http.cookiejar#用来保存cookie
from urllib.parse import urlencode


# 1. 淘宝图片爬虫实战




form_data = {'TPL_username':'17600660311'
,'TPL_password':''
,'ncoSig':''
,'ncoSessionid':''
,'ncoToken':'9198437b873d5f6901d732c7c453ac104777948e'
,'slideCodeShow':'false'
,'useMobile':'false'
,'lang':'zh_CN'
,'loginsite':'0'
,'newlogin':'0'
,'TPL_redirect_url':'https://s.taobao.com/search?q=%E5%A4%A7%E6%95%B0%E6%8D%AE&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=0&p4ppushleft=1%2C48&s=88'
,'from':'tb'
,'fc':'default'
,'style':'default'
,'css_style':''
,'keyLogin':'false'
,'qrLogin':'true'
,'newMini':'false'
,'newMini2':'false'
,'tid':''
,'loginType':'3'
,'minititle':''
,'minipara':''
,'pstrong':''
,'sign':''
,'need_sign':''
,'isIgnore':''
,'full_redirect':''
,'sub_jump':''
,'popid':''
,'callback':''
,'guf':''
,'not_duplite_str':''
,'need_user_id':''
,'poy':''
,'gvfdcname':'10'
,'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323330722E312E3735343839343433372E372E353630653662613949543779306926663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246732E74616F62616F2E636F6D25324673656172636825334671253344253235453525323541342532354137253235453625323539352532354230253235453625323538442532354145253236696D6766696C65253344253236636F6D6D656E64253344616C6C2532367373696425334473352D652532367365617263685F747970652533446974656D253236736F75726365496425334474622E696E64657825323673706D253344613231626F2E323031372E3230313835362D74616F62616F2D6974656D2E31253236696525334475746638253236696E69746961746976655F69642533447462696E6465787A5F323031373033303625323662636F6666736574253344302532366E746F666673657425334430253236703470707573686C6566742533443125323532433438253236732533443838'
,'from_encoding':''
,'sub':''
,'TPL_password_2':'696249364a71e25a39be731e01162e538faec666e59ddc84fdd473ca9ed48fbc0523c98163b86aa4e5a74adf1c9b38a13e828fdd039ee039c0498b08680100f7247b6f422e9482a4bf127c22554de09bb0994315cafc33a79b4783a3fc2a47c532d40263874ebb24ae836f39b3a36a2bb9ad0e8f9dbf01e674875ef0204e713d'
,'loginASR':'1'
,'loginASRSuc':'1'
,'allp':''
,'oslanguage':'zh-CN'
,'sr':'1920*1080'
,'osVer':''
,'naviVer':'chrome|76.03809132'
,'osACN':'Mozilla'
,'osAV':'5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
,'osPF':'Win32'
,'miserHardInfo':''
,'appkey':'00000000'
,'nickLoginLink':''
,'mobileLoginLink':'https://login.taobao.com/member/login.jhtml?redirectURL=https://s.taobao.com/search?q=%E5%A4%A7%E6%95%B0%E6%8D%AE&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=0&p4ppushleft=1%2C48&s=88&useMobile=true'
,'showAssistantLink':''
,'um_token':'T608132E6B5E0CCBBE2DFB2386E18D3BCEF26C806A55891843AEC00A339'
,'ua':'120#bX1bSTYL1gI2SrSbjbYoGsufbco3+edD2o/f+3tB79ik8CJNmZhBs20fP8OpzoJLWZJBW5She+JUSIV0gDnv9LSIGRk01JEk0kDaK5MfAWhOUHFZAXJT6/OMpuGHf7PEhit6+JASmHDKcmuUJqtHxmiJ9jSPb9Z0xWmoGDZ6OwqC5FF+vnTm8s0XYlQ7MPXN144xX1zvo/GEEh6IcRsBDnXbBtVDNadHrVsNwrAkMqpO69P5p6MwwZptYv7nHOdxdDOEq+M0tteQFnWmkVfxPbYb0lq1WqPVEvYb7grPNWIBbbTt1sydyXlWS5hcWqe/yTTS7UwPitc/bEnbb7PyyXIbngvpWqMLib55FRrPWPc/bbSNQeMPxcDb3LA4yee/ybbC7UBPWWl/bbYt7S9iaSXrSeaayivVSxtkOyzBzhYea80lO3AV02bR5+WldM73MeQ3XLOMlCQ8ooMCcuFenT9lFaA/YSh0EL0vVVlMP4EFHvO49MXnQv8Yt9suqWSsnF1uLBYGVS0zAwDxwoKfphL/r1qQ2loc9wPhvAwoWntpkdsXP97KfRJO7ai0PcTOjzim2qCMi59P7pNXwWYnjL1JnG/7hOQp2vvp/4xwPDeiVLSxHpB7dPFmlc3+loMuROLRhdIlyz1ejmHyCebyKbrZPyDmFWgMsv+sEF4owaKMDjnooLmPdF+qIvhXcR0XycRwKwY+/S6qoociXKsgbpJTtC3TP2OAldN4d1Mpc/Acb4ewePqAPIalH2fNN0djUm/xlD+Olp/w6eqLKWZFwTga/MIBzjkCmn1ZsRSifIER68rk3md+pF9myrtcYF3iFhKcoN8xrPa8lwdDmL9YM+acPnA5qaWetHaBrmjupQ5q4zJWAv8L4wwNiPlvZW0MUnAUGuxX/QPw6aLI9drfdZlDcNoQNkKhRsBbvG98bnOzaQMu1Na4+QvCB4fe3RubuOHvWkKlnNbVpwbENQLs/ICKqn92my5650dsEOJVcOBT/4hu3gqpFNkQac6HyIMqPowpTWtC7lMvfWhj7zM8SoLJLnexqlmbkkDuvNm3x98U2c6vgoko4r11+tJ0CQSJG4nRnTbPSDHi2lZHj1E3xIS3t4mAbeCWiUBdYsA0vVSLFuM6yDyzdasMtpHPcGf3G6zZGR8wcejFglA4WRsqU6s6Z5pKEnIzuRwZ6Wj/SZO2IVS6w2aePfr3B1Us+EEPbYJnRNvrY9+lSToNGGqUHPJhzwYcADUnEpeeRfUWeGX+4y012n2qQL6VnNoK6ZKsVyFvYepX7WqFKAeh08za31pQBJyRKaAq5/W4jXISHhfpvIdHJUmFzHvZPH+KTSo36Cbgpj5fX4uN/iM8CC0OwexRxs+nInSE3/4hYd43A8J+XiyOhLgWZ9Av/KoALvOxADvp06YyBCkjtms4vxgwbsjxgDnPAm4VC1/xD0WX9QILhihfJggW42LQqXMAUR007AvwX/ANu8NVJSiUuVn+kZv4xJA5hkm9tFJ6CeJBwweM6EqHB+2vEQFsPV+LYZyg93SdtWVO9VtHXxdV4zIRnjYYEr4uRjrx0O+wj9gedWzBECyJMQLasvlD3KdqggjNYnS1+fQkOY0Mw27Bvo0wsklC9c1HKUDq3Q1l+bceElCR2MbmP6dgecEoQaxFsWt7nd2bRiCOeOg27mJYqZz+2NTyxJBQGen7VAPkagS/yfxQ2g5R2ys9Q3SVf+ie0D0Z1v=='}


#创建一个cookiejar对象,用来保存cookie
cj = http.cookiejar.CookieJar()

#通过cookiejar创建一个handler
handler = urllib.request.HTTPCookieProcessor(cj)

#根据handler创建一个opener
opener = request.build_opener(handler)

headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')

# 登录url
url = 'https://login.taobao.com/member/login.jhtml?'

# 此url用来检测cookie是否保存成功，验证是否能成功登录
url_t = 'https://www.taobao.com/markets/xie/nvxie/index?spm=a21bo.2017.201867-main.4.5af911d9DO03rO'

form_data = urlencode(form_data).encode()
request0 = request.Request(url, headers)

# 将登录后的cookie信息保存到opener方法中
response = opener.open(request0, data=form_data)

request1 = request.Request(url_t,headers)
# print(request1)
response1 = opener.open(url_t).read()  # open方法中带有cookie信息
# print(response1)
file = open('D:\\Python\\Project\\爬虫\\result\\03-2\\taobao.html','wb')
file.write(response1)
file.close()

request.install_opener(opener)



key_name = '大数据'
key = request.quote(key_name)
# print('key = ' + key)

headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
request.install_opener(opener)

pattern = '"pic_url":"(.*?)"'


j = 6 
for i in range(0,1):
    # url = 'https://s.taobao.com/search?q='+ key + '&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190903&ie=utf8&bcoffset=' + str(j) + '&ntoffset=' + str(j) + '&p4ppushleft=1%2C48&s=' + str(i*44) 
    url = 'https://s.taobao.com/search?q='+ key + '&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=' + str(j) + '&ntoffset=' + str(j) + '&p4ppushleft=1%2C48&s=' + str(i*44) 

    print(url)
    data = request.urlopen(url).read().decode('utf-8','ignore')
    print(data)
    image_url = re.compile(pattern).findall(data)
    print(image_url)

    file = 'D:\\Python\\Project\\爬虫\\result\\03-2\\test' + str(i) + '.html'
    request.urlretrieve(url,file)


    j -= 3





