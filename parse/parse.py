# -*- coding:utf8 -*-

import re
import os

def shell():
    rules=regular("../rules1.txt") #{'left_symbol':{'right str'..}..}
    parse(rules)

def regular(inputF):
    rules={}
    srcRules=open(inputF, 'r').read().split('\n')
    #pass 1:去重，去除epsilon产生式
    for rulei in srcRules:
        tokenL=re.split('->',rulei)

        key=tokenL[0]
        value=tokenL[1]
        rightSymL=value.split(' ')
        while '-NONE-' in rightSymL:
            rightSymL.remove('-NONE-')
        if len(rightSymL)!=0:
            value=' '.join(rightSymL)
            rules[key]=rules.get(key,set())
            rules[key].add(value)
        #print(tokenL)
    if '-NONE-' in rules:
        del rules['-NONE-']

    #pass 2 对和终结符一样的非终结符进行转义
    for keyi in list(rules.keys()).copy():
        right=rules[keyi]
        for righti in right.copy():
            if righti==keyi:
                newKey='NT'+keyi
                rules[newKey]=set()
                rules[newKey].add(righti)
                rules[keyi].remove(righti)
        if len(right)==0:
            del rules[keyi]
    #print(rules)
    #pass 3 转换成CNF
    keys=list(rules.keys())
    for keyi in keys:
        rSet=rules[keyi]
        for rightStr in rSet:
            rightSymL=rightStr.split(' ')
            if len(rightSymL)>2:
                rSet.remove(rightStr)
                newSym='_'.join(rightSymL[1:])
                rSet.add(' '.join([rightSymL[0],newSym]))
                newSymL=newSym.split('_')
                while len(newSymL)>1:
                    rules[newSym]=rules.get(newSym,set())
                    nextNewSym='_'.join(newSymL[1:])
                    newRightStr=' '.join([newSymL[0],nextNewSym])
                    rules[newSym].add(newRightStr)
                    del newSymL[0]
                    newSym=nextNewSym
            else:
                pass
    #print(rules)
    return rules

def parse(rules):
    print(rules)
    for i in range(1,2):
        fNum='{}{}{}{}'.format(i//1000%10,i//100%10,i//10%10,i%10)
        inputF="../Data/treebank/raw/wsj_{}".format(fNum)
        outputF="./parsed/wsj_{}.out".format(fNum)

        os.makedirs('./parsed/',exist_ok=True)
        file=open(outputF, 'w')
        sentences=open(inputF,'r').read().split('\n')[1:]
        while '' in sentences:  sentences.remove('')
        for sentence in sentences:
            synTree=parseSentence(sentence,rules)
            printTree(synTree,file)
            #print(sentence)

def parseSentence(sentence,rules):
    sLen=len(sentence)
    # pass 1:词法分析,写成终结符序列.最大前向匹配
    terminal=[]
    l=0
    wordUnkown=''
    flag=False
    symbolSet=symbols(rules)
    #print(symbolSet)
    while l<sLen:
        r=sLen
        while r>l:
            if sentence[l:r] in symbolSet:
                terminal.append(sentence[l:r])
                wordUnkown=wordUnkown.replace(' ','')
                if len(wordUnkown)>0 :
                    print('tokenizer meet unrecognized word: $'+wordUnkown+'$')
                    print('before '+sentence[l:r])
                    wordUnkown=''
                    flag=True
                break
            r=r-1
        if r==l:
            wordUnkown=wordUnkown+sentence[l:l+1]
            l=l+1
        else: l=r
    wordUnkown =wordUnkown.replace(' ', '')
    if len(wordUnkown)>0:
        print('tokenizer meet unrecognized word: '+wordUnkown)
        flag=True

    print('\nTOKEN LIST DUMP:')
    print(terminal)
    print()

    if flag:
        print('drop sentence due to word segmentation failure:\n'+sentence)
        return []

    return terminal

    N=len(terminal)
    #pass 2 建立状态表,初始化叶子结点
    V=[[None]*N]*N
    for i in range(N):
        pass


def printTree(synTree,file):
    return
    file.write(synTree+'\n')
    print(synTree)

def key(dic,value):
    return list(dic.keys())[list(dic.values()).index(value)]

def symbols(rules):
    ret=set()
    for keyi in list(rules.keys()):
        for symbol in rules[keyi]:
            ret.add(symbol)
    return ret

if __name__ == '__main__':
    shell()

