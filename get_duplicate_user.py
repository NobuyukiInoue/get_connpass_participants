# coding: cp932

import sys
import os

def getDuplicateUsers(users1, users2):
    """２つのcsv配列を比較し、profile URLが一致するレコードを出力する"""
    urls2 = {user2.split('","')[1] for user2 in users2}
    for user1 in users1:
        name1, url1 = user1.split('","')
        if url1 in urls2:
            yield user1

def main():
    args = sys.argv

    if len(args) <= 2:
        print("Usage: python %s file1 file2" %(args[0]))
        exit()

    if ( os.path.isfile(args[1]) != True ):
        print("%s not found." %(args[1]))
        exit(0)
        
    if ( os.path.isfile(args[2]) != True ):
        print("%s not found." %(args[2]))
        exit(0)

    with open(args[1]) as f:
        users1 = f.readlines()

    with open(args[2]) as f:
        users2 = f.readlines()

    # ２つのcsv配列を比較し、profile URLが一致するレコードを出力する
    print("\n=== Dupulicate users [%s] in [%s] ===" %(args[1], args[2]))
    for user in getDuplicateUsers(users1, users2):
        print(user, end="")

if __name__ == "__main__":
    main()
