# -*- encoding:utf-8 -*- 
import urllib2,urllib,os,re
import cookielib
from collections import OrderedDict
import Color
class douban:
    def __init__(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
        urllib2.install_opener(opener)
        self.url = 'https://www.douban.com/accounts/login'
        self.info = {"source":"index_nav",
                "form_email":"fztfztfzt@qq.com",
                "form_password":"fzt782879714",
                'remember':"on"}
        res = urllib2.urlopen(self.url)
        self.ans = res.read()
    
    def hasCaptcha(self,str):
         match = re.match(r'.*<img id="captcha_image" src="(.*)&.*" alt="captcha" class="captcha_image"',str,re.S)
         if match is not None:
             return match.group(1)
         else :
             return None

    def connect(self):
        captcha = self.hasCaptcha(self.ans)
        if captcha != None:
            print captcha
            match = re.match(r'.*id=(.*)',captcha)
            id = match.group(1)
            print id
            res2=urllib2.urlopen(captcha)
            f = open('douban.jpg',"wb")
            f.write(res2.read())
            f.close()
            captcha_image = raw_input("input ans:")
            self.info['captcha-solution']=captcha_image
            self.info['captcha-id']=id
        data = urllib.urlencode(self.info)
        res = urllib2.urlopen(self.url,data)
        f2 = open('douban.html','wb')
        self.ans = res.read()
        if 'form_email' in self.ans:
            self.info['user_login']="登录"
            self.connect()
        else :
            f2.write(self.ans)

    def search(self):
        query = raw_input("请输入查询内容：".decode('utf-8').encode('gbk'))
        url = "http://www.douban.com/search?source=suggest&q="+query
        ans = urllib2.urlopen(url)
        result = ans.read()
        f = open('search.html','wb')
        f.write(result)
     
        match = re.findall(r'<span>\[(.*?)\]</span>.*? >(.*?)</a>.*?<span class="rating_nums">(.*?)</span>.*?<span>(.*?)</span>.*?<span class="subject-cast">(.*?)</span>.*?<p>(.*?)</p>',result,re.S)
        print len(match)
        for submatch in match:
            content = OrderedDict()
            content[u"类别"]=submatch[0].decode('utf-8')
            content[u"名称"]=submatch[1].decode('utf-8')
            content[u"评分"]=submatch[2].decode('utf-8')
            content[u"评价人数"]=submatch[3].decode('utf-8')
            content[u"说明"]=submatch[4].decode('utf-8')
            content[u"简介"]=submatch[5].decode('utf-8')
            for i in content:
                Color.setTextColor(Color.FOREGROUND_PINK)
                print i,
                Color.setTextColor(Color.FOREGROUND_BLUE)
                print content[i].encode('GB18030')
                Color.resetColor()
            print ''

if __name__ == "__main__":
    dou = douban()
    #dou.connect()
    dou.search()
   

