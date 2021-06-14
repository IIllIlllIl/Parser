#
# wang.tr@outlook.com
#

import io_file
import func

if __name__ == '__main__':
    #path = input()
    path = "../Scanner/tests/test.dyd"

    buf = io_file.read_file(path)
    func.parse(buf)

    if len(buf) != 0:
        #func.write(path, buf)
        func.out()
        print(func.err)
        print("Parser finished")
    else:
        print("File not found.")
