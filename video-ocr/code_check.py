import re

def remove_string(str):
    found = re.findall(r'''(?x)(?<!\\)".*?(?<!\\)"''', str)
    for f in found:
        str = str.replace(f, '')
    return str

def remove_bracket(str):
    found = re.findall(r'''(?x)(?<!\\)[\[\(].*?(?<!\\)[\]\)]''', str)
    for f in found:
        str = str.replace(f, '')
    return str

def to_wordlist(str):
    str1 = ' '.join(str.split())
    return str1.split()


str1 = 'typedef struct      node_b * hello    (int k) {'
rem = remove_bracket(str1)
print(to_wordlist(rem))

def get_reservednum(str):
    reserved = ['asm', 'double', 'new',	'switch', 'auto', 'else', 'operator', 'template',  
    'break', 'enum', 'private', 'this', 'case', 'extern', 'protected', 'throw', 'catch', 'float', 
    'public', 'try', 'char', 'for', 'register', 'typedef', 'class', 'friend', 'return', 'union', 
    'const', 'goto', 'short', 'unsigned', 'continue', 'if', 'signed', 'virtual', 'default', 
    'inline', 'sizeof', 'void', 'delete', 'int', 'static', 'volatile', 'do', 'long', 'struct', 'while', 
    '++', '--', '+=', '-=', '*=', '/=', '<=', '=>', '==', '!=']

    num = 0
    for w in reserved:
        if(w in str): num += 1    
    return num

def get_startspace(str):
    num = 0
    for c in str:
        if(c == ' '): 
            num += 1
        else: break
    return num

def delete_code(answer):    
    # reserved word가 하나도 없고 ""/괄호 안 제외하고 잘랐을 때 단어 5개이상이고 "",괄호 밖에 특수문자가 있으면 => 제거 
    # 이전 줄보다 시작이 8칸이상 차이나면 제거
    # 공백제거한 글자수가 1~3글자인데 +,-,*,/,= 등 없으면 제거
    res = []
    prev_space = get_startspace(answer[0][0])

    for line in answer:
        li = []
        for str in line:
            delete = False

            cur_space = get_startspace(str)
            if(cur_space - prev_space > 8): #이전 줄과 시작이 9칸이상 차이나면 삭제
                delete = True
                continue
            else: prev_space = cur_space

            str1 = ' '.join(str.split())
            if(len(str1) > 4):
                if(get_reservednum(str1) == 0):
                    tmp = remove_bracket(str1)
                    tmp = remove_string(tmp)
                    if(len(tmp.split()) > 4):
                        delete = True
            else:
                check = ['+','-','*','/','=']
                num = 0
                for c in check:
                    if(c in str1):
                        num+=1
                if(num == 0): delete = True

            if not delete: li.append(str)
            else: print('delete', str)

        if(len(li) != 0):
            res.append(li)
    
    return res





    


print(' '.join('        AN   ual     #8,  TERE ET, TR RET, THESENT'.split()))