import email, imaplib, os, sys, time, re, base64, quopri, glob, zipfile, datetime
import pandas as pd
import numpy as np

sys.path.append('./wallet')
from function import encode_txt, ymcc


########excel file load##########

path = '.'
path = os.path.join(path,'wallet\\attachments')

for num1, out_dir in enumerate(os.listdir(path)):
    dirpath = os.path.join(path,out_dir)
    if os.path.isdir(dirpath):
        for num2, in_dir in enumerate(os.listdir(dirpath)):
            f_path = os.path.join(dirpath,in_dir)
            if (in_dir.split('.')[1] == 'xlsx')&(in_dir[:2]!='~$'):
                ori_name = out_dir+'-'+in_dir.split('.')[0]
                print(ori_name)
                globals()['{}_{}_{}'.format(ori_name,num1,num2)] = pd.read_excel(f_path,sheet_name=None)
               
glo_list = globals().copy()               
key_list = glo_list.keys()
df_list = []         
     
for key in key_list:
    if key[3:4] == '님':
        df_list.append(key)
        
    
for cnt, lis in enumerate(df_list):
    name = glo_list[lis]['뱅샐현황'].iloc[4,1]
    if name in ('최향은','김호일'):
        glo_list[lis]['가계부 내역']['주인'] = name
    else: raise
    if cnt == 0:
        df = glo_list[lis]['가계부 내역']
    else:
        df = pd.concat([df,glo_list[lis]['가계부 내역']])


#################전처리###############

df.sort_values(by=['날짜','시간'],inplace=True)
df.drop_duplicates(subset=['날짜','시간','내용','금액','결제수단','주인'],keep='first',inplace=True)
df.drop(['화폐','메모'],axis=1,inplace=True)

df['타입'] = df['금액'].apply(lambda x: '수입' if x>0 else '지출')
df['년'] = df['날짜'].apply(lambda x: str(x)[:4]).astype('int32')
df['월'] = df['날짜'].apply(lambda x: str(x)[5:7]).astype('int32')
df['년월'] = df.apply(lambda x:ymcc(x.년,x.월),axis=1).astype('int32')

dtm6 = datetime.datetime.today()-datetime.timedelta(days=180)
if dtm6.month<10:
    dt6 = str(dtm6.year)+'0'+str(dtm6.month)
else: dt6 = str(dtm6.year)+str(dtm6.month)
    
df.drop(df[df['년월']<int(dt6)].index,axis=0,inplace=True)

# df['소분류'] = df.apply <----- 분류 시작

df[df['타입']=='수입']['내용'].unique()









# #########뱅샐메일 첨부파일 다운로드###########

# detach_dir = 'wallet'
# if 'attachments' not in os.listdir(detach_dir): #'.' 안해도될텐데..
#     os.mkdir('wallet/attachments') #dir 생성
    
# userid = 'sunaedon333@gmail.com'
# passwd = 'oqbr fpva ffdc seld'

# try:    
#     imapSession = imaplib.IMAP4_SSL('imap.gmail.com') #imap 객체 생성 / 993은 뭘까?
#     typ, account = imapSession.login(userid,passwd) #imap 서버에 로그인, 2차 앱비밀번호 필요   

#     imapSession.select('INBOX') #사서함 선택, inbox > 전체메일함
#     typ, data = imapSession.search(None, '(HEADER From "banksalad")') #보낸사람이 뱅샐인 메일 찾기, 제목은 HEADER Subject
#     for msgid in data[0].split():
#         typ, msgpt = imapSession.fetch(msgid, '(RFC822)') #메일 정보 가져옴, html정보로 가져온다 / RFC822는 본문의 필드이름임
#         body = msgpt[0][1]
#         mail = email.message_from_bytes(body)
        
#         for part in mail.walk():
#             if part.get_content_maintype() == 'multipart': #메인콘텐츠 유형
#                 continue
#             if part.get('Content-Disposition') is None:
#                 continue
            
#             name = part.get_filename()
#             name = encode_txt(name)
            
#             if bool(name): #bool 함수는 변수에 값이 있으면 true, empty면 false
#                 path = os.path.join(detach_dir,'attachments',name)
#                 if not os.path.isfile(path):
#                     print(name)
#                     fp = open(path,'wb') #바이너리 쓰기모드
#                     fp.write(part.get_payload(decode=True)) #payload는 내용임(content)
#                     fp.close()
#     imapSession.close()
#     imapSession.logout()
# except:
#     print('첨부 파일 다운로드 불가')
#     time.sleep(3)



# ###############압축해제################

# path = '.'

# zippath = []
# filename = []
# abspath = []    
# for root, dirs, files in os.walk(path):
#     rt_path = os.path.join(os.path.abspath(path),root)
#     for file in files:
#         name = file.split('.')[0]
#         ext = file.split('.')[1]
#         if ext == 'zip':
#             zippath.append(os.path.join(rt_path,file)) #zip 파일경로
#             filename.append(name) #확장자 제외 파일명
#             abspath.append(rt_path) #최상위 절대경로

# for i in range(len(zippath)):
#     bn = open(zippath[i],'rb') #zip file open
#     sus = zipfile.ZipFile(bn) #zip binary 변수 지정
#     for n in sus.namelist(): #내용물
#         try:
#             sus.extract(n,abspath[i]+"\\"+filename[i],pwd='1123'.encode('utf-8')) #압축해제 > 이거를 위해서 다....
#         except Exception as e:
#             print(e)
#     bn.close()

