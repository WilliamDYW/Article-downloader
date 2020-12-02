from os import system
from time import sleep
with open("num") as fn:
    num = int(fn.readline())
def get_filetype(filename):
    with open("ready", 'r', errors='replace') as f1:
        line = f1.readline()
    f1.close()
    if "%PDF" in line:
        return "pdf"
    if "<!DOCTYPE html>" in line:
        return "html"
    return "others"
system("mkdir -p log")
system("rm nohup.out")
with open("doi.txt") as f0:
    doi = f0.readlines()
k=0
for d in doi:
    root = ""
    k+=1
    if k < num:
        continue
    sleep(1)
    sd = "nohup wget -O ready --timeout=180 --waitretry=0 --tries=5 --retry-connrefused doi.org/"
    system(sd+d)
    with open("nohup.out", 'r', errors='replace') as f2:
        lineLoc = f2.readlines()
    for Loc in lineLoc:
        if "Location: http" in Loc:
            findHTTP = Loc.split("://")[1]
            root = findHTTP.split('/')[0]
    print(root)
    DownloadName = ""
    with open("key.txt","r") as f3:
        keys = f3.readlines()
    f3.close()
    for key in keys:
        site = key.split()
        if root == site[0]:
            DownloadName = site[1]
            break
    if DownloadName == "":
        DownloadName = "pdf"
    print(DownloadName)
    f2.close()
    with open("ready", 'r', errors='replace') as f1:
        line = f1.readline()
    if get_filetype("ready")=="pdf":
        s = "cp ready "+str(k)+".pdf"
        system(s)
        f1.close()
        continue
    f1.close()
    with open("ready", 'r', errors='replace') as f1:
        lines = f1.readlines()
    Value = []
    temp = 0
    for i in lines:
        j = i
        if "href=" in i or "content=" in i:
            i = i.split("href=")[-1]
            i = i.split("content=")[-1]
            #print(i)
            hajim = i.find("http")
            if hajim == -1:
                hajim = i.find("\"/")
                if hajim != -1 and root != "":	
                    i = root + i[hajim+1:]
                    #print(root,i)
                elif i.find("\"")!=-1 and root != "":
                    i = root + "/" + i[i.find("\"")+1:]
                    #print(root,i)
            else:
                i = i[hajim:]
            owar = i.find("\"")
            i = i[:owar]
            if i != "":
                temp+=1
                Value.append(i)
    Downloaded = []
    n = 0
    #print("HTML:")
    #print(Value)
    for i in Value:
        temp = i.split("://")[-1]
        if DownloadName in i and temp not in Downloaded:
            n+=1
            print(Downloaded,i,temp)
            Downloaded.append(temp)
            while(True):
                dropSpace = i.find(" ")
                if dropSpace == -1:
                    break
                i = i[0:dropSpace] + "%20" + i[dropSpace+1:]
            s = "nohup wget -O "+str(k)+"-"+str(n)+".pdf --timeout=180 --waitretry=0 --tries=5 --retry-connrefused "+i
            system(s)
        #print("finish")
    if n==0:
        s = "cp ready "+str(k)+".html"
        system(s)
    f1.close()
    system("rm ready")
    system("cp nohup.out log/"+str(k)+".log")
    system("rm nohup.out")
f0.close()
