import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Google():
    def __init__(self, query=''):
        self.google_url = 'https://www.google.com.tw/search'
        self.query = query
        self._params = {'q': self.query}
        self.flag, self.soup = self.parse_html()
        if self.flag:
            self.extract_name()
            self.extract_stars()
        else:
            self.name = ''
            self.stars= float(-5)
    def parse_html(self):
        r = requests.get(self.google_url, params= self._params)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            return True, soup
        else:
            return False, '' 
    def extract_name(self):
        try:
            items = self.soup.select_one('div.BNeawe.deIvCb.AP7Wnd') 
            self.name = items.text if len(items) > 0 else ''
        except:
            self.name = ''
    def extract_stars(self):
        try:
            items = self.soup.select_one('div.BNeawe.tAd8D.AP7Wnd > span.r0bn4c.rQMQod.tP9Zud > span.oqSTJd')
            self.stars = float(items.text)
        except:
            self.stars = float(-5)
'''
test = Google(query='彰化 HouseV 好室鍋物 冷藏肉專門店')
print(test.name, test.stars)
test1 = Google(query='高雄-精緻推車飲茶-國賓飯店')
print(test1.name, test1.stars)
test2 = Google(query='台中西屯 笨豬跳。美式韓風汽油桶燒肉~~~')
print(test2.name, test2.stars)
test3 = Google(query='*宜蘭市女中路美食推薦*六眷村麻辣鴛鴦')
print(test3.name, test3.stars)
test4 = Google(query='台北大安 超CP值的初魚 鐵板燒')
print(test4.name, test4.stars)
test5 = Google(query='板橋：永昌牛肉麵  紅燒清燉都美味')
print(test5.name, test5.stars)
'''
