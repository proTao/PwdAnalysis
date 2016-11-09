import pickle


keyboard = [  # 14, 14, 13, 1
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', None],
    [None, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', "\\"],
    [None, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', None, None],
    [None, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', None, None, None]
]

keyboard_shift = [
    ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', None],
    [None, 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', "|"],
    [None, 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', None, None],
    [None, 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', None, None, None]
]

# 模拟键盘坐标
keyboard_dic = {
    '`': (0, 0, 0),
    '1': (0, 1, 0),
    '2': (0, 2, 0),
    '3': (0, 3, 0),
    '4': (0, 4, 0),
    '5': (0, 5, 0),
    '6': (0, 6, 0),
    '7': (0, 7, 0),
    '8': (0, 8, 0),
    '9': (0, 9, 0),
    '0': (0, 10, 0),
    '-': (0, 11, 0),
    '=': (0, 12, 0),
    'q': (1, 1.6, 0),
    'w': (1, 2.6, 0),
    'e': (1, 3.6, 0),
    'r': (1, 4.6, 0),
    't': (1, 5.6, 0),
    'y': (1, 6.6, 0),
    'u': (1, 7.6, 0),
    'i': (1, 8.6, 0),
    'o': (1, 9.6, 0),
    'p': (1, 10.6, 0),
    '[': (1, 11.6, 0),
    ']': (1, 12.6, 0),
    '\\': (1, 13.6, 0),
    'a': (2, 1.9, 0),
    's': (2, 2.9, 0),
    'd': (2, 3.9, 0),
    'f': (2, 4.9, 0),
    'g': (2, 5.9, 0),
    'h': (2, 6.9, 0),
    'j': (2, 7.9, 0),
    'k': (2, 8.9, 0),
    'l': (2, 9.9, 0),
    ';': (2, 10.9, 0),
    '\'': (2, 11.9, 0),
    'z': (3, 1.2, 0),
    'x': (3, 2.2, 0),
    'c': (3, 3.2, 0),
    'v': (3, 4.2, 0),
    'b': (3, 5.2, 0),
    'n': (3, 6.2, 0),
    'm': (3, 7.2, 0),
    ',': (3, 8.2, 0),
    '.': (3, 9.2, 0),
    '/': (3, 10.2, 0),
    # shift 键盘
    '~': (0, 0, 1),
    '!': (0, 1, 1),
    '@': (0, 2, 1),
    '#': (0, 3, 1),
    '$': (0, 4, 1),
    '%': (0, 5, 1),
    '^': (0, 6, 1),
    '&': (0, 7, 1),
    '*': (0, 8, 1),
    '(': (0, 9, 1),
    ')': (0, 10, 1),
    '_': (0, 11, 1),
    '+': (0, 12, 1),
    'Q': (1, 1.6, 1),
    'W': (1, 2.6, 1),
    'E': (1, 3.6, 1),
    'R': (1, 4.6, 1),
    'T': (1, 5.6, 1),
    'Y': (1, 6.6, 1),
    'U': (1, 7.6, 1),
    'I': (1, 8.6, 1),
    'O': (1, 9.6, 1),
    'P': (1, 10.6, 1),
    '{': (1, 11.6, 1),
    '}': (1, 12.6, 1),
    '|': (1, 13.6, 1),
    'A': (2, 1.9, 1),
    'S': (2, 2.9, 1),
    'D': (2, 3.9, 1),
    'F': (2, 4.9, 1),
    'G': (2, 5.9, 1),
    'H': (2, 6.9, 1),
    'J': (2, 7.9, 1),
    'K': (2, 8.9, 1),
    'L': (2, 9.9, 1),
    ':': (2, 10.9, 1),
    '"': (2, 11.9, 1),
    'Z': (3, 1.2, 1),
    'X': (3, 2.2, 1),
    'C': (3, 3.2, 1),
    'V': (3, 4.2, 1),
    'B': (3, 5.2, 1),
    'N': (3, 6.2, 1),
    'M': (3, 7.2, 1),
    '<': (3, 8.2, 1),
    '>': (3, 9.2, 1),
    '?': (3, 10.2, 1),
}

'''
刚开始用来生成键盘映射表的代码
string = ""
for i in range(4):
    for j in range(14):
        if keyboard[i][j]:
            string += '\''
            string += str(keyboard_shift[i][j])
            string += '\':('
            string += str(i)
            string += ','
            string += str(j)
            string += '),\n'

print(string)
'''


def getManhattanDistance2(pos1_2d, pos2_2d):
    '''
    计算二维曼哈顿距离
    接受两个二维坐标的输入
    '''
    # 由于浮点数精度问题，可能浮点数的加减乘除得到的不是精确解而是近似解
    # 因此舍入后再返回
    # http://www.zhihu.com/question/25457573
    if(pos1_2d == pos2_2d):
        return 1.2
    else:
        return round(abs(pos1_2d[0] - pos2_2d[0]) + abs(pos1_2d[1] - pos2_2d[1]))


def getDistanceToShift(key_2d, weight):
    '''
    输入值是key的2维坐标
    返回一个键按shift时的代价
    两个shift的中垂线的横坐标是5.7
    shift_weight是按shift键的代价权重，推荐在0到1之间
    '''
    shift1 = (3, 1)
    shift2 = (3, 12.6)
    if(abs(key_2d[0] - 1) < abs(12.6 - key_2d[0])):
        # 离左边的shift近
        return getManhattanDistance2(key_2d, shift1) * weight
    else:
        # 离右边的shift近
        return getManhattanDistance2(key_2d, shift2) * weight


def getKeyDistance(key1, key2, shift_weight):
    '''
    计算两个键在键盘上的距离
    '''
    distance = 0
    # 检查两个件是否都存在于键位表中
    if key1 in keyboard_dic:
        pos1_3d = keyboard_dic[key1]
    else:
        return False
    if key2 in keyboard_dic:
        pos2_3d = keyboard_dic[key2]
    else:
        return False

    # 检查两个键是否一个需要按shift而另一个不需要
    # 这种计算方式使得中间的需要shift的按键的shift代价计算了两遍
    # 而串首和串尾的只被计算了一遍
    shift_flag = (pos1_3d[2] != pos2_3d[2])
    if (shift_flag):
        if(pos1_3d[2]):
            distance += getDistanceToShift(pos1_3d[0:2], shift_weight)
        else:
            distance += getDistanceToShift(pos2_3d[0:2], shift_weight)
    # 计算两个键在键盘上的2维曼哈顿距离，
    md = getManhattanDistance2(pos1_3d[0:2], pos2_3d[0:2])
    # print("键之间距离为" + str(md))
    distance += md
    return distance


def getStringDisdance(string, init_value=3, shift_weight=0.3):
    # length减一的原因是计算
    length = len(string)
    # 初始值越大，对于长串越有利
    distance = init_value

    for i in range(length - 1):
        distance += getKeyDistance(string[i], string[i + 1], shift_weight)
    return (distance, distance / length)

def main():
    result_dic = {}
    with open("data.txt", "r", encoding="utf-8") as f:
        i = -1
        line = f.readline()
        while(line):
            i += 1
            password = line[line.rindex(":")+1:-1]
            if(password != "" and not password.isdigit()):
                pwd_distance = getStringDisdance(password) #pwd_distance是一个有两个元素的数组
                result_dic.setdefault(password, pwd_distance[1])
            if(i % 37510 == 0):
                print('%i%%' % (i/37510)) # 在字符串中%%才能输出百分号
                print(password)
                print(pwd_distance)
            try:
                line = f.readline()
            except Exception as e:
                print("readline exception")
        print("100%")
    result_str = ""
    for key in sorted(result_dic, key=lambda k: result_dic[k]):
        result_str += str(key)
        result_str += ":"
        result_str += str(result_dic[key])
        result_str += '\n'
    with open("keyboard_str.pkl", 'wb') as pkl:  # 以写权限打开二进制文件
        pickle.dump(result_str, pkl)

    with open("keyboard_result.txt", 'wb') as f:
        f.write(result_str.encode("utf-8"))
    print("success")

main()
'''

while True:
    string = input("string")
    print(getStringDisdance(string))

'''