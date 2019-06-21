import json
import math
import jieba
import os
class SearchEngine:
    def __init__(self):
        self.k1=1
        self.b=0.75
        self.datapath=os.path.join(os.path.join(os.getcwd(),os.pardir),'data')
        self.doccnt,self.doclendic,self.avgdoclen=self.getDocLen()
        with open(os.path.join(self.datapath,'inverted_file.json'),'r') as f:
            self.worddic=json.load(f)
        with open(os.path.join(self.datapath,'docnametoidx.json'),'r',encoding='utf-8') as f:
            self.docidxtable=json.load(f)
        with open(os.path.join(self.datapath,'Food-final.json'),'r') as f:
            self.doclist=json.load(f)['articles']
        with open(os.path.join(self.datapath,'location.json'),'r',encoding='utf-8') as f:
            self.locdic=json.load(f)
    def cutQuery(self,query):
        word=[]
        '''for i in range(len(query)-1):
            word.append(query[i]+query[i+1])'''
        words=jieba.cut(query,cut_all=False)
        word=list(words)
        '''for result in words:
            if len(result)>2:
                for i in range(len(result)-1):
                    word.append(result[i:i+2])
            else:
                word.append(result)'''
        return word
    def parseLocation(self,query):
        mainloc=None
        miniloc=None
        for main in self.locdic.keys():
            if main in query:
                mainloc=main
                for mini in self.locdic[mainloc]:
                    if mini in query:
                        miniloc=mini
        if mainloc==None:
            for main in self.locdic.keys():
                for mini in self.locdic[main]:
                    if mini in query:
                        mainloc=main
                        miniloc=mini
                        break
                if mainloc != None:
                    break
        return mainloc,miniloc
    def getDocLen(self):
        doclendic=dict()
        with open(os.path.join(self.datapath,'documentlength'),'r') as f:
            lines=f.readlines()
            doccnt=int(lines[0])
            avgdoclen=float(lines[-1])
            del(lines[0])
            del(lines[-1])
            for line in lines:
                tmp=line.split()
                doclendic[tmp[0]]=float(tmp[1])
        return doccnt,doclendic,avgdoclen
    def printResult(self,results,printStar=False):
        for result in results:
            idx=self.docidxtable[result[0]]
            print(self.doclist[idx]['article_title'])
            if printStar==True:
                print(self.doclist[idx]['stars'])
    def BM25(self,queryword):
        scores=dict()
        print(queryword)
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
        tmpresults=sorted(scores.items(),key=lambda x:x[1],reverse=True)
        maxscore=tmpresults[0][1]
        base=tmpresults[19][1]
        results=[]
        for tmpresult in tmpresults[:20]:
            results.append((tmpresult[0],(tmpresult[1]-base)/(maxscore-base)))
        return results[:20]
    def rank(self,query):
        queryword=self.cutQuery(query)
        mainloc,miniloc=self.parseLocation(query)
        ranklist=[]
        results=self.BM25(queryword)
        mainlocsim=[]
        minilocsim=[]
        newresults=[]
        for result in results:
            idx=self.docidxtable[result[0]]
            ranklist.append(self.doclist[idx])
            locscore=0
            starscore=0
            if mainloc != None and 'main_location' in self.doclist[idx] and mainloc in self.doclist[idx]['main_location']:
                mainlocsim.append(1)
                locscore+=10
            else:
                mainlocsim.append(0)
            if miniloc!= None and 'mini_location' in self.doclist[idx] and  miniloc in self.doclist[idx]['mini_location']:
                minilocsim.append(1)
                locscore+=5
            else:
                minilocsim.append(0)
            if 'stars' in self.doclist[idx] and self.doclist[idx]['stars']>=0:
                starscore=self.doclist[idx]['stars']
            else:
                starscore=0
            newresults.append((result[0],result[1]+locscore+starscore/5,starscore))
        newresults=sorted(newresults,key=lambda x:x[1],reverse=True)
        self.printResult(results)
        print('==============================================')
        self.printResult(newresults[:10])
        return newresults[:10]
