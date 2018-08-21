# coding: cp932 
import sys
from datetime import datetime

import urllib.request, urllib.error
from bs4 import BeautifulSoup

def print_arg_error(commandName):
    """�����G���[���̃��b�Z�[�W�o��"""
    print("Usage: python {cmd} connpassURL\n"
          "\n"
          "example)\n"
          "python {cmd} https://GROUP_NAME.connpass.com/event/xxxxx/"
          .format(cmd=commandName))
    exit(0)


def is_url(url):
    """URL�����`�F�b�N"""
    return url.startswith("https://") or url.startswith("http://")


def participation_url(url):
    """�Q����URL�ɕϊ�"""
    if url.endswith("/participation/"):
        return url
    if url.endswith("/participation"):
        return url + "/"
    if url.endswith("/"):
        return url + "participation/"
    else:
        return url + "/participation/"


def getgrpName(url, extention):
    """�O���[�v���ƃC�x���g�ԍ������o���ăt�@�C�����Ƃ���"""

    # url format
    # "https://<groupName>.connpass.com/event/<eventId>/participation/"

    # <groupName>�����o��
    pos_l1 = url.find("/")
    pos_l2 = url.find("/", pos_l1 + 1)
    pos_l3 = url.find(".")

    if ((pos_l1 < 0) or (pos_l2 < 0) or (pos_l3 < 0)):
        print("groupName error...")
        return ""

    groupName = url[pos_l2 + 1:pos_l3]

    # <eventId>�����o��
    pos_r1 = url.rfind("/")
    pos_r2 = url.rfind("/", 0, pos_r1 - 1)
    pos_r3 = url.rfind("/", 0, pos_r2 - 1)

    if ((pos_r1 < 0) or (pos_r2 < 0) or (pos_r3 < 0)):
        print("eventId error...")
        return ""

    eventId = url[pos_r3 + 1:pos_r2]

    # ���݂̎�����N�A���A���A���A���A�b�Ŏ擾
    dateStr = datetime.now().strftime("%Y%m%d_%H%M%S")

    return(groupName + "_" + eventId + "_" + dateStr + extention)


def users(tags):
    """���[�U�[���̎擾(���[�U���ƃ��[�UURL��CSV�`��)"""
    for tag in tags:
        try:
            if tag.text and tag.text != "\n\n":
                href = tag['href']
                if "/open/" in href or "/user/" in href:
                    yield '"{name}","{url}"\n'.format(name=tag.text, url=href)
        except:
            pass


def main():
    args = sys.argv

    if len(args) <= 1:
        print_arg_error(args[0])

    # URL Format
    # "https://xxxxxx.connpass.com/event/xxxxx/"

    # URL�����`�F�b�N
    if not is_url(args[1]):
        print("URL Error...%s\n" %args[1])
        print_arg_error(args[0])

    # �Q����URL�ɕϊ�
    url = participation_url(args[1])

    save_fname = getgrpName(url, ".csv")
    if (save_fname == ""):
        print_arg_error(args[0])

    # �w�肵��URL�̏o��html���擾���� 
    html = urllib.request.urlopen(url)

    # html��BeautifulSoup�Ɏ�荞��
    soup = BeautifulSoup(html, "html.parser")

    # ���ׂĂ�<A>�^�O�𒊏o����
    tags = soup.find_all("a")

    # ���[�U�[���ۑ��p���X�g�Ɋi�[
    ulist = list(users(tags))

    # ���o�������X�g��W���o�͂ɕ\������
    for user in ulist:
        print(user, end="")

    # �t�@�C���ɏo�͂���
    with open(save_fname, mode='w') as f:
        f.writelines(ulist)

    print("\nsave as ... [%s]" %(save_fname))

if __name__ == "__main__":
    main()
