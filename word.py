import pickle
import re
import math

class Trie:
    # 全部转换为小写存到树里面
    def __init__(self, root={}):
        self.root = root
        self.END = '$'

    def add(self, word):
        # 从根节点遍历单词,char by char,如果不存在则新增,最后加上一个单词结束标志
        word=word.strip()
        word=word.lower()
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node[self.END] = None

    def find(self, word):
        node = self.root
        for c in word:
            if c not in node:
                return False
            node = node[c]
        return self.END in node

    def _forwardMatch(self, string):
        '''
        正向匹配字符串中是否含有单词
        不区分大小写

        eg：asdlovefgh
        先匹配整个串
        如果失败，去掉最后一个字符，再次匹配
        如果成功，前面的部分加入result，后面的部分递归调用

        如果整个串失败，去掉第一个字母，继续调用该函数
        如果没有这个步骤，eg中的字符创将匹配不到单词
        '''
        result = []
        lower_string = string.lower()
        length = len(string)
        index = len(string)
        if(length == 0):
            return []
        while(index > 0):  # 一个字母不算单词
            # print(string[0:index])
            # print(self.find(string[0:index]))
            if(self.find(lower_string[0:index])):
                result.append(string[0:index])
                result.extend(self._forwardMatch(string[index:length]))
                break  # 找到最长匹配后无需继续匹配
            index -= 1
        else:
            return self._forwardMatch(string[1:])
        #print(result)
        return result

    def _reverseMatch(self, string):
        '''
        逆向匹配字符串中是否含有单词
        不区分大小写

        匹配方式与forward相反
        '''
        result = []
        lower_string = string.lower()
        length = len(string)
        index = 0
        if(length == 0):
            return []
        while(index < length):  # 一个字母不算单词
            # print(string[index:length])
            # print(self.find(lower_string[index:length]))
            if(self.find(lower_string[index:length])):
                result.append(string[index:length])
                result.extend(self._reverseMatch(string[0:index]))
                break  # 找到最长匹配后无需继续匹配
            index += 1
        else:
            return self._reverseMatch(string[:-1])
        return result

    def match(self, string):
        # 无论大写小写，都会转换成小写
        lower_string = string.lower()
        result_f = self._forwardMatch(lower_string)
        result_r = self._reverseMatch(lower_string)
        result_r.reverse()
        # 好像是说逆向的效果比正向的好，所以长度一样时优先选择逆向匹配
        length_f=0
        length_r=0

        #计算两种识别覆盖的字母数
        for element in result_f:
            length_f+=len(element)
        for element in result_r:
            length_r+=len(element)

        if length_r > length_f:
            return result_r
        elif length_r == length_f:
            if(len(result_f) > len(result_r)):
                return result_f
            else:
                return result_r
        else:
            return result_f

    def batchMatch(self, string):
        '''
        输入一个字符串
        在函数内部调用self.match函数，获得该字符串内可能存在的拼音

        该函数功能室将前后邻接的拼音合并
        '''
        string = string.lower()
        new_pinyin_list = []  # 要返回的合并后的一个字符串中的拼音列表
        pinyin_list = self.match(string)
        pos_list = self.getSubstrPos(string, pinyin_list)

        # 如果pinyin_list是空列表，说明string中根本没有拼音，直接返回
        if(len(pinyin_list) == 0):
            return pinyin_list

        i = 0
        temp_str = pinyin_list[0]  # 暂存已经扫描的还没有添加进result的拼音串
        while i + 1 < len(pinyin_list):
            if pos_list[i] + len(pinyin_list[i]) == pos_list[i + 1]:
                temp_str += pinyin_list[i + 1]
            else:
                new_pinyin_list.append(temp_str)
                temp_str = pinyin_list[i + 1]
            i += 1
        if temp_str != "":
            new_pinyin_list.append(temp_str)
        return new_pinyin_list

    def getSubstrPos(self, string, pinyin_list):
        # 返回pinyin_list依次在string中出现的下标
        #print(string)
        #print(pinyin_list)
        index = 0
        result_list = []
        length = len(string)
        for sub in pinyin_list:
            index = string.index(sub, index)
            result_list.append(index)
            index += 1
        return result_list


def transWordsFile():
    '''
    一次性函数，没啥用了，处理刚下载下来的文件的
    把我下载的带音标的WordsWithAnnonciation.txt转储
    成为不带音标的words.txt
    '''
    result = ""
    with open("WordsWithAnnociation.txt", "r") as f:
        raw_data = f.readlines()
    for line in raw_data:
        # 每行的处理函数
        newline = line[0:line.index("[")]
        result += newline
        result += "\n"
    with open("words.txt", 'w') as f:
        f.write(result)


def makeTrie():
    '''
    pickle文件不存在时执行该函数，
    尝试打开words.txt文件，如果不存在，使用transFile函数建立
    从words.txt中读取单词，并建立trie树
    最后存储至 trie.pkl文件 
    （其实这不没什么必要，太小了，也就快了0.5s）

    返回trie树
    '''
    trie = Trie()
    try:
        with open('words.txt', "r") as f:
            raw_data = f.readlines()

    except Exception as e:
        print("words.txt文件不存在，正在建立...")
        transWordsFile()
        with open('words.txt', "r") as f:
            raw_data = f.readlines()
    

    for word in raw_data:
        trie.add(word[0:-1].lower())
    '''
    with open("trie.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(trie.root, pkl)
    '''
    return trie

# coding=utf-8

def returnToWord(string):
    # 把字符串中的字符转换成可能的字母
    # 把0还原回o，1还原回l @还原为o 5还原为s
    newstr=""
    newstr = string.replace('0','o')
    newstr = newstr.replace('1','l')
    newstr = newstr.replace('@','a')
    newstr = newstr.replace('5','s')
    newstr = newstr.replace('3', 'e')
    return newstr


def handlePwdAndMakeDic(filename, match_module):
    # makeTrie中用readlines函数
    # 这个密码文件太大，一次性读取空间消耗太大，所以逐行读取
    # 使用正则表达式匹配单词
    # match_module,调用其match函数，根据match_module的不同，实现对拼音或者单词的匹配
    # 从词库中提取出来的单词区分大小写，存至词典
    dic = {}
    temp_results = []
    pattern = re.compile(r'[a-z]+', re.IGNORECASE) # 忽略大小写
    with open(filename, "r", encoding="utf-8") as f:
        i=-1
        line = f.readline()
        
        while(line):
            
            if(i % 14430 == 0):
                print('%i%%' % (i/14430)) # 在字符串中%%才能输出百分号
            
            line = line[line.rindex(':') + 1:-1]  # -1为了去掉'\n'
            line = returnToWord(line).lower()
            
            match = pattern.findall(line)
            if(match):
                for element in match:
                    temp_results = match_module.match(element) #检查这个字母串是单词吗
                    for temp_result in temp_results:
                        if temp_result in dic:
                            dic[temp_result] += 1
                        else:
                            dic.setdefault(temp_result, 1)
            try:
                line = f.readline()
            except Exception as e:
                print("readline exception")
            i+=1
        print("100%")
    
    with open("worddic.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(dic, pkl)
    
    return dic
        


def main():

    '''
    try:
        with open("trie.pkl", 'rb') as f:
            trie = Trie(pickle.load(f))
    except Exception as e:
        print("trie.pkl文件不存在，正在建立...")
        makeTrie()
        with open("trie.pkl", 'rb') as f:
            trie = Trie(pickle.load(f))
    '''
    trie = makeTrie()

    '''
    try:
        with open("worddic.pkl", 'rb') as f:
            dic = pickle.load(f)
    except Exception as e:
        print("worddic.pkl文件不存在，正在建立...")
        handlePwdAndMakeDic("temp.txt", trie)
    
        with open("worddic.pkl", 'rb') as f:
            dic = pickle.load(f)
    '''

    
    dic=handlePwdAndMakeDic("data_eng.txt",trie)

    #长度因素归一化
    for key in dic:
        dic[key]=dic[key]*(len(key))



    result_str = ""
    for key in sorted(dic, key=lambda k: dic[k], reverse=1):
        result_str += str(key)
        result_str += ":"
        result_str += str(dic[key])
        result_str += '\n'
    with open("word_result.txt", 'w') as f:
        f.write(result_str)
    print("success!")

    '''
    while(True):
        string=input("input")
        print(trie.batchMatch(string))
    '''
main()