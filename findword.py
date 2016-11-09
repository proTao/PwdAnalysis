import re

def returnToWord(string):
    # 把字符串中的字符转换成可能的字母
    # 把0还原回o，1还原回l @还原为o 5还原为s
    newstr=""
    newstr = string.replace('0','o')
    newstr = newstr.replace('1','l')
    newstr = newstr.replace('@','a')
    newstr = newstr.replace('5','s')
    newstr = newstr.replace('3','e')

    return newstr


def main(word):
    pattern = re.compile(word, re.IGNORECASE) # 忽略大小写
    dic = {}
    with open("data_all.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        i = -1
        while(line):
            i += 1
            if(i % 37510 == 0):
                print('%i%%' % (i/37510))

            # -1为了去掉'\n'
            pwd = returnToWord(line[line.rindex(':') + 1:-1].strip())
            
            # print("string：%s" % line)
            if (not pwd.isdigit() and len(pwd)>=len(word)):
                match = pattern.search(pwd)
                if(match):
                    # 如果匹配到，写入字典
                    if pwd[match.end():] in dic:
                        dic[pwd[match.end():]] += 1
                    else:
                        dic.setdefault(pwd[match.end():], 1)
            try:
                line = f.readline()
            except Exception as e:
                print("readline exception")

    print("100%")
    result_str = ""
    for key in sorted(dic, key=lambda k: dic[k], reverse=1):
        result_str += str(key)
        result_str += ":"
        result_str += str(dic[key])
        result_str += '\n'

    filename="find_"+word+".txt"
    with open(filename, 'w') as f:
        f.write(result_str)

main("aini")