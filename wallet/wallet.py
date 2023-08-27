import email, imaplib, os, time
from function import encode_txt


detach_dir = 'wallet'
if 'attachments' not in os.listdir(detach_dir): #'.' 안해도될텐데..
    os.mkdir('wallet/attachments') #dir 생성
    
userid = 'sunaedon333@gmail.com'
passwd = 'oqbr fpva ffdc seld'

try:    
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com') #imap 객체 생성 / 993은 뭘까?
    typ, account = imapSession.login(userid,passwd) #imap 서버에 로그인, 2차 앱비밀번호 필요   
    # if typ != 'OK':
    #     print ('로그인 불가')
    #     raise
    imapSession.select('INBOX') #사서함 선택, inbox > 전체메일함
    # typ, data = imapSession.search(None,'ALL')
    typ, data = imapSession.search(None, '(HEADER From "banksalad")') #보낸사람이 뱅샐인 메일 찾기, 제목은 HEADER Subject
    # if typ != 'OK':
    #     print ('인박스 검색 중 에러 발생')
    #     raise
    for msgid in data[0].split():
        typ, msgpt = imapSession.fetch(msgid, '(RFC822)') #메일 정보 가져옴, html정보로 가져온다 / RFC822는 본문의 필드이름임
        # if typ != 'OK':
        #     print('메일 가져오는 중 에러 발생')
        #     raise
        body = msgpt[0][1]
        mail = email.message_from_bytes(body)
        
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart': #메인콘텐츠 유형
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            name = part.get_filename()
            name = encode_txt(name)
            
            if bool(name): #bool 함수는 변수에 값이 있으면 true, empty면 false
                path = os.path.join(detach_dir,'attachments',name)
                if not os.path.isfile(path):
                    print(name)
                    fp = open(path,'wb') #바이너리 쓰기모드
                    fp.write(part.get_payload(decode=True)) #payload는 내용임(content)
                    fp.close()
                
    imapSession.close()
    imapSession.logout()
            
except:
    print('첨부 파일 다운로드 불가')
    time.sleep(3)






#=================예제파일 따라하기================

# try:    
#     imapSession = imaplib.IMAP4_SSL('imap.gmail.com') #imap 객체 생성 / 993은 뭘까?
#     typ, account = imapSession.login(userid,passwd) #imap 서버에 로그인, 2차 앱비밀번호 필요   
#     # if typ != 'OK':
#     #     print ('로그인 불가')
#     #     raise
#     imapSession.select('INBOX') #사서함 선택, inbox > 전체메일함
#     typ, data = imapSession.search(None,'ALL')
#     # if typ != 'OK':
#     #     print ('인박스 검색 중 에러 발생')
#     #     raise
#     for msgid in data[0].split():
#         typ, msgpt = imapSession.fetch(msgid, '(RFC822)') #메일 정보 가져옴, html정보로 가져온다 / RFC822는 본문의 필드이름임
#         # if typ != 'OK':
#         #     print('메일 가져오는 중 에러 발생')
#         #     raise
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

        