import requests
from bs4 import BeautifulSoup
import time
from numpy import *
import csv

#深圳各行政区路由
districts=['luohuqu','futianqu','nanshanqu','yantianqu','baoanqu','longgangqu','longhuaqu','guangmingqu','pingshanqu','dapengxinqu']

#行政区中文名
districts_cn=['罗湖区','福田区','南山区','盐田区','宝安区','龙岗区','龙华区','光明区','坪山区','大鹏新区']

#设置请求头
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
}

#源地址
s_url='https://sz.lianjia.com/zufang/'

price_dic={}
pro=0
t_pro=0

#对每个行政区的租房信息进行爬取
for item in districts:
    #获取当前行政区房源页数
    url=s_url+item
    text=requests.get(url,headers=headers).text
    soup=BeautifulSoup(text,'html.parser')
    pages=soup.select('.content__pg')[0].attrs['data-totalpage']
    pages=eval(pages)
    
    ls=[]

    #爬取每一页
    for page in range(1,pages+1):
        p_url=url+'/'+f'pg{page}'

        p_text=requests. get(p_url,headers=headers).text

        p_soup=BeautifulSoup(p_text,'html.parser')

        prices=p_soup.select('.content__list .content__list--item-price em')
        
        #将价格由字符串型转换为数字型
        for i in prices:
            price=i.string.strip() 
            price=price.split('-')[0]
            ls.append(eval(price)) 
            print(price)
        
        #计算进度
        pro=page/(pages+1)/10*100
        pro+=t_pro
        print('\r爬取进度：{:.2f}%'.format(pro),end='')
        
        # time.sleep(0.5)
    t_pro=pro

    price_dic[item]=ls

#计算各区平均价格
average_prices={}
for i in range(10):    
    average_prices[districts_cn[i]]=mean(price_dic[districts[i]])

#将结果以csv格式储存
f=open('lianjia.csv','w',encoding='utf-8')
csv_writer=csv.writer(f)
csv_writer.writerow(['Area','Price'])

for i in average_prices:
    csv_writer.writerow([i,average_prices[i]])

f.close()

#输出信息
print('深圳市各区月租房平均价格：')
print(average_prices)
