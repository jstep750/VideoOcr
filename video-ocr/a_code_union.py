import enum
from pickle import FALSE
import re

def get_start_space(str):
    n = 0
    for c in str:
        if(c.isalpha() == False):
            n += 1
        else: break
    return n

def compare_start_space(str1, str2):
    n1 = get_start_space(str1)
    n2 = get_start_space(str2)

    return abs(n1-n2)

def compare_start_space2(str1, str2):
    n1 = get_start_space(str1)
    n2 = get_start_space(str2)
    print('#',str1, n1)
    print('$',str2, n2)

    return abs(n1-n2)

def compare_items_num(str1, str2):
    dic = {}
    res = 0
    for c in str1:
        if(c not in dic): dic[c] = 0
        dic[c] += 1
    for c in str2:
        if(c not in dic): dic[c] = 0
        dic[c] -= 1

    for k in dic:
        res += abs(dic[k])

    return res


reserved = set(['or', 'if', 'in', 'do', '+','-','*','/','=','<','>','{','}','(',')','[',']', '++', '--', '+=', '-=', '—=', '*=', '/=', '<=', '=>', '==', '!='])
new_reserved = set(['or', 'if', 'in', 'do', '+','-','*','/','=','<','>','{','}','(',')','[',']', '++', '--', '+=', '-=', '—=', '*=', '/=', '<=', '=>', '==', '!='])
def get_reservednum(str1):
    words = re.findall(r'[a-zA-Z\d]{3,}',str1)
    n = 0
    global new_reserved
    for w in words:
        if(w[0].isalpha()):
            if(w in reserved): n += 1
            new_reserved.add(w)
    return n

def set_reserved_default():
    global reserved
    reserved = set(['or', 'if', 'in', 'do', '+','-','*','/','=','<','>','{','}','(',')','[',']', '++', '--', '+=', '-=', '—=', '*=', '/=', '<=', '=>', '==', '!='])

def update_reserved():
    global reserved, new_reserved
    reserved = new_reserved.copy()

def same_reservednum(str1, str2):
    n1 = get_reservednum(str1)
    n2 = get_reservednum(str2)
    update_reserved()

    return abs(n1-n2)

def get_substr(str1, str2):
    len_t = len(str1)
    len_c = len(str2)
    result = ''

    for i in range(len_t):
        for j in range(len_c):
            lcs_temp = 0
            match = ''

            while ((i + lcs_temp < len_t) and (j + lcs_temp < len_c) and (str1[i + lcs_temp] == str2[j + lcs_temp])):
                match += str2[j + lcs_temp]
                lcs_temp += 1
            if len(match) > len(result):
                result = match

    return result


def get_LCS(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    result = ''

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])

    i = len1
    j = len2
    while(i>0 and j>0):
        if str1[i - 1] == str2[j - 1]:
            result = str1[i - 1] + result
            i-=1
            j-=1
        elif matrix[i-1][j] > matrix[i][j-1]:
            i-=1
        else:
            j-=1

    return result


def get_difference_score(str1, str2):
    diff = 0
    #print('startspace',compare_start_space(str1, str2))
    diff += compare_start_space(str1, str2) * 2     #시작 공백 수
    diff += compare_items_num(str1, str2)
    #print('itemsnum',compare_items_num(str1, str2))
    #diff += compare_brackets_num(str1, str2) * 2    #괄호 종류별 개수
    #diff += compare_alphabets_num(str1, str2)    #알파벳 종류별 개수
    diff -= same_reservednum(str1, str2) * 2

    str1 = ' '.join(str1.split())   #공백 여러개를 한개로 바꿈
    str2 = ' '.join(str2.split())
    diff += (max(len(str1), len(str2)) - len(get_LCS(str1, str2)))
    #print('maxlen',max(len(str1), len(str2)))
    #print('lcs',get_LCS(str1, str2), len(get_LCS(str1, str2)))       

    #diff = diff/max(len(str1), len(str2)) * 10
    #가장 긴 common substring의 길이를 뺌

    return diff

def correct_str(str):
    n = get_start_space(str)

    i = n
    blank = -1
    while(i<len(str)):
        if(str[i] == ' ' and blank == -1):
            blank = i
        elif(blank != -1 and abs(i-blank)>9):
            str = str[:blank]
            break
        elif(str[i] != ' '):
            blank = -1
        i+=1

    str = str[:n] + re.sub('\s+',' ',str[n:])   #앞 공백 말고 다른 공백 하나로

    strip = len(str)
    for i,s in enumerate(str):
        if(s in [';', ':', ')', ']','}'] and len(str[i+1:])<4):
            strip = i+1
    str = str[:strip]

    '''dic = {'>':'<', ']':'[', ')':'(', '}':'{'}
    dic2 = {'<':'>', '[':']', '(':')', '{':'}'}
    stack = []
    ignore = False
    string = False
    for i,s in enumerate(str):
        if(s == '#' or s == '//'): ignore = True
        if(s=='"' or s=="'"): string = not string
        if not ignore and not string:
            if(s in dic.values()): stack.append(s)
            elif(len(stack)>0 and s in dic): 
                if(dic[s] == stack[-1]): 
                    stack.pop(-1)
            elif(len(stack)>0 and s in ['|','I','l','1'] and dic2[stack[-1]] not in str[i:]):
                print('change', str)
                str = str[:i-1]+dic2[stack[-1]]+str[i:]
                print('to',str)
                stack.pop(-1)
    if(len(stack)>0):
        str += dic2[stack.pop(-1)]  # 괄호 고치기'''
    
    return str


def union_code(lines, txt):
    dic = {i:[] for i in range(len(txt))}
    match = {i:[] for i in range(len(txt))}

    for i,text in enumerate(txt):
        txt[i] = correct_str(text)

    for i,text in enumerate(txt):
        for j,l in enumerate(lines):
            line = l[0]
            diff = get_difference_score(line, text)
            if(diff<25): dic[i].append((diff, j, line))  #조금 유사
            if(diff<4): match[i].append((diff, j, line))    #많이 유사
    
    #print(match)
    match2 = {i:-1 for i in range(len(txt))}    #확실하게 매치된 것
    for k in match:
        if(len(match[k]) == 1): match2[k] = match[k][0][1]
    #print(match2)

    trusted = set()
    for k in match2:
        if(k>0 and k<len(match2)-1):
            if(match2[k-1] == match2[k]-1 and match2[k+1] == match2[k]+1):
                trusted.add(k-1)
                trusted.add(k)      #3번연속 증가하면 trusted에 넣기
                trusted.add(k+1)
    
    #print('Trust',trusted)
    if(len(trusted)>0):
        trusted = sorted(trusted)
        cur = 0
        for k in match2:
            if(k not in trusted and k<trusted[cur]):
                if(match2[k] >= trusted[cur]):  # trusted앞에 있는데 trusted보다 크면 기각 
                    match2[k] = -1
            elif(k not in trusted and k>trusted[cur]):
                if(match2[k] <= trusted[cur]):  # trusted뒤에 있는데 trusted보다 작으면 기각
                    match2[k] = -1
            elif(k in trusted):
                cur = trusted.index(k)
        trusted = set(trusted)

    #print(match2)
    for k in dic:
        # txt의 k번째 줄의 자리찾기
        candid = sorted(dic[k], key=lambda x:x[0])  #diff를 기준으로 후보 sort
        remove = []
        for c in candid:
            rm = False
            for i in range(0,k):   #앞에 매칭된 번호보다 현재번호가 작으면 기각
                if(match2[i] != -1 and match2[i]>=c[1]):
                    if(k not in trusted):
                        remove.append(c)
                        rm = True
                        break
            if(not rm):
                for i in range(k+1,len(txt)):   #뒤에 매칭된 번호보다 현재번호가 크면 기각
                    if(match2[i] != -1 and match2[i]<=c[1]):
                        if(k not in trusted):
                            remove.append(c)
                            break
        for r in remove:
            if(match2[k] == r[1]):
                match2[k] = -1
            candid.remove(r)

        if(len(candid) != 0):
            match2[k] = candid[0][1]    #후보중 가장 점수 높은 것을 매치해줌

    #print(match2)

    newlines = []
    prev = []
    last = 0
    for i in match2:
        add = True
        if(match2[i] != -1):
            newlines += lines[last:match2[i]]   #lines에서 매칭되지 않았던 것들 추가
            last = match2[i]+1

            line = lines[match2[i]][0]
            text = txt[i]
            diff = get_difference_score(line, text)

            if(len(newlines)>0) and (compare_start_space(newlines[-1][0], text)>15):
                add = False     #이전 시작공백과 현재 시작공백이 너무 많이 차이나면 추가X
            if(len(text)>15 and get_reservednum == 0):
                add = False     #길이가 긴데 reservednum이 없으면 추가X
            
            newlines += prev    #전에 txt에서 매칭되지 않았던 것들 추가
            prev = []
            if(add):
                if(diff>4):
                    newlines.append([line, text])
                else: newlines.append([text])
        else:
            text = txt[i]
            if(len(newlines)>0) and (compare_start_space(newlines[-1][0], text)>15):
                add = False
            if(len(text)>15 and get_reservednum == 0):
                add = False
            if(add): prev.append([txt[i]])

    newlines += prev
    newlines = newlines + lines[last:]
    #print('-------------------------------------')
    #for n in newlines:
    #    print(n)
    #    print()

    return newlines

def correct_code(str):
    for i,text in enumerate(str):
        str[i] = correct_str(text)
    return str

def make_result(answer):
    res = []
    for i,lines in enumerate(answer):
        j = 0
        for str in lines:
            if(j<2 and (get_reservednum(str)>0 or len(str)-get_start_space(str)==1)):
                res.append(str)
                j += 1
    return res

def make_string(lines):
    str = ''
    for line in lines:
        str += line + '\n'
    return str

if __name__ == '__main__':
    
    #video-ocr\image_frames\4e9309a735fa4978b492a35f3b54f4d7
    #video-ocr\image_frames\1b1e24ff94ac4cc0be041412ace8eb45
    f0 = open('./image_frames/4e9309a735fa4978b492a35f3b54f4d7/frame'+str(0)+'text.txt', 'r')
    #f0 = open('./image_frames/test/txt'+str(0)+'.txt', 'r')
    txt0 = f0.readlines()
    res = []
    for t in txt0:
        print(t)
        res.append([t])

    #print(correct_code(res))
    for i in range(1,12):
        textfile = './image_frames/4e9309a735fa4978b492a35f3b54f4d7/frame' + str(i) + 'text.txt'
        f = open(textfile, 'r')
        print('---------------------'+str(i)+'---------------------')
        lines = f.readlines()
        for line in lines:
            print(line)
        print('-----------------------------------------------------')
        #res = correct_code(res)
        res = union_code(res, lines)
        for line in res:
            print(line)
        f.close() 

    '''for i in range(1,7):
        textfile = './image_frames/test/txt' + str(i) + '.txt'
        f = open(textfile, 'r')
        print('---------------------'+str(i)+'---------------------')
        lines = f.readlines()
        for line in lines:
            print(line)
        print('-----------------------------------------------------')
        #res = correct_code(res)
        res = union_code(res, lines)
        for line in res:
            print(line)
        f.close() '''
        
    print('#########################################################')
    answer = make_result(res)
    for l in answer:
        print(l)
    
    print()
    print(reserved)
    set_reserved_default() # reserved를 원래대로 바꿔줌
