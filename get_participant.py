# coding: cp932 
import sys
from datetime import datetime

import urllib.request, urllib.error
from bs4 import BeautifulSoup

##-------------------------------------------------------##
## グループ名とイベント番号を取り出してファイル名とする
## url          対象イベントのURL
## extension    拡張子  ex) ".csv"
##-------------------------------------------------------##
def getgrpName(url, extention):
    # 現在の時刻を年、月、日、時、分、秒で取得します
    dateStr = datetime.now().strftime("%Y%m%d_%H%M%S")

    # url = "https://<groupName>.connpass.com/event/<event_id>/participation/"

    # グループ名<groupName>を取り出す
    pos_l1 = url.find("/")
    pos_l2 = url.find("/", pos_l1 + 1)
    pos_l3 = url.find(".")

    if ((pos_l1 < 0) or (pos_l2 < 0) or (pos_l3 < 0)):
        print("groupName error...")
        return ""

    groupname = url[pos_l2 + 1:pos_l3]

    # イベント番号<event_id>を取り出す
    pos_r1 = url.rfind("/")
    pos_r2 = url.rfind("/", 0, pos_r1 - 1)
    pos_r3 = url.rfind("/", 0, pos_r2 - 1)

    if ((pos_r1 < 0) or (pos_r2 < 0) or (pos_r3 < 0)):
        print("event_id error...")
        return ""

    eventid = url[pos_r3 + 1:pos_r2]

    return(groupname + "_" + eventid + "_" + dateStr + extention)

##-------------------------------------------------------##
## メイン
##-------------------------------------------------------##
if __name__ == "__main__":
    args = sys.argv
    argc = len(args)

    if argc <= 1:
        print("Usage: python %s connpassURL" %(args[0]))
        exit(0)

    # アクセスするURL
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

    # 指定したURLの出力htmlを取得する 
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupに取り込む
    soup = BeautifulSoup(html, "html.parser")

    # すべての<A>タグを抽出する
    td = soup.find_all("a")

    # ユーザー情報保存用配列
    ulist = []

    for tag in td:
        try:
            if ((tag.text != "") and (tag.text != "\n\n")):

                #print("%s,%s" %(tag.text, tag['href']))
                hrefStr = tag['href']

                if ((hrefStr.find("/open/") >= 0) or (hrefStr.find("/user/") >= 0)):
                    # csv形式でリストに出力
                    ulist.append("\"" + tag.text + "\",\"" + hrefStr +"\"\n")

        except:
            pass

    # 抽出したリストを標準出力に表示する
    for user in ulist:
        print(user, end="")

    # ファイルに出力する
    with open(save_fname, mode='w') as f:
        f.writelines(ulist)

    print("\nsave as ... [%s]" %(save_fname))
