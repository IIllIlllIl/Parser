#
# wang.tr@outlook.com
#
import io_file
import os

class variable:
    name = None
    proc = None
    type = None
    kind = None
    leve = None
    addr = None

    def __init__(self, n, p, t, k, l, a):
        self.name = n
        self.proc = p
        self.type = t
        self.kind = k
        self.leve = l
        self.addr = a

    def str(self):
        return self.name + " " + self.proc + " " + self.type + " " \
               + str(self.kind) + " " + str(self.leve) + " " + str(self.addr)


class procedure:
    name = None
    type = None
    leve = None
    adrf = None
    adrl = None

    def __init__(self, n="", t="", l=0, fa=0, la=-1):
        self.name = n
        self.type = t
        self.leve = l
        self.adrf = fa
        self.adrl = la

    def adr(self):
        return self.adrl - self.adrf + 1

    def check(self, n):
        if self.name == n:
            return 0
        else:
            return 1

    def str(self):
        return self.name + " " + self.type + " " + str(self.leve) + " " + str(self.adrf) + " " + str(self.adrl)


# variable table
var = []
# procedure table
pro = []
# error table
err = []

# symbol
sym = ""
# value
val = -1

# end of file
eof = 0
# buffer list
buf = []
# current line
line = 1
# current level
level = 0
# current buffer list printer
buf_ptr = 0
# current procedure list printer
pro_ptr = 0


# parse (all in one)
def parse(buffer):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    init(buffer)
    a()


# init
def init(buffer):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    # read
    buf = buffer.split("\n")

    # add main
    proc = procedure()
    pro.append(proc)

    advance()


# read line
def read_line():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr
    temp = buf[buf_ptr].split(" ")
    val = int(temp[-1])
    if val < 10:
        sym = temp[-3]
    else:
        sym = temp[-2]
    buf_ptr += 1
    return [sym, val]


# read next from buf
def advance():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    # read
    read_line()

    # eof?
    if sym == "EOF":
        eof = 1

    # eoln?
    while sym == "EOLN":
        line += 1
        read_line()

    #print(sym, val)


# error
def error(type):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if type == 0:
        err.append("LINE "+str(line)+": variable \""+str(sym)+"\" previously declared.")
    elif type == 1:
        err.append("LINE "+str(line)+": missing declaration here.")
    elif type == 2:
        err.append("LINE "+str(line)+": missing executive statement here.")
    elif type == 3:
        err.append("LINE "+str(line)+": missing \"end\" here.")
    elif type == 4:
        err.append("LINE "+str(line)+": missing \"begin\"n here.")
    elif type == 5:
        err.append("LINE "+str(line)+": missing \';\' here.")
    elif type == 6:
        err.append("LINE "+str(line)+": brackets doesn't matched.")
    elif type == 7:
        err.append("LINE "+str(line)+": illegal variable here.")
    elif type == 8:
        err.append("LINE "+str(line)+": missing \'(\' here.")
    elif type == 9:
        err.append("LINE "+str(line)+": illegal declaration here.")
    elif type == 10:
        err.append("LINE "+str(line)+": illegal executive statement here.")
    elif type == 11:
        err.append("LINE "+str(line)+": variable \""+str(sym)+"\" undeclared.")
    elif type == 12:
        err.append("LINE "+str(line)+": missing \"else\" here.")
    elif type == 13:
        err.append("LINE "+str(line)+": missing \"then\" here.")
    elif type == 14:
        err.append("LINE "+str(line)+": illegal operator here.")
    else:
        err.append("LINE "+str(line)+": unknown error")

    advance()


# check if exist in the variable table
def check(kind=-1):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    same = 0
    for i in range(pro[pro_ptr].adr()):
        var_ptr = i + pro[pro_ptr].adrf
        if (var[var_ptr].name == sym) and (var[var_ptr].leve == level):
            # exist
            if same == 0:
                same = 1
            # same kind
            if var[var_ptr].kind == kind:
                same = 2

    return same


# add to the variable table
def add(kind):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    # already exist
    if check(kind) == 2:
        error(0)
        return

    # add variable
    vari = variable(str(sym), pro[pro_ptr].name, "integer", kind, level, len(var))
    var.append(vari)
    pro[pro_ptr].adrl += 1


# A~J are parsing processes
def a():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if sym == "begin":
        advance()
        if sym == "integer":
            advance()
            b()
        else:
            error(1)
        if sym == ";":
            while sym == ";":
                advance()
                if sym == "integer":
                    advance()
                    b()
                else:
                    break
        else:
            error(2)
        c()
        while sym == ";":
            advance()
            c()
        if sym == "end":
            advance()
            return
        else:
            error(3)
    else:
        error(4)


def b():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if val == 10:
        add(0)
        advance()
    elif sym == "function":
        advance()
        func_name = sym
        if val == 10:
            advance()
            level += 1
            proc = procedure(func_name, "integer", level, len(var), len(var)-1)
            pro.append(proc)
            pro_ptr += 1
            if sym == "(":
                advance()
                if val == 10:
                    add(1)
                    advance()
                    if sym == ")":
                        advance()
                        if sym == ";":
                            advance()
                            a()
                            level -= 1
                            pro_ptr -= 1
                        else:
                            error(5)
                    else:
                        error(6)
                else:
                    error(7)
            else:
                error(8)
        else:
            error(7)
    else:
        error(9)


def c():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if sym == "read":
        advance()
        d()
    elif sym == "write":
        advance()
        d()
    elif val == 10:
        advance()
        e()
    elif sym == "if":
        advance()
        i()
    else:
        error(10)


def d():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if sym == "(":
        advance()
        if val == 10:
            if check() > 0:
                advance()
            else:
                error(11)
            if sym == ")":
                advance()
            else:
                error(6)
        else:
            error(7)
    else:
        error(8)


def e():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    if sym == ":=":
        advance()
        f()
    else:
        error(14)


def f():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    g()
    while sym == "-":
        advance()
        f()


def g():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    h()
    while sym == "*":
        advance()
        h()


def h():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    # if function exist
    exist = 1
    for p in pro:
        exist *= p.check(sym)
    if exist == 0:
        advance()
        if sym == "(":
            advance()
            f()
            if sym == ")":
                advance()
            else:
                error(6)
        else:
            error(8)
    elif val == 10:
        if check() > 0:
            advance()
        else:
            error(11)
    elif val == 11:
        advance()
    else:
        error(10)


def i():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    j()
    if sym == "then":
        advance()
        c()
        if sym == "else":
            advance()
            c()
        else:
            error(12)
    else:
        error(13)


def j():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    f()
    if (val >= 12) and (val <= 17):
        advance()
        f()
    else:
        error(14)


# write to the file
def write(path, buffer):
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr

    p_err = path[0:len(path)-3] + "err"
    p_dys = path[0:len(path)-3] + "dys"
    p_var = path[0:len(path)-3] + "var"
    p_pro = path[0:len(path)-3] + "pro"

    io_file.write_file(p_dys, buffer)
    io_file.add_file(p_err, err)

    io_file.str_file(p_var, var)
    io_file.str_file(p_pro, pro)

    # delete dyd
    #os.remove(path)


# output
def out():
    global buf, sym, val, line, level, eof, buf_ptr, pro_ptr
    for v in var:
        print(v.str())
    for p in pro:
        print(p.str())


