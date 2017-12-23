import sys
import os
import CompilationEngine


def compileFile(filename):
    engine = CompilationEngine.CompilationEngine(filename)
    engine.compileClass()
    engine.tree.write(filename.replace('.jack', '.xml'))

def compileAll(path):
    if path.endswith('.jack'):
        compileFile(path)
    else:
        for filename in os.listdir(path):
            if filename.endswith('.jack'):
                compileFile(path + '/' + filename)


if __name__ == "__main__":
    path = sys.argv[1]
    compileAll(path)