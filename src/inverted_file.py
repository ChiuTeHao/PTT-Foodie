import numpy as np
import json
import re
import jieba
from collections import Counter

class IF():
    def __init__(self, path='../data/Food-2010-7010.json'):
        self.path = path
        with open(self.path, 'r') as f:
            content = json.loads(f.read(), encoding='utf-8')['articles']
        self.content = [content[i] for i in range(len(content)) if "article_id" in content[i]]
        self.id_list = [self.content[i]["article_id"] for i in range(len(self.content))]
        self.title_list = [self.content[i]["article_title"] for i in range(len(self.content))]
        assert(len(self.id_list) == len(self.title_list) == len(self.content))
        self.num_of_docs = len(self.id_list)  #99745 docs
    
    def clean_data(self):
        self.inverted_file = {}
        for i in range(self.num_of_docs):
            if not self.title_list[i] or '[食記]' not in self.title_list[i]:
                continue
            content_cnt = Counter()
            _id = self.id_list[i]
            char = '[a-zA-ZＡ-Ｚ0-9’!"#$%&\'()*+,-./:;<=>?@，。?：；（）★、…【】《》？“”‘’！[\\]^_`{|}~]+'
            split_sen = [mini_sen for mini_sen in re.sub(char, ' ', self.content[i]["content"]).split() if mini_sen]
            bigram_list = []
            for mini_sen in split_sen:
                for words in list(jieba.cut(mini_sen)):
                    bigram_list.append(words)
                    '''
                    else:
                        for j in range(len(words)-1):
                            sub = ''.join(words[j:j+2])
                            bigram_list.append(sub)
                    '''
            content_cnt.update(bigram_list)
            for (word, freq) in content_cnt.items():
                if word not in self.inverted_file:
                    self.inverted_file[word] = []
                self.inverted_file[word].append({_id: freq})
            
            ''' for debugging
            print(split_sen, len(split_sen))
            print(content_cnt)
            print('-----------------------')
            '''
        
        print('Totally {} words in the inverted file.'.format(len(self.inverted_file)))

    def save_to_json(self):
        outfile = '../data/inverted_file.json'
        print('Write {} words into the inverted file'.format(len(self.inverted_file)))
        s = json.dumps(self.inverted_file, ensure_ascii=False, separators=(',\n',':'))
        
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(s)
        print('Finish writing to json file.')
        
    def load_inverted_file(self, if_path='../data/inverted_file.json'):
        
        print('-------------------------------------------------------')
        print('Loading the inverted file from path: {}'.format(if_path))
        with open(if_path, 'r') as f:
            inverted_file = json.loads(f.read(), encoding='utf-8')
        print('length of inverted file: {}'.format(len(inverted_file)))
        print('Loading finished.')

data = IF()
data.clean_data()
data.save_to_json()
#data.load_inverted_file()
