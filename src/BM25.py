import json
import math
import jieba
class BM25:
    def __init__(self):
        self.k1=1
        self.b=0.75
        self.doccnt,self.doclendic,self.avgdoclen=self.getDocLen()
        with open('inverted_file.json','r') as f:
            self.worddic=json.load(f)
        with open('docnametoidx.json','r',encoding='utf-8') as f:
            self.docidxtable=json.load(f)
        with open('Food-final.json','r') as f:
            self.doclist=json.load(f)['articles']
    def cutQuery(self,query):
        word=[]
        '''for i in range(len(query)-1):
            word.append(query[i]+query[i+1])'''
        words=jieba.cut(query,cut_all=False)
        for result in words:
            if len(result)>2:
                for i in range(len(result)-1):
                    word.append(result[i:i+2])
            else:
                word.append(result)
        return word
    def getDocLen(self):
        doclendic=dict()
        with open('documentlength','r') as f:
            lines=f.readlines()
            doccnt=int(lines[0])
            avgdoclen=float(lines[-1])
            del(lines[0])
            del(lines[-1])
            for line in lines:
                tmp=line.split()
                doclendic[tmp[0]]=float(tmp[1])
        return doccnt,doclendic,avgdoclen
    def rank(self,query):
        queryword=self.cutQuery(query)
        scores=dict()
        for word in queryword:
            if word not in self.worddic:
                continue
            df=len(self.worddic[word])
            for dic in self.worddic[word]:
                for docname,freq in dic.items():
                    idf=math.log((self.doccnt-df+0.5)/(df+0.5))
                    tf=(self.k1+1)*freq/(self.k1*(1-self.b+self.b*self.doclendic[docname]/self.avgdoclen)+freq)
                    if docname not in scores:
                        scores[docname]=idf*tf
                    else:
                        scores[docname]+=idf*tf
        results=sorted(scores.items(),key=lambda x:x[1],reverse=True)
        ranklist=[]
        results=results[:10]
        for result in results:
            idx=self.docidxtable[result[0]]
            ranklist.append(self.doclist[idx])
        return ranklist[:10]
