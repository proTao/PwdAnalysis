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
    return newstr

def handlePwd(filename):
    # makePinyinTrie中用readlines函数
    # 这个密码文件太大，一次性读取空间消耗太大，所以逐行读取
    # 使用正则表达式匹配日期
   
    dic = {}
    pattern = re.compile(r"(?<![0-9])(?:(?:(?:(?:[1,3,5,7,9][2,6]|[2,4,6,8][0,4,8]|0?[4,8])00|(?:\d{2})(?:[1,3,5,7,9][2,6]|[2,4,6,8][0,4,8]|0[4,8]))[-/_\.\\`\^]?0?2[-/_\.\\`\^]?29|0?2[-/_\.\\`\^]?29[-/_\.\\`\^]?(?:(?:[1,3,5,7,9][2,6]|[2,4,6,8][0,4,8]|0?[4,8])00|(?:\d{2})(?:[1,3,5,7,9][2,6]|[2,4,6,8][0,4,8]|0[4,8])))|(?:(?:(?:1[789]|2[01])(?:\d{2})|[6789]\d)[-/_\.\\`\^]?(?:1[02][-/_\.\\`\^]?(?:[12][0-9]|3[01]|0?[1-9])|11[-/_\.\\`\^]?(?:[12][0-9]|30|0?[1-9])|0?[469][-/_\.\\`\^]?(?:[12][0-9]|30|0?[1-9])|0?[13578][-/_\.\\`\^]?(?:[12][0-9]|3[01]|0?[1-9])|0?2[-/_\.\\`\^]?(?:[1][0-9]|2[0-8]|0?[1-9]))|(?:1[02][-/_\.\\`\^]?(?:[12][0-9]|3[01]|0?[1-9])|11[-/_\.\\`\^]?(?:[12][0-9]|30|0?[1-9])|0?[469][-/_\.\\`\^]?(?:[12][0-9]|30|0?[1-9])|0?[13578][-/_\.\\`\^]?(?:[12][0-9]|3[01]|0?[1-9])|0?2[-/_\.\\`\^]?(?:[1][0-9]|2[0-8]|0?[1-9]))[-/_\.\\`\^]?(?:(?:1[789]|2[01])(?:\d{2})|[6789]\d)))(?![0-9])")
    with open(filename, "r", encoding="utf-8") as f:
        i = -1
        line = f.readline()

        while(line):
            if(i % 37510 == 0):
                print('%i%%' % (i / 37510))  # 在字符串中%%才能输出百分号
            
            line = line[line.rindex(':') + 1:-1]  # -1为了去掉'\n'
            

            if not line.isalpha():
                # 如果全是字母，不可能含有日期，跳过匹配过程
                match = pattern.search(line) #我猜测一个人的密码只有一个日期，所以
                if(match):
                    element = match.group(0)
                    if(len(element) >= 6):
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

    with open("date_dic.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(dic, pkl)


def main():    
    try:
        with open("date_dic.pkl", 'rb') as f:
            word_dic = pickle.load(f)
    except Exception as e:
        print("date_dic.pkl文件不存在，正在建立...")
        handlePwd("data_all.txt")
        with open("date_dic.pkl", 'rb') as f:
            word_dic = pickle.load(f)

    # 将已经识别提取出来的拼音字典排序后写入txt文件
    result_str = ""
    for key in sorted(word_dic, key=lambda k: word_dic[k], reverse=1):
        result_str += str(key)
        result_str += ":"
        result_str += str(word_dic[key])
        result_str += '\n'
    with open("date_result_new.txt", 'w') as f:
        f.write(result_str)
    print("success!")
main()
