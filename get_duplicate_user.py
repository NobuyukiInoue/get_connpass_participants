# coding: utf-8

import sys
import os
import pandas


def fileCheck(path):
    """ファイルの存在チェック"""
    if ( os.path.isfile(path) != True ):
        print("%s not found." %path)
        exit(0)


def readCSVfile(fileName):
    """csvファイルを開く"""

    # encodingは、必要に応じて書き換えてください。
    lines = pandas.read_csv(fileName, encoding="sjis")

    return lines


def getDuplicateRecord(lines1, lines2):
    """２つのcsv配列を比較し、profile URLが一致するレコードを出力する"""
    hit = False
    for i in range(0, len(lines1)):
        for j in range(0, len(lines2)):
            # profileのURLが一致しているか調べる
            if (lines1.values[i][1] == lines2.values[j][1]):
                hit = True
                print("\"%s\",\"%s\"" %(lines1.values[i][0], lines1.values[i][1]))

                # 見つかった場合は次のレコードへ
                break

    return hit


def main():
    args = sys.argv
    argc = len(args)

    if argc <= 2:
        print("Usage: python %s file1 file2" %(args[0]))
        exit()

    fileCheck(args[1])
    fileCheck(args[2])
    
    lines1 = readCSVfile(args[1])
    lines2 = readCSVfile(args[2])

    print("\n=== Dupulicate users [%s] in [%s] ===" %(args[1], args[2]))
    getDuplicateRecord(lines1, lines2)
    print()


if __name__ == "__main__":
    main()
