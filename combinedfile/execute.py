# Low-level execution of AST commands using xdotool.

import os
from spark import GenericASTTraversal
import GPIOclass
GPIO = GPIOclass.GPIOclass()
outputstring = ""
counter = 0
from os import listdir
import time
import subprocess
class ExecuteCommands(GenericASTTraversal):
    def __init__(self, ast, real = True):
        GenericASTTraversal.__init__(self, ast)
        self.output = []
        self.automator = Automator(real)
        self.postorder_flat()
        self.automator.flush()
        global counter
        counter = 0
    # a version of postorder which does not visit children recursively
    def postorder_flat(self, node=None):
        if node is None:
            node = self.ast

        #for kid in node:
        #    self.postorder(kid)

        name = 'n_' + self.typestring(node)
        if hasattr(self, name):
            func = getattr(self, name)
            func(node)
        else:
            self.default(node)

    def n_chain(self, node):
        for n in node.children:
            self.postorder_flat(n)  
    def n_elec(self, node): 
        pins = []
        for n in node.children:
            pins.append(n.meta)
        test = GPIO.perform(node.meta[0], pins) 
        self.automator.addOutputstrings(test)
    def n_pinsetup(self,node):
        pins = []
        for n in node.children:
            pins.append(int(n.meta))
        self.automator.addOutputstrings(GPIO.setup(str(node.meta[0]), pins))
    def n_print_sleep(self, node):
        global outputstring
        outputstring = str(node.meta)
    def n_program(self, node):
        #print node.meta[0], node.children[0].meta
        dirs = listdir("/home/pi/mysilvius/combinedfile/programs")
        files = []
        status = ""
        for f in dirs:
            if f.endswith(".py"):
                files.append(f)
        if node.meta[0] == "list":
            for f in range(0, len(files)):
                status+="%s is file %s||"%(files[f], f+1)
        else:
            try:
                num = int(node.children[0].meta) - 1
                directory = "sudo python programs/%s"%files[num]
                status = "executed file %s"%files[num]
                os.system(directory) 
            except IndexError:
                status = "program does not exist"
        self.automator.addOutputstrings(status)
    def n_getvalue(self,node):
        string = ""
        if node.meta[0] == "time":
            string = time.asctime( time.localtime(time.time()))
        else:
            string = subprocess.check_output("hostname -I | cut -d\' \' -f1", shell = True)
        self.automator.addOutputstrings(string)
    def n_char(self, node):
        char_list = list(node.meta[0])
        for i in char_list:
            self.automator.key(i)
    def n_raw_char(self, node):
        self.automator.raw_key(node.meta[0])
    def n_mod_plus_key(self, node):
        self.automator.mod_plus_key(node.meta, node.children[0].meta[0])
    def n_movement(self, node):
        self.automator.key(node.meta[0].type)
    def n_sequence(self, node):
        for c in node.meta[0]:
            self.automator.raw_key(c)
    def n_word_sequence(self, node):
        n = len(node.children)
        for i in range(0, n):
            word = node.children[i].meta
            for c in word:
                self.automator.raw_key(c)
            if(i + 1 < n):
                self.automator.raw_key('space')
    def n_null(self, node):
        pass

    def n_repeat(self, node):
        self.postorder_flat(node.children[0])
        xdo = self.automator.xdo_list[-1]
        for n in range(1, node.meta[0]):
            self.automator.xdo(xdo)

    def default(self, node):
        pass

class Automator:
    def __init__(self, real = True):
        self.xdo_list = []
        self.real = real

    def xdo(self, xdo):
        self.xdo_list.append(xdo)

    def flush(self):
        if len(self.xdo_list) == 0: return
        string = ""
        string += ' '.join(self.xdo_list)
        string = string.replace('key ', '')
        string = string.replace('space','')
        self.addOutputstrings(string)
        command = '/usr/bin/xdotool' + ' '
        command += ' '.join(self.xdo_list)
        self.execute(command)
        self.xdo_list = []
    def addOutputstrings(self, string):
        global counter
        counter+=1
        global outputstring
        if counter>1:
            outputstring+="-- " + string
        else:
            outputstring = string
    def execute(self, command):
        if command == '': return

        print "`%s`" % command
        if self.real:
            os.system(command)
    def raw_key(self, k):
        if(k == "'"): k = 'apostrophe'
        elif(k == '.'): k = 'period'
        elif(k == '-'): k = 'minus'
        self.xdo('key ' + k)
    def key(self, k):
        if(len(k) > 1): k = k.capitalize()
        self.xdo('key ' + k)
    def mod_plus_key(self, mods, k):
        command = 'key '
        command += '+'.join(mods)
        if(len(k) > 1 and k != 'plus' and k != 'apostrophe' and k != 'period' and k != 'minus'): k = k.capitalize()
        command += '+' + k
        self.xdo(command)

def execute(ast, real):
    ExecuteCommands(ast, real)
