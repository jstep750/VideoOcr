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

    str1 = ' '.join(str1.split())   #공백 여러개를 한개로 바꿈
    str2 = ' '.join(str2.split())
    diff += max(len(str1), len(str2)) - len(get_LCS(str1, str2))       

    #diff = diff/max(len(str1), len(str2)) * 10
    #가장 긴 common substring의 길이를 뺌

    return diff



def union_code(lines, txt):
    idx = 0
    for j in txt:
        found = False
        append = True
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
        if(found and append): lines[idx].append(j)
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

    if(len(txt)>3 and reserved == 0): return []
    
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

            if((len(b_stack)==0 or b_stack[-1]!='(') and c ==';'):
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



txt0 = ''' #include  <string> 
 #tinclude <vector> 
 using  namespace std; 
                                                 I 
  int solution(string  s) { 
      int answer = s. length(); 
      for (int  i=1; i <  s.length()/2;  +i)  { 
          int pos =  0; 
          int  len = s.length(); 
          for (  53) { 
          } 
      1 
'''
txt0 = txt0.splitlines()
#txt0 = correct_code(txt0)


for i in txt0:
    print(i)

txt1 = ''' using  namespace std; 
  int solution(string  s) { 
      int answer = s. length(); 
      for (int  i=1; i <= s.length()/2:  +i)  { 
          int pos =  0;                 I 
          int  len = s. length(); 
          for (  53) { 
              string  unit = s.substr(pos,  i); 
          } 
      } 
'''
txt1 = txt1.splitlines()
#txt1 = correct_code(txt1)

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

txt2 = ''' using  namespace std; 
  int solution(string  s) { 
      int answer =  s. length(); 
      for (int  i=1; i <= s.length()/2;  +i)  { 
          int pos =  0; 
          int  len = s.length(); 
          for (  53) { 
              string  unit = s.substr(pos,  i); 
              pos +=  i; 
               if (pos >= s.length())  Break; 
          } 
      } 
'''
txt2 = txt2.splitlines()
#txt2 = correct_code(txt2)

print('-----------------------------------')
answer = union_code(res, txt2)
for i in answer:
    print(i)

txt3 = '''  int solution(string  s) { 
      int answer =  s. length(); 
      for (int  i=l; i <= s.length()/2;  +i)  { 
          int pos =  0; 
          int  len = s.length(); 
          for (  53) { 
              string  unit = s.substr(pos,  i);                   I 
              pos +=  i; 
               if (pos >= s.length())  break; 
               int cnt = 0; 
              for  ( 5:) { 
'''
txt3 = txt3.splitlines()
#txt3 = correct_code(txt3)

print('-----------------------------------')
answer = union_code(res, txt3)
for i in answer:
    print(i)



txt4 = '''         IIL TG = Oslin   g 
         for ( 53) { 
            string unit = s.substr(pos, i); 
            pos += i; 
             if (pos >= s.length()) break; 
             int cnt = 0; 
            for ( 53) { 
                if (unit.compare(s.substr(pos, i)) = 0) { 
                    tnt   5 
                    pos += i; 
                } else { 
'''
txt4 = txt4.splitlines()
#txt4 = correct_code(txt4)

print('-----------------------------------')
answer = union_code(res, txt4)
for i in answer:
    print(i)


txt5 = '''      for (int i=1; i <= s.length()/2; +i)   { 
          int pos = 0; 
          int len = s. length(); 
          for ( 53) { 
              string unit = s.substr(pos,  i); 
              pos += i; 
              if (pos >= s.length()) break; 
                                     I 
              int cnt = 0; 
              for ( 5;) { 
                  if (unit.compare(s.substr(pos,  i)) =  0) { 
                      +cnt 
'''
txt5 = txt5.splitlines()
#txt5 = correct_code(txt5)

print('-----------------------------------')
answer = union_code(res, txt5)
for i in answer:
    print(i)


txt6 = '''          for ( 53) { 
              string unit = s.substr(pos,  i); 
              pos += i;  I 
              if (pos >= s.length())  break; 
              int cnt = 0; 
              for ( 53) { 
                  if (unit.compare(s.substr(pos,  i)) =  0)  { 
                      +cnt; 
                      pos +=  i; 
                  } else { 
                      break; 
                  } 
'''
txt6 = txt6.splitlines()
#txt6 = correct_code(txt6)

print('-----------------------------------')
answer = union_code(res, txt6)
for i in answer:
    print(i)


txt7 = '''                  if (unit.compare(s.substr(pos, i)) = 0) { 
                     +cnt 
                     pos += i; 
                 } else { 
                     break; 
                 } 
             } 
              if (cnt > 0) { 
                  len —= i * cnt; 1 
                  len += 1; 
             } 
         } 
     } 
'''
txt7 = txt7.splitlines()
#txt7 = correct_code(txt7)

print('-----------------------------------')
answer = union_code(res, txt7)
for i in answer:
    print(i)

