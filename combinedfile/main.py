# Main file. Parse new commands from stdin until EOF.

from scan import find_keywords
from scan import scan
from parse import parse
from parse import GrammaticalError
from parse import SingleInputParser
import execute
from ast import printAST
import OLEDclass

OLED = OLEDclass.OLEDclass()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        f = open(filename)
    else:
        f = sys.stdin

    parser = SingleInputParser()
    find_keywords(parser)  # init lexer

    while True:
        line = f.readline()
        if line == '': break
        if line == '\n': continue

        print ">", line,
        try:
            OLED.printToOLED(line)  #for when I don't want to speak
            ast = parse(parser, scan(line))
            printAST(ast)
            execute.execute(ast, f == sys.stdin)
            OLED.printStatus(execute.outputstring)
        except GrammaticalError as e:
            print("Error:", e)

    if f != sys.stdin:
        f.close()

    print 'ok'
