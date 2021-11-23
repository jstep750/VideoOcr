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
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    num_alphabets1 = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
    for c in str1:
        for (i,b) in enumerate(alphabets):
            if(c == b):
                num_alphabets1[i] += 1

    num_alphabets2 = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
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
    diff += compare_start_space(str1, str2) * 3     #시작 공백 수
    diff += compare_brackets_num(str1, str2) * 2    #괄호 종류별 개수
    diff += compare_alphabets_num(str1, str2)    #알파벳 종류별 개수

    str1 = ' '.join(str1.split())   #공백 여러개를 한개로 바꿈
    str2 = ' '.join(str2.split())
    diff += max(len(str1), len(str2)) - len(get_LCS(str1, str2))       
    #가장 긴 common substring의 길이를 뺌

    return diff


txt0 = '''  #include  <string>
 include   <vector>
 using  namespace std;
                                               |
  int solution(string s) {
      int answer = s. length();
     for  (int i=l; | <= s.length()/2; +i)  {
          int pos = 0,
          int len = s. length();
          for (53)  {
     l

'''
txt0 = txt0.splitlines()

txt1 = '''  using  namespace std;
  int solution(string s)  {
      int answer = s. length();
      for (int  i=l; | <= s.length()/2: +i)   {
          int pos = 0,                 I
          int len = s. length();
          for ( ;:) {
              string unit  = s.substr(pos,  i);
              |
      }

'''
txt1 = txt1.splitlines()


def union_code(lines, txt):
    idx = 0
    for j in txt:
        found = False
        append = True
        for (i,line) in enumerate(lines):
            if(i > idx):
                for l in line:
                    diff = get_difference_score(j, l)
                    if(diff < 15):
                        if(diff < 10): 
                            append = False
                        idx = i
                        found = True
        if(found and append): lines[idx].append(j)
        elif(found == False):
            idx += 1
            lines.insert(idx,[j])
    
    return lines


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

txt2 = '''  using  namespace std;
  int solution(string  s) {
      int answer = s. length();
      for (int  i=l; i <= s.length()/2; +i)   {
          int pos = 0,
          int  len = s. length();
          for (  53) {
              string  unit = s.substr(pos,  i);
              pos +=  |,
               if (pos >= s. length()) Break;
          }
      }

'''
txt2 = txt2.splitlines()

print('-----------------------------------')
answer = union_code(res, txt2)
for i in answer:
    print(i)

txt3 = '''  int solution(string  s) {
      int answer =  s. length();
      for (int  i=l; i <= s.length()/2;  +i)  {
          int pos =  0,
          int  len = s. length();
          for (  53) {
              string  unit = s.substr(pos,  i);
              pos +=  |;
               if (pos >= s.length())  break;
               int cnt = 0;
              for  ( 53) {

'''
txt3 = txt3.splitlines()

print('-----------------------------------')
answer = union_code(res, txt3)
for i in answer:
    print(i)



txt4 = '''         IIL 1  = ENR  ARRAY
        for ( 53) {
            string unit = s.substr(pos, i);
            pos += |,
            if (pos >= s.length()) break;
            int cnt = 0;
            ASHE
                if (unit.compare(s.substrpos, i)) = 0) {
                   ++2nt.
                     I
                   Dos += i;
                CEC
 
'''
txt4 = txt4.splitlines()

print('-----------------------------------')
answer = union_code(res, txt4)
for i in answer:
    print(i)


txt5 = '''     for (int i=l; i <= s.length()/2; +i) {
         int pos = 0,
         int len = s. length();
         for ( 53) {
            string unit = s.substr(pos, i);
            pos += |;
             if (pos >= s.length()) break;
                                 I
             int cnt = 0,
            ASHE
                if (unit.compare(s.substrpos, i)) = 0) {
                   Hcnt,

'''
txt5 = txt5.splitlines()

print('-----------------------------------')
answer = union_code(res, txt5)
for i in answer:
    print(i)


txt6 = '''          for ( 3)  {
              string unit = s.substr{pos,  i);
              pos += 15  7
              if (pos >= s.length()) break;
              int cnt = 0,
              for ( 53) {
                  if (unit.compare(s.substr(pos,  i)) =  0) {
                      Hent,
                      pos += I,
                  IER
                      break;
                  }

'''
txt6 = txt6.splitlines()

print('-----------------------------------')
answer = union_code(res, txt6)
for i in answer:
    print(i)


txt7 = '''                  if (unit.compare(s.substr(pos, i)) =  0) {
                      Hent,
                      pos += |;
                  IER
                      break;
              if (cnt > 0) {
                  len =|   * cnt   7
                  len += 1,

'''
txt7 = txt7.splitlines()

print('-----------------------------------')
answer = union_code(res, txt7)
for i in answer:
    print(i)
