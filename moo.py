import argparse
import os
import sys
from typing import List, Optional


class cow:
    instructions = ["moo", "mOo", "moO", "mOO", "Moo", "MOo", "MoO", "MOO", "OOO", "MMM", "OOM", "oom"]
    def __init__(self) -> None:
        super().__init__()
        self.cellArray  :   list[int] = [0 for _ in range(30000)]
        self.commands   :   list[int] = []
        self.ptr        :   int = 0
        self.commandPtr :   int = 0
        self.register   :   Optional[int] = None
        
        self.commandFunctionIndex = {
            0   :   self.loopEnd,
            1   :   self.prevCell,
            2   :   self.nextCell,
            3   :   self.handleAsInstruction,
            4   :   self.printOrReadChar,
            5   :   self.decrementCell,
            6   :   self.incrementCell,
            7   :   self.loopStart,
            8   :   self.setZero,
            9   :   self.copyPaste,
            10  :   self.printInt,
            11  :   self.readInt
        }
        
        
    def interpret(self, code: str):
        filtered_cmds = filter(lambda x: x in self.instructions, code.split())
        mapped_cmds = map(lambda x: self.instructions.index(x), filtered_cmds)
        self.commands = list(mapped_cmds)
        self.ptr = 0
        
        while self.commandPtr < len(self.commands):
            self.handleCommand(self.commands[self.commandPtr])
            self.commandPtr += 1
    
    def loopEnd(self):
        startPtr = self.getLoopStart(self.commandPtr)
        self.commandPtr = int(startPtr) - 1 
            
    def handleCommand(self, curentCmd):
        self.commandFunctionIndex[curentCmd]()
        
    def nextCell(self):
        self.ptr += 1
        
    def prevCell(self):
        self.ptr -= 1
        
    def handleAsInstruction(self):
        if 0 > self.cellArray[self.ptr] >= len(self.instructions) or self.cellArray[self.ptr] == 3:
            raise Exception("Invalid instruction")
        self.handleCommand(self.cellArray[self.ptr])
    
    def printOrReadChar(self):
        if self.cellArray[self.ptr] == 0:
            self.readChar()
        else:
            self.printChar()
    
    def incrementCell(self):
        self.cellArray[self.ptr] += 1
        
    def decrementCell(self):
        self.cellArray[self.ptr] -= 1
        
    def loopStart(self):
        if self.cellArray[self.ptr] == 0:
            endPtr = self.getLoopEnd(self.commandPtr)
            self.commandPtr = endPtr
    
    def copyPaste(self):
        if self.register is None:
            self.register = self.cellArray[self.ptr]
        else:
            self.cellArray[self.ptr] = self.register 
            self.register = None  
                
    def setZero(self):
        self.cellArray[self.ptr] = 0
        
    def printInt(self):
        print(self.cellArray[self.ptr])
    
    def printChar(self):
        print(chr(self.cellArray[self.ptr]), end="")
        
    def readInt(self):
        self.cellArray[self.ptr] = int(input())
    
    def readChar(self):
        self.cellArray[self.ptr] = ord(input())
        
    def getLoopStart(self, commandPtr) :
        start = commandPtr
        commandPtr -= 1
        level = 1
        while (level > 0):
            commandPtr -= 1
            if commandPtr < 0:
                sys.exit("ERROR -- Loop not initialized: floating 'moo' at instruction [" + str(start) +"] Terminating program")
            if self.commands[commandPtr] == 0:
                level += 1
            elif self.commands[commandPtr] == 7:
                level -= 1
        if level != 0:
            pass
        return commandPtr
            
    def getLoopEnd(self, commandPtr):
        start = commandPtr
        layer = 1
        commandPtr += 1
        while (layer >0):
            commandPtr += 1
            if commandPtr > len(self.commands):
                sys.exit("ERROR -- Loop not closed: floating 'MOO' at instruction [" +str(start)+"] Terminating program")
            if self.commands[commandPtr] == 7:
                layer += 1
            elif self.commands[commandPtr] == 0:
                layer -= 1
        if layer != 0:
            pass
        return commandPtr
                
def main (args):
    filename = args.input
    
    if not os.path.isfile(filename):
        raise Exception("File not found")
    
    file = open(filename, "rt")
    if not file.readable():
        raise Exception("File is not readable")
    lines = '\n'.join(file.readlines())
    
    interpreter = cow()
    interpreter.interpret(lines)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The input file")
    args = parser.parse_args()
    main(args)