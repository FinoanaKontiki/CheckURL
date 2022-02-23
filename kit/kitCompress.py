import re
from click import style
import cssutils
from bs4 import BeautifulSoup

def replaceCharMultiple(string,tupleChar):
        for cr in tupleChar:
                string = string.replace(*cr)
        return string

def backGround(file, newBackUrl):
    fileContent = ""
    with open(file, "r") as f:
        fileContent = f.read()
   
    reg_no_space = "(?<=background-image:url\()(.*)(?=\);)"
    reg_with_space = "(?<=background-image:\surl\()(.*)(?=\);)"
    
    no_space = re.findall(reg_no_space,fileContent)
    with_space = re.findall(reg_with_space,fileContent)
    if no_space != None:
        print(no_space, "no_space")   
    if with_space != None:
        print(with_space, "with_space")   
    print("--"*50)
    
    to_replace_content = fileContent    
    if len(no_space) > 0 :
        for img in no_space:
            check = replaceCharMultiple(img, (("/","\/"),(".","\.")))
            print(check,'---------')
            to_replace_content =re.sub(check,"vavao.png"+img,to_replace_content)
    if len(with_space) > 0:
        for img in with_space:
            check = replaceCharMultiple(img, (("/","\/"),(".","\.")))
            to_replace_content = re.sub(check,"vavao.png"+img,to_replace_content)
    
    with open("result.html", "w") as res:
        res.write(to_replace_content)
    
backGround('files\kit1.html', "test.png")
# backGround('files\kit2.html', "vao.png")
# backGround('files\multiple.html', "test.png")

code= ""
match = re.findall('url\(([^)]+)\)', code)