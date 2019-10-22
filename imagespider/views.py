import requests
from urllib import parse
import re,time,random,os
from fake_useragent import UserAgent
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def spider_view(request):
    if request.method == 'GET':
        return render(request, 'imagespider/spider.html')
    elif request.method == 'POST':
        # 搜索的关键字
        name = request.POST.get('name')
        if not name:
            return HttpResponse('Please give me name!')
        # 起始页
        begin = request.POST.get('begin')
        if not begin:
            return HttpResponse('Please give me begin page!')
        # 终止页
        end = request.POST.get('end')
        if not end:
            return HttpResponse('Please give me end page!')
        s = BaiduImageSpider()
        s.run(name,begin,end)

        static_dir = 'static/images/' + name
        dir = os.path.join(settings.BASE_DIR, static_dir)

        dic ={}
        img = []
        for file in os.listdir(dir):
            # filename = '{}/{}'.format(dir,file)
            img.append(file)
        dic['img'] = img
        dic['name'] = name
        print('='*50)
        print(dic)
        return render(request,'imagespider/spider.html',dic)



class BaiduImageSpider(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/index?tn=baiduimage&word={}&pn={}'
        self.i = 1

    def get_ua(self):
        ua = UserAgent()
        agent = ua.random
        return agent

    def get_image(self,url,word):
        html = requests.get(url=url,headers={'User-Agent':self.get_ua()}).text
        pattern = re.compile('"hoverURL":"(.*?)"',re.S)
        # link_list:['http://xxx.jpg','','']
        link_list = pattern.findall(html)
        static_dir = 'static/images/' + word + '/'
        directory = os.path.join(settings.BASE_DIR, static_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)

        for link in link_list:
            filename = '{}{}_{}.jpg'.format(directory, word, self.i)
            self.save_image(link, filename)
            # time.sleep(random.uniform(1,2))
            self.i += 1

    def save_image(self,link,filename):
        try:
            img = requests.get(url=link,headers={'User-Agent':self.get_ua()}).content
            with open(filename,'wb') as f:
                f.write(img)
        except Exception as e:
            print('---error----')
            print(e)

    def run(self,name,begin,end):
        word = name
        begin = int(begin)
        end = int(end)
        for i in range(begin,end+1):
            print(i)
            word_parse = parse.quote(word)
            url = self.url.format(word_parse,i*30)
            self.get_image(url,word)
















































