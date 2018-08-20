# coding: cp932 
import sys
from datetime import datetime
import urllib.request, urllib.error
from bs4 import BeautifulSoup

##-------------------------------------------------------##
## �����̃`�F�b�N
##-------------------------------------------------------##
def check_args(commandName, url):
    if ((url.rfind("https://") < 0) and (url.rfind("http://") < 0)):
        print("Usage: python %s connpassURL1 connpassURL2" %(commandName))
        print("ex) > python %s https://xxxxxx.connpass.com/event/xxxxx/" %(commandName))
        exit(0)

##-------------------------------------------------------##
## URL�̃`�F�b�N
##-------------------------------------------------------##
def check_Directory_participation(url):
    if (url.rfind("/participation/") >= 0):
        new_url = url
    elif (args[1].rfind("/participation") >= 0):
        new_url = url + "/"
    else:
        if (url.endswith("/")):
            new_url = url + "participation/"
        else:
            new_url = url + "/participation/"
    
    return(new_url)

##-------------------------------------------------------##
## ���[�U�[���̎擾
##-------------------------------------------------------##
def ulist_add(td):
    ulist = []
    for tag in td:
        try:
            if ((tag.text != "") and (tag.text != "\n\n")):
                hrefStr = tag['href']
                if ((hrefStr.find("/open/") >= 0) or (hrefStr.find("/user/") >= 0)):
                    # csv�`���Ń��X�g�ɏo��
                    ulist.append("\"" + tag.text + "\",\"" + hrefStr +"\"\n")
        except:
            pass
    
    return(ulist)

##-----------------------------------------------------------------------##
## �Q��csv�z����r���Aprofile URL����v���郌�R�[�h���o�͂���
##-----------------------------------------------------------------------##
def getDuplicateRecord(lines1, lines2):
    hit = False
    for data1 in lines1:
        flds1 = data1.split(",")
        for data2 in lines2:
            flds2 = data2.split(",")
            # profile��URL����v���Ă��邩���ׂ�
            if (flds1[1] == flds2[1]):
                hit = True
                print("%s" %data1, end="")

                # ���������ꍇ�͎��̃��R�[�h��
                break
    return hit

##-------------------------------------------------------##
## ���C��
##-------------------------------------------------------##
if __name__ == "__main__":
    args = sys.argv
    argc = len(args)

    # �A�N�Z�X����URL
    # url = "https://xxxxxx.connpass.com/event/xxxxx/participation/"

    if argc <= 2:
        print("Usage: python %s connpassURL1 connpassURL2" %(args[0]))
        exit(0)

    check_args(args[0], args[1])
    check_args(args[0], args[2])

    # URL���`�F�b�N��A���X�g�Ɋi�[����
    url = []
    url.append(check_Directory_participation(args[1]))
    url.append(check_Directory_participation(args[2]))

    # �w�肵��URL�̏o��html���擾���� 
    html = []
    html.append(urllib.request.urlopen(url[0]))
    html.append(urllib.request.urlopen(url[1]))

    # html��BeautifulSoup�Ɏ�荞��
    soup = []
    soup.append(BeautifulSoup(html[0], "html.parser"))
    soup.append(BeautifulSoup(html[1], "html.parser"))

    # ���ׂĂ�<A>�^�O�𒊏o����
    td = []
    td.append(soup[0].find_all("a"))
    td.append(soup[1].find_all("a"))

    # ���[�U�[���̎擾
    ulist = [[]]
    ulist[0] = ulist_add(td[0])
    ulist.append(ulist_add(td[1]))

    # ���o�������X�g��W���o�͂ɕ\������
    for i in range(0, len(ulist)):
        print("\n===== %s ==== " %url[i])
        for user in ulist[i]:
            print(user, end="")

    # �d�����郆�[�U�[��\������
    print("\n===== Duplicate Users ==== ")
    getDuplicateRecord(ulist[0], ulist[1])
    print()
