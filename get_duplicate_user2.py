import sys
import pandas

##-----------------------------------------------------------------------##
## [�O���[�v��_�C�x���gID_YYYYmmdd_HHMMSS.csv]���J��
##-----------------------------------------------------------------------##
def readCSVfile(fileName):

    lines = pandas.read_csv(fileName)

    return lines

##-----------------------------------------------------------------------##
## �Q��csv�z����r���A�Q�߂̔z��ɂȂ����R�[�h��id��Ԃ�
##-----------------------------------------------------------------------##
def getDiff(lines1, lines2):

    hit = False
    for i in range(0, len(lines1)):
        for j in range(0, len(lines2)):
            # profile��URL����v���Ă��邩���ׂ�
            if (lines1.values[i][1] == lines2.values[j][1]):
                hit = True
                print("\"%s\",\"%s\"" %(lines1.values[i][0], lines1.values[i][1]))

                # ���������ꍇ�͎��̃��R�[�h��
                break

    return hit

##-----------------------------------------------------------------------##
## main
##-----------------------------------------------------------------------##
if __name__ == "__main__":

    args = sys.argv
    argc = len(args)

    if argc <= 2:
        print("Usage: python %s file1 file2" %(args[0]))
        exit(0)

    lines1 = []
    lines1 = readCSVfile(args[1])

    lines2 = []
    lines2 = readCSVfile(args[2])

    print()
    print("=== Dupulicate users [%s] in [%s] ===" %(args[1], args[2]))
    getDiff(lines1, lines2)

    print()
