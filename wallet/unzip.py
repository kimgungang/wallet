import os, zipfile


path = '.'

zippath = []
filename = []
abspath = []    
for root, dirs, files in os.walk(path):
    rt_path = os.path.join(os.path.abspath(path),root)
    for file in files:
        name = file.split('.')[0]
        ext = file.split('.')[1]
        if ext == 'zip':
            zippath.append(os.path.join(rt_path,file)) #zip 파일경로
            filename.append(name) #확장자 제외 파일명
            abspath.append(rt_path) #최상위 절대경로

for i in range(len(zippath)):
    bn = open(zippath[i],'rb') #zip file open
    sus = zipfile.ZipFile(bn) #zip binary 변수 지정
    for n in sus.namelist(): #내용물
        try:
            sus.extract(n,abspath[i]+"\\"+filename[i],pwd='1123'.encode('utf-8')) #압축해제 > 이거를 위해서 다....
        except Exception as e:
            print(e)
    bn.close()

