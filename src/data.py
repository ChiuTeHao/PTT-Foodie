import numpy as np
import json
from google import Google
import time
class Data():
    def __init__(self, path='../data/Food-2010-7010.json', location_path='../data/location.json'):
        self.path = path
        self.location_path = location_path
        with open(self.path, 'r') as f:
            content = json.loads(f.read(), encoding='utf-8')['articles']
        self.content = [content[i] for i in range(len(content)) if "article_id" in content[i]]
        self.id_list = [self.content[i]["article_id"] for i in range(len(self.content))]
        self.title_list = [self.content[i]["article_title"] for i in range(len(self.content))]
        assert(len(self.id_list) == len(self.title_list) == len(self.content))
        self.num_of_docs = len(self.id_list)  #99745 docs
        
        self.parse_location()
        self.get_stars_and_name()
        self.save_to_json()
    
    def parse_location(self):
        with open(self.location_path, 'r') as f:
            location = json.loads(f.read(), encoding='utf-8') #{"loc_1":[mid_loc of loc_1....]}
        main_location = [key for key, value in location.items()]
        #### Determin the main & mini location
        count = 0
        for i in range(self.num_of_docs):
            if not self.title_list[i] or '[食記]' not in self.title_list[i]:
                continue
            _title = self.title_list[i].replace("臺","台").strip('[食記]').strip(' ').strip('Re:').strip('Fw:')
            tmp_dict = {}
            for main in main_location:
                if main in _title:
                    tmp_dict['main_location'] = main
                    break
            for mini_list in list(location.values()):
                for mini in mini_list:
                    if mini in _title: 
                        tmp_dict['mini_location'] = mini
                        if "main_location" not in tmp_dict:
                            tmp_dict["main_location"] = list(location.keys())[list(location.values()).index(mini_list)]
            self.content[i].update(tmp_dict)
    
    def get_stars_and_name(self):
        with open('./tmp.txt', 'w') as f:
            f.write('Start Crawling.\n')
        #self.num_of_docs
        for i in range(self.num_of_docs):
            if not self.title_list[i] or '[食記]' not in self.title_list[i]:
                continue
            _title = self.title_list[i].replace("臺","台").strip('[食記]').strip(' ').strip('Re:').strip('Fw:')
            tmp_dict = {}
            tmp_obj = Google(query=_title)
            tmp_dict['store_name'] = tmp_obj.name
            tmp_dict['stars'] = tmp_obj.stars
            print(i, tmp_obj.name, tmp_obj.stars)
            w_str = '{}_{}_{}'.format(i, tmp_obj.name, tmp_obj.stars)
            with open('./tmp.txt', 'a') as f:
                f.write(w_str)
                f.write('\n')
            self.content[i].update(tmp_dict)
            time.sleep(1)
    
    def save_to_json(self):
        
        outfile = '../data/Food-final.json'
        out_dict = {}
        print('Write {} of docs to output:'.format(len(self.content)))
        out_dict['articles'] = self.content
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(u'{"articles": [')
        for i in range(self.num_of_docs):
            s = json.dumps(self.content[i], ensure_ascii=False, separators=(',', ':'))
            with open(outfile, 'a', encoding='utf-8') as f:
                f.write(s)
                if i != self.num_of_docs-1:
                    f.write(',\n')
        with open(outfile, 'a', encoding='utf-8') as f:
            f.write(u']}')
        print('Finish writing json file.')

data = Data()
        
