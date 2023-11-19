# coding: utf-8

import sys
from datetime import datetime

import urllib.request, urllib.error
from bs4 import BeautifulSoup


def print_arg_error(commandName):
    """引数エラー時のメッセージ出力"""
    print("Usage: python {0} connpassURL\n"
          "\n"
          "example)\n"
          "python {0} https://GROUP_NAME.connpass.com/event/xxxxx/"
          .format(commandName))
    exit(0)


def is_url(url):
    """URL書式チェック"""
    return url.startswith("https://") or url.startswith("http://")


def participation_url(url):
    """参加者URLに変換"""
    if url.endswith("/participation/"):
        return url
    elif url.endswith("/participation"):
        return url + "/"
    elif url.endswith("/"):
        return url + "participation/"
    else:
        return url + "/participation/"


def getgrpName(url, extention):
    """グループ名とイベント番号を取り出してファイル名とする"""

    # url format
    # "https://<groupName>.connpass.com/event/<eventId>/participation/"

    # <groupName>を取り出す
    pos_l1 = url.find("/")
    pos_l2 = url.find("/", pos_l1 + 1)
    pos_l3 = url.find(".")

    if pos_l1 < 0 or pos_l2 < 0 or pos_l3 < 0:
        print("groupName error...")
        return ""

    groupName = url[pos_l2 + 1:pos_l3]

    # <eventId>を取り出す
    pos_r1 = url.rfind("/")
    pos_r2 = url.rfind("/", 0, pos_r1 - 1)
    pos_r3 = url.rfind("/", 0, pos_r2 - 1)

    if ((pos_r1 < 0) or (pos_r2 < 0) or (pos_r3 < 0)):
        print("eventId error...")
        return ""

    eventId = url[pos_r3 + 1 : pos_r2]

    # 現在の時刻を年、月、日、時、分、秒で取得
    dateStr = datetime.now().strftime("%Y%m%d_%H%M%S")

    return(groupName + "_" + eventId + "_" + dateStr + extention)


def users(tags):
    """ユーザー情報の取得(ユーザ名とユーザURLのCSV形式)"""
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

    # URL書式チェック
    if not is_url(args[1]):
        print("URL Error...%s\n" %args[1])
        print_arg_error(args[0])

    # 参加者URLに変換
    url = participation_url(args[1])

    save_fname = getgrpName(url, ".csv")
    if save_fname == "":
        print_arg_error(args[0])

    # 指定したURLの出力htmlを取得する 
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupに取り込む
    soup = BeautifulSoup(html, "html.parser")

    # すべての<A>タグを抽出する
    tags = soup.find_all("a")

    # ユーザー情報保存用リストに格納
    ulist = list(users(tags))

    # 抽出したリストを標準出力に表示する
    for user in ulist:
        print(user, end="")

    # ファイルに出力する
    with open(save_fname, mode='w') as f:
        f.writelines(ulist)

    print("\nsave as ... [{0}]".format(save_fname))

if __name__ == "__main__":
    main()
