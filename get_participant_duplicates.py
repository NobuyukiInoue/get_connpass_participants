# coding: utf-8

import sys
import urllib.request
import urllib.error
from bs4 import BeautifulSoup


def print_arg_error(commandName):
    """引数エラー時のメッセージ出力"""
    print("Usage: python {cmd} connpassURL1 connpassURL2\n"
          "\n"
          "example)\n"
          "python {cmd} https://GROUP_A.connpass.com/event/xxxxx/"
                      " https://GROUP_B.connpass.com/event/yyyyy/"
          .format(cmd=commandName))
    exit(0)


def is_url(url):
    """URL書式チェック"""
    return url.startswith("https://") or url.startswith("http://")


def participation_url(url):
    """参加者URLに変換"""
    if url.endswith("/participation/"):
        return url
    if url.endswith("/participation"):
        return url + "/"
    if url.endswith("/"):
        return url + "participation/"
    else:
        return url + "/participation/"


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


def getDuplicateUsers(users1, users2):
    """２つのcsv配列を比較し、profile URLが一致するレコードを出力する"""
    urls2 = {user2.split(",")[1] for user2 in users2}
    for user1 in users1:
        name1, url1 = user1.split(",")
        if url1 in urls2:
            yield user1


class Connpass:
    """Compassイベント参加者情報"""

    def __init__(self, url):
        self.url = participation_url(url)
        html = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find_all("a")
        self.users = list(users(tags))

    def show_users(self):
        """抽出した参加者リストを標準出力に表示する"""
        print("\n===== %s ==== " % self.url)
        for user in self.users:
            print(user, end="")


def main():

    # URL Format
    # "https://xxxxxx.connpass.com/event/xxxxx/"

    cmd, *args = sys.argv
    argc = len(args)
    if argc != 2:
        print_arg_error(cmd)
    url1, url2 = args

    if not is_url(url1) or not is_url(url2):
        print_arg_error(cmd)

    connpass1 = Connpass(url1)
    connpass2 = Connpass(url2)

    connpass1.show_users()
    connpass2.show_users()

    # 重複するユーザーを表示する
    print("\n===== Duplicate Users ==== ")
    for user in getDuplicateUsers(connpass1.users, connpass2.users):
        print(user, end="")
    print()

if __name__ == "__main__":
    main()
