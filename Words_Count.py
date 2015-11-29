#-*- coding:utf-8 -*-
import os
import re
import sys
import time
reload(sys)
sys.setdefaultencoding("utf8")
file_path = r"E:\EnglishComplete\src.txt"
def min(x,y):
    if x < y:
        return x
    return y
def Get_All_Files(path):
    try:
        if not os.path.exists(path):
            return []
        else:
            rs = []
            subdirs = os.listdir(path)
            for subdir in subdirs:
                temp = os.path.join(path,subdir)
                if os.path.isfile(temp) and temp.endswith('.txt'):
                    rs.append(temp)
            return rs
    except Exception,e:
        print e
        return []

def Read_File(file_path):
    try:
        fileobj = open(file_path,'r')
        lines = fileobj.read()
        fileobj.close()
        lines = lines.replace('\r','')
        lines = lines.replace('-\n','')
        lines =lines.replace('\n',' ')
        return lines
    except Exception,e:
        print e
        return ""
def Format(line):
    reobj = re.compile("[a-z]+",re.IGNORECASE)
    results = []
    rs = re.search(reobj,line)
    while rs:
        temp = rs.group().lower()
        if len(temp) > 2:
            results.append(temp)
        #print results
        line = line[rs.end():]
        rs = re.search(reobj,line)
    return ','.join(results)

words_counts = {}
def Append(line):
    words = line.split(',')
    for word in words:
        if len(word) > 2:
            if word in words_counts.keys():
                words_counts[word] += 1
            else :
                words_counts[word] = 1

def sort_by_values(words_counts):
    new_count = sorted(words_counts.items(), key=lambda d: d[1],reverse=True)
    return new_count
def Output(file_path,word,cnt):
    try:
        fp = open(file_path,'a')
        fp.write(word + ":" + str(cnt) + "\n")
        fp.close()
    except Exception,e:
        print e
def Create(path):
    try:
        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)
            return True
    except Exception,e:
        print e
        return False
        
if "__main__" == __name__:
    rootdir = os.path.split(__file__)[0]
    all_files = Get_All_Files(os.path.join(rootdir,"input"))
    for f in all_files:
        print "process %s"%(f)
        txt = Read_File(f)
        line = Format(txt)
        Append(line)
    new_words_counts = sort_by_values(words_counts)
    
    now = time.localtime()
    today_str = time.strftime("%Y-%m-%d",now)
    time_str = time.strftime("%H_%M_%S",now)
    #create path
    output = os.path.join(rootdir,"output",today_str,time_str)
    if Create(output):
        time.sleep(5)
        for i in range(len(new_words_counts)):
            #every day 100 words
            dayIndex = int(i / 100) + 1
            name = "day%s words%s-%s.txt"%(str(dayIndex),str((dayIndex - 1)*100 + 1),str(min(dayIndex*100,len(new_words_counts))))
            file_name = os.path.join(output,name)
            Output(file_name,new_words_counts[i][0],new_words_counts[i][1])
        print "all the output --> %s"%(output)
    else:
        print "can not create path %s"%(output)