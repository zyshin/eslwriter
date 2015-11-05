from django.conf import settings


def convert_parsed(text):
    sentenceCount=0
    termLineList=[]
    pairsLineList=[]
    outputText=''
    for line in text.split('\n'):	
        if not line.strip():
            if termLineList:
                outputText+=str(len(termLineList))+' '+str(len(pairsLineList))+'\r\n'
                outputText+='\r\n'.join(termLineList)+'\r\n'
                outputText+='\r\n'.join(pairsLineList)
                outputText+='\r\n'
                termLineList=[]
                pairsLineList=[]	
                sentenceCount+=1
        else:
            cellList=line.split()
            termLineList.append(cellList[1]+' '+cellList[2]+' '+cellList[3])
            if cellList[5]!='0' and cellList[6]!='punct':
                pairsLineList.append(cellList[6]+' '+cellList[5]+' '+cellList[0])
    outputText=str(sentenceCount)+'\r\n'+outputText
    return outputText


def build_all():
    # with open(path, 'r') as fin:
    #     corpora = fin.read().split()
    from corpus_building.build import build_corpus
    from datetime import datetime
    import gc
    dbc = settings.DBC
    for c in list(dbc.common.corpora.find()):
        cid = c['db']
        if dbc.sentences[cid].count():
            continue
        print datetime.now(), cid
        build_corpus(cid, False)
        gc.collect()
