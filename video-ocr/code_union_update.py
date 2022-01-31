import re

def compare_start_space(str1, str2):
    n1 = 0
    n2 = 0
    for c in str1:
        if(c == ' '):
            n1 += 1
        else: break
    for c in str2:
        if(c == ' '):
            n2 += 1
        else: break

    return abs(n1-n2)


def compare_brackets_num(str1, str2):
    brackets = ['<','>','[',']','(',')','{','}']
    
    num_brackets1 = [0, 0, 0, 0, 0, 0, 0, 0]
    for c in str1:
        for (i,b) in enumerate(brackets):
            if(c == b):
                num_brackets1[i] += 1

    num_brackets2 = [0, 0, 0, 0, 0, 0, 0, 0]
    for c in str2:
        for (i,b) in enumerate(brackets):
            if(c == b):
                num_brackets2[i] += 1

    result = 0
    for (c1,c2) in zip(num_brackets1, num_brackets2):
        result += abs(c1-c2)

    return result

def compare_alphabets_num(str1, str2):
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    num_alphabets1 = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    for c in str1:
        for (i,b) in enumerate(alphabets):
            if(c == b):
                num_alphabets1[i] += 1

    num_alphabets2 = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    for c in str2:
        for (i,b) in enumerate(alphabets):
            if(c == b):
                num_alphabets2[i] += 1

    result = 0
    for (c1,c2) in zip(num_alphabets1, num_alphabets2):
        result += abs(c1-c2)
    return result


def same_reservednum(str1, str2):
    reserved = ['asm', 'double', 'new',	'switch', 'auto', 'else', 'operator', 'template',  
    'break', 'enum', 'private', 'this', 'case', 'extern', 'protected', 'throw', 'catch', 'float', 
    'public', 'try', 'char', 'for', 'register', 'typedef', 'class', 'friend', 'return', 'union', 
    'const', 'goto', 'short', 'unsigned', 'continue', 'if', 'signed', 'virtual', 'default', 
    'inline', 'sizeof', 'void', 'delete', 'int', 'static', 'volatile', 'do', 'long', 'struct', 'while', 
    '++', '--', '+=', '-=', '—=', '*=', '/=', '<=', '=>', '==', '!=']

    same_reserved = 0

    for w in reserved:
        if(w in str1 and w in str2): same_reserved += 1    
    return same_reserved



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
    diff += compare_start_space(str1, str2) * 2     #시작 공백 수
    diff += compare_brackets_num(str1, str2) * 2    #괄호 종류별 개수
    diff += compare_alphabets_num(str1, str2)    #알파벳 종류별 개수
    #diff -= same_reservednum(str1, str2) * 10

    str1 = ' '.join(str1.split())   #공백 여러개를 한개로 바꿈
    str2 = ' '.join(str2.split())
    diff += max(len(str1), len(str2)) - len(get_LCS(str1, str2))       

    #diff = diff/max(len(str1), len(str2)) * 10
    #가장 긴 common substring의 길이를 뺌

    return diff


def union_code(lines, txt):
    idx = 0
    multi_sim_check = True # 유사한 라인이 여러개 일때 True, 아니면 false
    multi_sim_index = {} #유사한 라인 인덱스 저장. 유사한 라인이 여러개인 것이 중복으로 나올 수 있으므로
    temp_sim_index = [] # multi_sim_index에 추가 될 리스트.
    is_start_line = True #첫 번째 시작줄은 다르게 적용된다.
    for j in txt:
        found = False
        append = True
        if (multi_sim_check): # 첫 라인 검사 시 전체 검사, 유사한 라인이 여러개 일 때 추가 검토 필요.
            for (i,line) in enumerate(lines):
                for l in line:
                    diff = get_difference_score(j, l)
                    if(diff < 10):
                        if(diff < 5): 
                            append = False
                        idx = i
                        found = True
                        #print(idx, j)
                if (found): # 유사한 라인 발견 시 temp_sim_index에 해당 line 인덱스 추가.
                    temp_sim_index.append(i)
                    found = False
            # 전체 조사가 끝나고
            multi_sim_index[len(multi_sim_index)] = {
                "txt" : j,
                "index" : temp_sim_index[:],
                "append" : append,
            }
            sim_n = len(temp_sim_index)
            if sim_n == 0: # 없으면 .. 
                if (is_start_line): # 첫 라인일 때 없으면 다음줄로 판단 보류.
                    temp_sim_index.clear() #정리.
                    is_start_line = False   
                else:
                    if len(multi_sim_index[len(multi_sim_index) - 2]["index"]) ==0: #이전 줄이 유사한 줄이 없을 때
                        if len(multi_sim_index) == len(txt): # multi_sim_index에 들어간 라인 수가 txt전체 라인수와 같다면.
                            
                            for line in multi_sim_index:
                                # if len(multi_sim_index[line]["index"]) == 0: #유사한 줄 없는 것만 (있는 건 추가를 안하는 방향으로) -> 버리는 것은 없는 것이 더 좋다.
                                lines.append([multi_sim_index[line]["txt"]]) # lines 뒤에 붙인다. (or 모두 잘못된 것이라 판단하고 버리는 방법도 있다.)
                        else: # 아니면 판단 다음 줄로 보류.
                            temp_sim_index.clear() #정리. 
                            pass
                    else: # 이전 줄이 유사한 줄이 여러개 일 때. -> 이 줄은 잘못 인식된 줄이라고 판단.  -> 다음 줄로.
                        temp_sim_index.clear() #정리. 
            elif sim_n == 1: # 단 하나일 때
                found = True
                if (is_start_line): # 첫 라인일 때
                    idx = temp_sim_index[0]
                    if(found and append): lines[idx].append(j) #found만 true일때는 너무 유사하므로 추가 x (이미 있다고 판단)
                    temp_sim_index.clear() #정리.
                    multi_sim_index.clear() #정리
                    multi_sim_check = False # false로 바꿔준다.
                    is_start_line = False
                else: # 이전 라인이 유사한 라인을 여러개 발견했을 때 여기로 온다.
                    idx = temp_sim_index[0] # 이 라인의 index.
                    sim_line_n = len(multi_sim_index) # 이번 라인을 포함한 multi_sim 라인의 개수.
                    before = idx - sim_line_n + 1 # 이번 index에서 multi_sim 라인 개수만큼 뺀게 시작 index.
                    # 이전 라인들 모두 추가
                    if sim_line_n > idx: # 잘못인식.
                        for line in multi_sim_index:
                            # if len(multi_sim_index[line]["index"]) == 0: #유사한 줄 없는 것만 (있는 건 추가를 안하는 방향으로) -> 버리는 것은 없는 것이 더 좋다.
                            lines.append([multi_sim_index[line]["txt"]]) # lines 뒤에 붙인다. (or 모두 잘못된 것이라 판단하고 버리는 방법도 있다.)
                    else:
                        for i in range(sim_line_n):
                            # 추가 or pass(found만 true면)
                            if((len(multi_sim_index[i]["index"]) != 0) and multi_sim_index[i]["append"]): # 앞 조건은 해당 라인이 found가 있었는지 확인.
                                lines[before].append(multi_sim_index[i]["txt"]) #found만 true일때는 너무 유사하므로 추가 x (이미 있다고 판단)
                            before += 1
                    temp_sim_index.clear() #정리.
                    multi_sim_index.clear() #정리
                    multi_sim_check = False # false로 바꿔준다.
            else: # 여러개 일 때, 다음 줄로 판단을 보류.
                if (is_start_line) : # 첫 줄일때
                    temp_sim_index.clear() #정리. 
                    is_start_line = False  
                else: 
                    if len(multi_sim_index) == len(txt): # multi_sim_index에 들어간 라인 수가 txt전체 라인수와 같다면. -> 전체가 중복 append 생략.
                        for line in multi_sim_index:
                            # if len(multi_sim_index[line]["index"]) == 0: #유사한 줄 없는 것만 (있는 건 추가를 안하는 방향으로)
                                lines.append([multi_sim_index[line]["txt"]]) # lines 뒤에 붙인다. (or 모두 잘못된 것이라 판단하고 버리는 방법도 있다.)
                    else: # 아니면 판단 인덱스 이어지는 것이 있는 지 확인. -> 여러개/없으면 보류. 하나면 추가하고 끝
                        temp_sim_index.clear() #정리. 
                        pass  
                    
        else: #기존
            for (i,line) in enumerate(lines):
                if(i >= idx):
                    for l in line:
                        diff = get_difference_score(j, l)
                        if(diff < 10):
                            if(diff < 5): 
                                append = False
                            idx = i
                            found = True
                            #print(idx, j)
                    if(found): break
            if(found and append): lines[idx].append(j) #found만 true일때는 너무 유사하므로 추가 x (이미 있다고 판단)
            elif(found == False):
                idx += 1
                lines.insert(idx,[j])
    
    return lines



def get_startspace(str):
    num = 0
    for c in str:
        if(c == ' '): 
            num += 1
        else: break
    return num


def get_reservednum(str):
    reserved = ['asm', 'double', 'new',	'switch', 'auto', 'else', 'operator', 'template',  
    'break', 'enum', 'private', 'this', 'case', 'extern', 'protected', 'throw', 'catch', 'float', 
    'public', 'try', 'char', 'for', 'register', 'typedef', 'class', 'friend', 'return', 'union', 
    'const', 'goto', 'short', 'unsigned', 'continue', 'if', 'signed', 'virtual', 'default', 
    'inline', 'sizeof', 'void', 'delete', 'int', 'static', 'volatile', 'do', 'long', 'struct', 'while', 
    '++', '--', '+=', '-=', '—=', '*=', '/=', '<=', '=>', '==', '!=']

    num = 0
    for w in reserved:
        if(w in str): num += 1    
    return num
    

# check = ['@','#','//','£','|']
def correct_code(txt):
    reserved = 0
    for str in txt:
        reserved += get_reservednum(str)

    if(reserved == 0): return []
    
    prev_startspace = get_startspace(txt[0])
    brackets = ['[',']','(',')','{','}']
    b_stack = []
    ret = []

    for str in txt:
        newstr = '' 
        skipstr = ''
        append = True
        cur_startspace = get_startspace(str)

        brackets_like = ['|','I','l','1']
        nonblank_num = 0
        blank_num = 0
        change_brackets = -1

        skip = False
        for (idx,c) in enumerate(str):
            if(c != ' '): 
                if(nonblank_num>0 and blank_num>15): 
                    skip = True
                blank_num = 0
                nonblank_num += 1
            else: 
                blank_num += 1

            if(not skip and (len(b_stack)==0 or b_stack[-1]!='(') and c ==';'):
                str1 = ' '.join(str.split())
                if(len(str1.split(';')[1]) < 4):
                    newstr += c
                    skip = True

            if(not skip):
                if(c in brackets_like):
                    change_brackets = c

                if(c in brackets):
                    b_idx = brackets.index(c)
                    if(b_idx%2 == 1):   #close
                        if(len(b_stack)!=0 and b_stack[-1] == brackets[b_idx-1]):   #stack의 top이 open이라면 pop
                            b_stack.pop()
                        else: b_stack.append(c)
                    elif(b_idx%2 == 0):
                        b_stack.append(c)

            if(not skip): newstr+=c
            elif(c!=';' and c!=' '): skipstr+=c

        if(nonblank_num > 0):
            if(cur_startspace-prev_startspace > 8): #이전 줄과 시작이 9칸이상 차이나면 삭제
                print('remove', newstr,'*')
                append = False
            else:
                prev_startspace = cur_startspace

        if(nonblank_num == 1 and change_brackets != -1 and append):
            if(len(b_stack)==0): continue
            top = b_stack[-1]
            idx = brackets.index(top)
            
            if(idx%2 == 0):   #open
                print("replace",change_brackets, brackets[idx+1])
                newstr = newstr.replace(change_brackets, brackets[idx+1])     #stack의 top이 open이면 close로 바꿔줌
                b_stack.pop()
        
        if(append): ret.append(newstr)
        if(len(skipstr)!=0): print('skip', skipstr)

    return ret



txt0 = ''' #include <string> 
 #include <vector> 
 using namespace std; 
 string solution(string new_id)  { 
     string answer =  **;          I 
     return answer; 
 } 
'''
txt0 = txt0.splitlines()
txt0 = correct_code(txt0)


for i in txt0:
    print(i)

txt1 = ''' #include <string> 
 #include <vector> 
 using namespace std; 
 string solution(string  new_id)- { 
     string answer =  ""; 
     for (char ch  : new_id) { 
     } 
     return answer; 
 } 
'''
txt1 = txt1.splitlines()
txt1 = correct_code(txt1)

res = []
for i in txt0:
    temp = []
    temp.append(i)
    res.append(temp)

for i in res:
    print(i)

print('-----------------------------------')
answer = union_code(res, txt1)
for i in answer:
    print(i)


#print(get_difference_score('     for  (int i=l; | <= s.length()/2; +i)  { ', '    for (int i=l; | <= s.length()/2: +i) { '))

txt2 = ''' #include <string> 
 #include <vector> 
 using namespace  std; 
 bool isvalid(char  c) { 
     if  (isalnum(c)) return  true; 
     if  (c =  1   [Il  c=  "'_" || ¢ =  "'".") return true; 
     return  false; 
 } 
 string solution(string  new_id)  { 
     string  answer = ""; 
     for  (char ch : new_id)  { 
'''
txt2 = txt2.splitlines()
txt2 = correct_code(txt2)

print('-----------------------------------')
answer = union_code(res, txt2)
for i in answer:
    print(i)

txt3 = '''     if (isalnum(c))  return true; 
     if{(c="'-"||lc="'_"]|]       c=   ".") return  true; 
     return false; 
 } 
 string solution(string  new_id) { 
     string answer =  ""; 
     for (char ch  : new_id) { 
     } 
     return answer; 
 } 
 |          T 
'''
txt3 = txt3.splitlines()
txt3 = correct_code(txt3)

print('-----------------------------------')
answer = union_code(res, txt3)
for i in answer:
    print(i)



txt4 = '''     if(c="'-"|]]c="'_          ||] c=  "."') return true; 
     return  false; 
 } 
 string solution(string  new_id) { 
     string answer  = ""; 
     for (char  ch : new_id) { 
         if  (isvalid(ch) =  false)  continue; 
         if  (ch="."){ 
              if (answer.length() =   0) continue;  I 
         } 
         ch =  tolower(ch); 
         on mm amt son or wmanemlh bhawlsf kL % 
'''
txt4 = txt4.splitlines()
txt4 = correct_code(txt4)

print('-----------------------------------')
answer = union_code(res, txt4)
for i in answer:
    print(i)


txt5 = '''     bool lastDot = false; 
     for (char ch : new_id) { 
         if (isvalid(ch) =   false) continue; 
         if (ch="."){ 
             if (answer.length() ==  0 || lastDot) continue; 
             lastDot = true; 
         } else { 
             lastDot, = false; 
         } 
         ch = tolower(ch); 
         answer .push_back(ch); 
     } 
     return answer; 
 1 
'''
txt5 = txt5.splitlines()
txt5 = correct_code(txt5)

print('-----------------------------------')
answer = union_code(res, txt5)
for i in answer:
    print(i)


txt6 = '''             if  (answer.length() == 0  || lastDot) continue; 
             lastDot  = true; 
         } else { 
             lastDot  = false; 
         } 
         ch = tolower(ch); 
         answer .push_back(ch); 
     } 
     return answer; 
 }
'''
txt6 = txt6.splitlines()
txt6 = correct_code(txt6)

print('-----------------------------------')
answer = union_code(res, txt6)
for i in answer:
    print(i)

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

def select_startspace(line):
    select = True
    if(len(line)>1):
        line1 = [' '.join(line[0].split())]
        for str in line[1:]:
            str1 = ' '.join(str.split())
            if(get_difference_score(line1[0], str1)>=2):
                select = False
    else: select = False

    if(select):
        str1 = ' '.join(line[0].split())
        if len(str1)==1 and ('{' in str1 or '}'in str1):
            line.sort(key=lambda x : get_startspace(x))
            print('select', int(len(line)/2), ':', line)
            return [line[int(len(line)/2)]]
    return line


def select_code(line):
    if(len(line)>1):
        line.sort(key=lambda x : get_reservednum(x))
        if(get_reservednum(line[0]) != get_reservednum(line[-1])):
            print('line', line)
            return [line[-1]]
    return line


def delete_code(answer):    

    # 이전 줄보다 시작이 9칸이상 차이나면 제거
    # 글자수가 1~4글자인데 +,-,*,/,= 등 없으면 제거
    res = []
    prev_space = get_startspace(answer[0][0])

    for line in answer:
        line = select_startspace(line)
        line = select_code(line)
        li = []

        for str in line:
            delete = False
            dnum = 0

            cur_space = get_startspace(str)
            if(cur_space - prev_space > 8): #이전 줄과 시작이 9칸이상 차이나면 삭제
                delete = True
                dnum = 1

            else: 
                prev_space = cur_space
                str1 = ' '.join(str.split())
                # reserved word가 하나도 없고 "",괄호 안 제외했을 때 단어 6개이상이면 제거 or //로 시작하면 제거
                if(str1.startswith('//')): delete = True
                elif(len(str1) > 5):
                    if(get_reservednum(str1) == 0):
                        tmp = remove_bracket(str1)
                        tmp = remove_string(tmp)
                        if(len(tmp.split()) > 5):
                            delete = True
                            dnum = 2

                else:
                    check = ['+','-','*','/','=','{','}','(',')','[',']']
                    num = 0
                    for c in check:
                        if(c in str1):
                            num+=1
                    if(num == 0): 
                        delete = True
                        dnum = 3

            if not delete: li.append(str)
            else: print('delete', dnum, str)

        if(len(li) != 0):
            res.append(li)
    
    return res


print('-----------------------------------')
answer = delete_code(answer)
for i in answer:
    print(i)
