# coding: cp932 
import sys
from datetime import datetime

import urllib.request, urllib.error
from bs4 import BeautifulSoup

##-------------------------------------------------------##
## �O���[�v���ƃC�x���g�ԍ������o���ăt�@�C�����Ƃ���
## url          �ΏۃC�x���g��URL
## extension    �g���q  ex) ".csv"
##-------------------------------------------------------##
def getgrpName(url, extention):
    # ���݂̎�����N�A���A���A���A���A�b�Ŏ擾���܂�
    dateStr = datetime.now().strftime("%Y%m%d_%H%M%S")

    # url = "https://<groupName>.connpass.com/event/<event_id>/participation/"

    # �O���[�v��<groupName>�����o��
    pos_l1 = url.find("/")
    pos_l2 = url.find("/", pos_l1 + 1)
    pos_l3 = url.find(".")

    if ((pos_l1 < 0) or (pos_l2 < 0) or (pos_l3 < 0)):
        print("groupName error...")
        return ""

    groupname = url[pos_l2 + 1:pos_l3]

    # �C�x���g�ԍ�<event_id>�����o��
    pos_r1 = url.rfind("/")
    pos_r2 = url.rfind("/", 0, pos_r1 - 1)
    pos_r3 = url.rfind("/", 0, pos_r2 - 1)

    if ((pos_r1 < 0) or (pos_r2 < 0) or (pos_r3 < 0)):
        print("event_id error...")
        return ""

    eventid = url[pos_r3 + 1:pos_r2]

    return(groupname + "_" + eventid + "_" + dateStr + extention)

##-------------------------------------------------------##
## ���C��
##-------------------------------------------------------##
if __name__ == "__main__":
    args = sys.argv
    argc = len(args)

    if argc <= 1:
        print("Usage: python %s connpassURL" %(args[0]))
        exit(0)

    # �A�N�Z�X����URL
    # url = "https://xxxxxx.connpass.com/event/xxxxx/participation/"
    if ((args[1].rfind("https://") < 0) and (args[1].rfind("http://") < 0)):
        print("Usage: python %s connpassURL" %(args[0]))
        print("ex) > python %s https://xxxxxx.connpass.com/event/xxxxx/" %(args[0]))
        exit(0)

    if (args[1].rfind("/participation/") >= 0):
        url = args[1]
    elif (args[1].rfind("/participation") >= 0):
        url = args[1] + "/"
    else:
        if (args[1].endswith("/")):
            url = args[1] + "participation/"
        else:
            url = args[1] + "/participation/"

    save_fname = getgrpName(url, ".csv")
    if (save_fname == ""):
        exit

    # �w�肵��URL�̏o��html���擾���� 
    html = urllib.request.urlopen(url)

    # html��BeautifulSoup�Ɏ�荞��
    soup = BeautifulSoup(html, "html.parser")

    # ���ׂĂ�<A>�^�O�𒊏o����
    td = soup.find_all("a")

    # ���[�U�[���ۑ��p�z��
    ulist = []

    for tag in td:
        try:
            if ((tag.text != "") and (tag.text != "\n\n")):

                #print("%s,%s" %(tag.text, tag['href']))
                hrefStr = tag['href']

                if ((hrefStr.find("/open/") >= 0) or (hrefStr.find("/user/") >= 0)):
                    # csv�`���Ń��X�g�ɏo��
                    ulist.append("\"" + tag.text + "\",\"" + hrefStr +"\"\n")

        except:
            pass

    # ���o�������X�g��W���o�͂ɕ\������
    for user in ulist:
        print(user, end="")

    # �t�@�C���ɏo�͂���
    with open(save_fname, mode='w') as f:
        f.writelines(ulist)

    print("\nsave as ... [%s]" %(save_fname))
