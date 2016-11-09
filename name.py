import pickle
import re


class Trie:
    # 全部转换为小写存到树里面

    def __init__(self, root={}):
        self.root = root
        self.END = '/'

    def add(self, word):
        # 从根节点遍历单词,char by char,如果不存在则新增,最后加上一个单词结束标志
        word = word.strip()
        word = word.lower()
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
        # 好像是说逆向的效果比正向的好，所以长度一样时优先选择逆向匹配
        if(len(result_f) > len(result_r)):
            return result_f
        else:
            return result_r


def makeTrie(filename):
    '''
    pickle文件不存在时执行该函数，
    尝试打开words.txt文件，如果不存在，使用transFile函数建立
    从words.txt中读取单词，并建立trie树
    最后存储至 trie.pkl文件 
    （其实这不没什么必要，太小了，也就快了0.5s）

    返回trie树
    '''
    trie = Trie()
    with open('name.txt', "r", encoding="utf-8") as f:
        line = f.readline()
        while(line):
            line = line[0:-1].lower()
            trie.add(line)
            line = f.readline()

    '''
    with open("trie.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(trie.root, pkl)
    '''
    print(trie)
    return trie


def returnToWord(string):
    # 把字符串中的字符转换成可能的字母
    # 把0还原回o，1还原回l @还原为o 5还原为s
    newstr = ""
    newstr = string.replace('0', 'o')
    newstr = newstr.replace('1', 'l')
    newstr = newstr.replace('@', 'a')
    newstr = newstr.replace('5', 's')
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
    pattern = re.compile(r'[a-z]+', re.IGNORECASE)  # 忽略大小写
    with open(filename, "r", encoding="utf-8") as f:
        i = -1
        line = f.readline()

        while(line):

            if(i % 37510 == 0):
                print('%i%%' % (i / 37510))  # 在字符串中%%才能输出百分号
            line = line[line.rindex(':') + 1:-1]  # -1为了去掉'\n'
            line = returnToWord(line).lower()
            match = pattern.findall(line)
            if(match):
                for element in match:
                    temp_results = match_module.match(element)  # 检查这个字母串是单词吗
                    for temp_result in temp_results:
                        if temp_result in dic:
                            dic[temp_result] += 1
                        else:
                            dic.setdefault(temp_result, 1)
            try:
                line = f.readline()
            except Exception as e:
                print("readline exception")
            i += 1
        print("100%")

    with open("dic_name.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
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
    trie = makeTrie("name.txt")

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
    dic = handlePwdAndMakeDic("data_all.txt", trie)

    #长度因素归一化
    for key in dic:
        dic[key]=dic[key]*(len(key))


    result_str = ""
    for key in sorted(dic, key=lambda k: dic[k], reverse=1):
        result_str += str(key)
        result_str += ":"
        result_str += str(dic[key])
        result_str += '\n'
    with open("name_result_one.txt", 'w') as f:
        f.write(result_str)

main()
