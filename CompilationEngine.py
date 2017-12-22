import xml.etree.ElementTree as et
import JackTokenizer


class CompilationEngine:

    def __init__(self, filename):
        self.tokenizer = JackTokenizer.JackTokenizer(filename)
        xml_filename = filename.split('.') + '.xml'
        self.file = open(xml_filename, 'w')
        self.root = et.Element('class')  # The root of the xml tree that the engine builds
        self.current_node = self.root  # Keeps track of the current node we're writing to

    def writeNode(self):
        """Writes the current token as an xml node under the current node."""
        et.SubElement(self.current_node, tag=self.tokenizer.tokenType, text=str(self.tokenizer.tokenVal))

    def compileClass(self):
        self.writeNode()  # Writes 'class'
        self.tokenizer.advance()
        self.writeNode()  # Writes the class name identifier
        self.tokenizer.advance()
        self.writeNode()  # Writes {
        self.tokenizer.advance()

        # Writes the content of the class
        while self.tokenizer.tokenVal != '}':
            if self.tokenizer.tokenVal in ['static', 'field']:
                self.compileClassVarDec()
                self.tokenizer.advance()
            elif self.tokenizer.tokenVal in ['constructor', 'function' , 'method']
                self.compileSubroutineDec()
                self.tokenizer.advance()

        self.writeNode()  # Writes }

    def compileClassVarDec(self):
        # Writes <classVarDec> under the current node and makes it the current node
        # et doesn't have a getParent() function, so we save the current node in order to get back to it
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'classVarDec')
        while self.tokenizer.tokenVal != ';':
            self.writeNode()
            self.tokenizer.advance()
        self.writeNode()  # Writes ;
        self.current_node = parent

    def compileSubroutineDec(self):
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'subroutineDec')
        self.writeNode()  # Writes constructor/function/method
        self.tokenizer.advance()
        self.writeNode()  # Writes the subroutine type
        self.tokenizer.advance()
        self.writeNode()  # Writes the subroutine name
        self.tokenizer.advance()
        self.writeNode()  # Writes (
        self.tokenizer.advance()
        self.compileParameterList()
        self.writeNode()  # Writes )
        self.tokenizer.advance()
        self.writeNode()  # Writes {
        self.tokenizer.advance()
        self.compileSubroutineBody()
        self.writeNode()  # Writes }
        self.current_node = parent

    def compileParameterList(self):
        """Writes the parameter list to the xml tree not including parentheses."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'parameterList')
        if self.tokenizer.tokenVal != ')':
            self.writeNode()  # Writes the first parameter
            self.tokenizer.advance()
        while self.tokenizer.tokenVal != ')':
            self.writeNode()  # Writes ,
            self.tokenizer.advance()
            self.writeNode()  # Writes the parameter
            self.tokenizer.advance()
        self.current_node = parent

    def compileSubroutineBody(self):
        """Writes the subroutine body to the xml not including { and }"""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'subroutineBody')
        while self.tokenizer.tokenVal == 'var'
            self.compileVarDec()
            self.tokenizer.advance()
        while self.tokenizer.tokenVal != '}'
            self.compileStatements()
            self.tokenizer.advance()  ########### IMPORTANT: I ADVANCE PAST THE STATEMENT BECAUSE compilesubroutinedec writes the }
        self.current_node = parent

    def compileVarDec(self):
        """Writes a varDec node to the xml tree"""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'varDec')
        while self.tokenizer.tokenVal != ';':
            self.writeNode()  # Writes var, type, ',' or varName
            self.tokenizer.advance()
        self.writeNode()  # Writes ';'
        self.current_node = parent
