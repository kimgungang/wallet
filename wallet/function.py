import re, base64, quopri, os, sys, datetime

def encode_txt(words): #메일의 html? 정보 encoding
    try:
        regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_txt = re.match(regex, words)
        if encoding == 'B':
            string = base64.b64decode(encoded_txt)
        elif encoding == 'Q':
            string = quopri.decodestring(encoded_txt)
        return string.decode(charset)
    except:
        return words
    
def ymcc(year,month):
    if month<10:
        return str(year)+'0'+str(month)
    else: return str(year)+str(month)


def gubun(타입,내용,결제수단,금액,주인):
    if 타입=='수입':
        if 내용=='에스케이하이':
            return '급여'
        elif (내용=='김호일')&(주인=='김호일'):
            return '내계좌이체'
        elif (내용=='최향은')&(주인=='최향은'):
            return '내계좌이체'
        elif 내용[:4]=='전세대출':
            return '대출환급'
        elif 내용[:2]=='용돈':
            return '용돈'
        elif '이자' in 내용:
            return '이자'
    
