# encoding = utf-8
import pickle
import re
def returnToDigit(string):
    # 把字符串中的字符转换成可能的字母
    # 把0还原回o，1还原回l @还原为o 5还原为s
    newstr=""
    newstr = string.replace('o','0')
    newstr = newstr.replace('l','i')
    newstr = newstr.replace('s','5')
    newstr = newstr.replace('e','3')
    return newstr

def handlePwd(filename, count):
    # makePinyinTrie中用readlines函数
    # 这个密码文件太大，一次性读取空间消耗太大，所以逐行读取
    # 使用正则表达式匹配日期
    # count 表示匹配连续的几个数字
   
    dic = {}
    string="(?:(?<=\D)|^)\d{"+str(count)+"}(?:(?=\D)|$)"
    pattern = re.compile(string)
    with open(filename, "r", encoding="utf-8") as f:
        i = -1
        line = f.readline()

        while(line):
            if(i % 37510 == 0):
                print('%i%%' % (i / 37510))  # 在字符串中%%才能输出百分号
            
            line = line[line.rindex(':') + 1:-1]  # -1为了去掉'\n'
            

            if not line.isalpha():
                # 如果全是字母，不可能含有日期，跳过匹配过程
                match = pattern.findall(line) #我猜测一个人的密码只有一个日期，所以
                if(match):
                    for element in match:
                        if element in dic:
                            dic[element] += 1
                        else:
                            dic.setdefault(element, 1)
            try:
                line = f.readline()
            except Exception as e:
                print("readline exception")

            i += 1
        print("100%")
    '''
    with open("num_dic.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(dic, pkl)
    '''
    return dic

def main():    
    i=22
    if i==22:
    #for i in range(22):
        dic=handlePwd("data.txt",i)
        # 将已经识别提取出来的拼音字典排序后写入txt文件
        result_str = ""
        for key in sorted(dic, key=lambda k: dic[k], reverse=1):
            result_str += str(key)
            result_str += ":"
            result_str += str(dic[key])
            result_str += '\n'
        filename="result/num_result"+str(i)+".txt"
        with open(filename, 'w') as f:
            f.write(result_str)
        print("success!")
        
    '''
    string="(?:(?<=\D)|^)\d{"+str(2)+"}(?:(?=\D)|$)"
    pattern = re.compile(string)
    while(True):
        s=input("input")
        print(pattern.findall(s))
    '''
main()
