import os
from enum import Enum
from copy_kb import copy_kb
import sys


class CopyKbPaths(Enum):
    SCRIPTS = os.path.dirname(os.path.abspath(__file__))
    OSTIS = os.path.split(SCRIPTS)[0]
    KB = os.path.join(OSTIS, 'ims.ostis.kb')


def main(copy_kb_path: str):
    copy_kb_path = os.path.join(CopyKbPaths.OSTIS.value, os.path.split(copy_kb_path)[1])
    copy_kb(CopyKbPaths.KB.value, copy_kb_path)
    scripts = [os.path.join(CopyKbPaths.SCRIPTS.value, 'remove_scsi.py')]
    for script in scripts:
        os.system("python3 " + script + ' ' + copy_kb_path)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("invalid number of arguments, Please specify only the work directory")
