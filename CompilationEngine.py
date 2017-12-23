import xml.etree.ElementTree as et
import JackTokenizer


class CompilationEngine:

    def __init__(self, filename):
        self.tokenizer = JackTokenizer.JackTokenizer(filename)
        # Keeps track of the current node we're writing to. Initialized as 'class' node.
        self.current_node = et.Element('class')
        # The xml tree that the engine builds
        self.tree = et.ElementTree()._setroot(self.current_node)

    def writeNode(self, tag = None, text = None):
        """Writes the current token as an xml node under the current node."""
        if tag is None and text is None:
            et.SubElement(self.current_node, self.tokenizer.tokenType, text=str(self.tokenizer.tokenVal))
        else:
            et.SubElement(self.current_node, tag, text=text)

    def compileClass(self):
        self.tokenizer.advance()
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
            elif self.tokenizer.tokenVal in ['constructor', 'function', 'method']:
                self.compileSubroutineDec()
                # This advances either to }, or to first token of a classVarDec or subroutineDec.
                self.tokenizer.advance()

        self.writeNode()  # Writes }

    def compileClassVarDec(self):
        # Writes <classVarDec> under the current node and makes it the current node
        # et doesn't have a getParent() function, so we save the current node in order to get back to it
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'classVarDec')
        while self.tokenizer.tokenVal != ';':
            print(self.tokenizer.tokenVal)
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
        self.tokenizer.advance()  # This advances either to ) or the first parameter type.
        self.compileParameterList()
        self.writeNode()  # Writes )
        self.tokenizer.advance()  # This advances to {
        self.compileSubroutineBody()  # When this finishes the current token is }
        self.current_node = parent

    def compileParameterList(self):
        """Writes the parameter list to the xml tree not including parentheses.
        When this is called the current token is either ) or the first parameter type.
        When this finishes the current token is )."""
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
        """Writes the subroutine body to the xml including { and }.
        When this method is called the current token is {"""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'subroutineBody')
        self.writeNode()  # Writes {
        self.tokenizer.advance()  # This advances to }, var or the first statement token.
        while self.tokenizer.tokenVal == 'var':
            self.compileVarDec()
            self.tokenizer.advance()  # This advances either to a 'var' token or to the first statement token.
        # The statements node is written whether or not there exist any statements.
        self.compileStatements()
        self.writeNode()  #  Writes }
        self.current_node = parent

    def compileVarDec(self):
        """Writes a varDec node to the xml tree.
        When this method is called the current token is 'var'.
        When this method finishes the current token is the last ;"""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'varDec')
        while self.tokenizer.tokenVal != ';':
            self.writeNode()  # Writes var, type, ',' or varName
            self.tokenizer.advance()
        self.writeNode()  # Writes ';'
        self.current_node = parent

    def compileStatements(self):
        """Writes the statements node of a subroutine body to the xml tree.
        When this method is called the current token is the first statement token.
        When this finishes the current token is } ending the body of the subroutine or conditional clause."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'statements')
        while self.tokenizer.tokenVal != '}':
            if self.tokenizer.tokenVal == 'let':
                self.compileLet()
                self.tokenizer.advance()  # Advances to another statement token or to }.
            elif self.tokenizer.tokenVal == 'if':
                self.compileIf()
                self.tokenizer.advance()
            elif self.tokenizer.tokenVal == 'while':
                self.compileWhile()
                self.tokenizer.advance()  # Advances to another statement token or to }.
            elif self.tokenizer.tokenVal == 'do':
                self.compileDo()
                self.tokenizer.advance()  # Advances to another statement token or to }.
            elif self.tokenizer.tokenVal == 'return':
                self.compileReturn()
                self.tokenizer.advance()  # Should advance to } but another statement token is also supported.
        self.current_node = parent

    def compileLet(self):
        """Writes a 'let' node to the xml tree.
        When this is called the current token is 'let'.
        When this finishes the current token is ;"""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'letStatement')
        self.writeNode()  # Writes 'let'.
        self.tokenizer.advance()
        self.writeNode()  # Writes varName
        self.tokenizer.advance()  # Advances to [ or =
        if self.tokenizer.tokenVal == '[':
            self.writeNode()  # Writes [
            self.tokenizer.advance()  # Advances to first token of an expression
            self.compileExpression()  # When this finishes the current token is the last token of expression
            self.tokenizer.advance()  # Advances to the first token of an expression, or to ]
            self.writeNode()  # Writes ]
            self.tokenizer.advance()  # Advances to =
        self.writeNode()  # Writes =
        self.tokenizer.advance()  # Advances to expression
        self.compileExpression()
        self.tokenizer.advance()  # Advances to ;
        self.writeNode()  # Writes ;
        self.current_node = parent

    def compileIf(self):
        """Writes an 'if' subtree to the xml tree.
        When this is called the current token is 'if'.
        When this finishes the current token is } ending the if or the else."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'ifStatement')
        self.writeNode()  # Writes 'if'.

    def compileExpression(self):
        """Writes an expression subtree to the xml tree.
        When this is called the current token is the first token of the expression
        When this finishes the current token is the first toke AFTER expression."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'expression')
        self.compileTerm()

    def compileTerm(self):
        """Writes a term subtree to the xml tree.
        When this is called the current token is the first token of the expression.
        When this finishes the current token is the first token AFTER the expression.
        The functions looks at the two first tokens to determine the type of term to write."""
        firstType = self.tokenizer.tokenType  # The first token type
        firstVal = self.tokenizer.tokenVal  # The first token value
        self.tokenizer.advance()  # Advances to the second token of the term, or to the first token after the term.
        secondType = self.tokenizer.tokenType  # The second token type
        secondVal = self.tokenizer.tokenVal  # The second token value

        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'term')

        # Handles unaryOp term
        if firstVal in ['-', '~']:
            self.writeNode(firstType, firstVal)
            self.compileTerm()

        # Handles a constant term
        elif firstType in ['keyword', 'integerConstant', 'stringConstant'] or firstVal in ['true', 'false', 'this', 'null']:
            self.writeNode(firstType, firstVal)

        # Handles (expression)
        elif firstVal == '(':
            self.writeNode(firstType, firstVal)  # Writes (
            self.compileExpression()  # After this the current token is the one after the expression.
            self.writeNode()  # Writes )
            self.tokenizer.advance()  # Advances to token after the term.

        # Handles varName [expression]
        elif secondVal == '[':
            self.writeNode(firstType, firstVal)  # Writes varName
            self.writeNode()  # Writes [
            self.compileExpression()  # When this finishes the current token is ]
            self.writeNode()  # Writes ]
            self.tokenizer.advance()  # Advances to token after term.

        # Handles subroutineCall
        elif firstType == 'identifier' and secondVal in ['.', '(']:
            # When this is called the current token is the SECOND token in the subroutineCall.
            # When this finishes the current token is ..........
            self.compileSubroutineCall(firstType, firstVal)

        # Handles varName
        else:
            self.writeNode(firstType, firstVal)

        self.current_node = parent

    def compileSubroutineCall(self, firstType, firstVal):
        """Writes a subroutine call to the xml tree.
        This does not write a subroutineCall node. The nodes this creates are written in sequence under current node.
        When this is called the current token is the SECOND token of the subroutine call."""
        self.writeNode(firstType, firstVal) # Writes a subroutineName, className or varName.
        self.writeNode()  # Writes ( or .
        if self.tokenizer.tokenVal == '.':
            self.tokenizer.advance()  # Advances to subroutineName
            self.writeNode()  # Writes subroutineName
            self.tokenizer.advance()  # Advances to (
            self.writeNode()  # Writes (
        # At this point the current token is expressionList.
        self.compileExpressionList()

    def compileExpressionList(self):
        """"""











