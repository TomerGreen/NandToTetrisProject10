import xml.etree.ElementTree as et
import JackTokenizer


class CompilationEngine:

    def __init__(self, filename):
        self.tokenizer = JackTokenizer.JackTokenizer(filename)
        ############# REMOVE ####################
        elementDict = {"1": 'keyword', "2": 'symbol', "3": 'integerConstant', "4": 'stringConstant', "5": 'identifier'}
        new_tokens = list()
        for token in self.tokenizer._tokens:
            new_type = elementDict[str(token[0])]
            new_token = (new_type, token[1])
            new_tokens.append(new_token)
        self.tokenizer._tokens = new_tokens
        #########################################
        # Keeps track of the current node we're writing to. Initialized as 'class' node.
        self.current_node = et.Element('class')
        # The root of the xml tree that the engine builds
        self.root = self.current_node

    def writeNode(self, tag = None, text = None):
        """Writes the current token as an xml node under the current node."""
        if tag is None and text is None:
            tag = str(self.tokenizer.tokenType)
            text = str(self.tokenizer.tokenVal)
        newNode = et.SubElement(self.current_node, str(tag))
        newNode.text = str(text)
        print(newNode.text)

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
            self.writeNode()  # Writes the first parameter type
            self.tokenizer.advance()  # Advances to first parameter value
            self.writeNode()  # Writes the first parameter value
            self.tokenizer.advance()  # Advances to ) or to ,
        while self.tokenizer.tokenVal != ')':
            self.writeNode()  # Writes ,
            self.tokenizer.advance()
            self.writeNode()  # Writes the parameter type
            self.tokenizer.advance()
            self.writeNode()  # Writes the parameter value
            self.tokenizer.advance()  # Advances to , or )
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
                self.compileIf()  # Finishes at next statement or at }
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
            self.compileExpression()  # When this finishes the current token is the one after the expression
            self.writeNode()  # Writes ]
            self.tokenizer.advance()  # Advances to =
        self.writeNode()  # Writes =
        self.tokenizer.advance()  # Advances to expression
        self.compileExpression()  # Finishes at ;
        self.writeNode()  # Writes ;
        self.current_node = parent

    def compileIf(self):
        """Writes an 'if' subtree to the xml tree.
        When this is called the current token is 'if'.
        When this finishes the current token is the one AFTER the closing } or the if or else clause."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'ifStatement')
        self.writeNode()  # Writes 'if'.
        self.tokenizer.advance()  # Advances to (
        self.writeNode()  # Writes (
        self.tokenizer.advance()  # Advances to expression
        self.compileExpression()  # Finishes at )
        self.writeNode()  # Writes )
        self.tokenizer.advance()  # Advances to {
        self.writeNode()  # Writes {
        self.tokenizer.advance()  # Advances to statements block.
        self.compileStatements()  # When this finishes the current token is }
        self.writeNode()  # Writes }
        self.tokenizer.advance()  # Advances to 'else' or to another statement or to } ending the statements block.
        if self.tokenizer.tokenVal == 'else':
            self.writeNode()  # Writes 'else'
            self.tokenizer.advance()  # Advances to {
            self.writeNode()  # Writes {
            self.tokenizer.advance()  # Advances to a statements block
            self.compileStatements()  # Ends at }
            self.writeNode()  # Writes }
            self.tokenizer.advance()  # Advances to a new statement or to the } after the statements block.
        self.current_node = parent

    def compileWhile(self):
        """Writes a while node to the xml tree.
        When this is called the current token is 'while'.
        When this finishes the current token is the } closing the while clause."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'whileStatement')
        self.writeNode()  # Writes 'while'
        self.tokenizer.advance()  # Advances to (
        self.writeNode()  # Writes (
        self.tokenizer.advance()  # Advances to the first token in an expression.
        self.compileExpression()  # Ends at )
        self.writeNode()  # Writes )
        self.tokenizer.advance()  # Advances to {
        self.writeNode()  # Writes {
        self.tokenizer.advance()  # Advances to a statements block.
        self.compileStatements()  # Ends at the } closing the while clause.
        self.writeNode()  # Writes }.
        self.current_node = parent

    def compileDo(self):
        """Writes a 'doStatement' node to the xml tree.
        When this is called the current token is 'do'.
        When this finishes the current token is the ; ending the do statement."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'doStatement')
        self.writeNode()  # Writes 'do'.
        self.tokenizer.advance()  # Advances to first token in a subroutine call.
        firstType = self.tokenizer.tokenType
        firstVal = self.tokenizer.tokenVal
        self.tokenizer.advance()  # Advances to the second token in the subroutine call.
        self.compileSubroutineCall(firstType, firstVal)  # Starts at second token and ends at the last token of call.
        self.tokenizer.advance()  # Advances to ;
        self.writeNode()  # Writes ;
        self.current_node = parent

    def compileReturn(self):
        """Writes a 'returnStatement' node to the xml tree.
        When this is called the current token is 'return'.
        When this finishes the current token is the ; ending the return statement."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'returnStatement')
        self.writeNode()  # Writes 'return'
        self.tokenizer.advance()  # Advances to ; or to an expression.
        if self.tokenizer.tokenVal != ';':
            self.compileExpression()  # Finishes when current token is ;
        self.writeNode()  # Writes ;
        self.current_node = parent

    def compileExpression(self):
        """Writes an expression node to the xml tree.
        When this is called the current token is the first token of the expression
        When this finishes the current token is the first token AFTER expression."""
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'expression')
        self.compileTerm()  # When this finishes the current token is either an operator or: ')', ';' or ']'.
        while self.tokenizer.tokenVal in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.writeNode()  # Writes the operator
            self.tokenizer.advance()  # Advances to the first token in a term.
            self.compileTerm()  # When this finishes the current token is an operator or ')', ';' or ']'.
        self.current_node = parent

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

        # Handles varName[expression]
        elif secondVal == '[':
            self.writeNode(firstType, firstVal)  # Writes varName
            self.writeNode()  # Writes [
            self.tokenizer.advance()  # Advances to beginning of expression.
            self.compileExpression()  # When this finishes the current token is ]
            self.writeNode()  # Writes ]
            self.tokenizer.advance()  # Advances to token after term.

        # Handles subroutineCall
        elif firstType == 'identifier' and secondVal in ['.', '(']:
            # When this is called the current token is the SECOND token in the subroutineCall.
            # When this finishes the current token is the last token in the subroutine call
            self.compileSubroutineCall(firstType, firstVal)
            self.tokenizer.advance()  # Advances to the token after the ) that ends the subroutineCall

        # Handles varName
        else:
            self.writeNode(firstType, firstVal)

        self.current_node = parent

    def compileSubroutineCall(self, firstType, firstVal):
        """Writes a subroutine call to the xml tree.
        This does not write a subroutineCall node. The nodes this creates are written in sequence under current node.
        When this is called the current token is the SECOND token of the subroutine call.
        When this finishes the current token is the ) that marks the end of the subroutine call expression list."""
        self.writeNode(firstType, firstVal) # Writes a subroutineName, className or varName.
        self.writeNode()  # Writes ( or .
        if self.tokenizer.tokenVal == '.':
            self.tokenizer.advance()  # Advances to subroutineName
            self.writeNode()  # Writes subroutineName
            self.tokenizer.advance()  # Advances to (
            self.writeNode()  # Writes (
        self.tokenizer.advance()
        # At this point the current token is the first token in expressionList, or ) if the list is empty.
        self.compileExpressionList()
        self.writeNode()  # Writes )

    def compileExpressionList(self):
        """Writes an expressionList node to the xml tree.
        When this is called the current token is the first token in expressionList or ) if it's empty.
        When this finishes the current token is ).
        """
        parent = self.current_node
        self.current_node = et.SubElement(self.current_node, 'expressionList')
        if self.tokenizer.tokenVal != ')':
            self.compileExpression()  # When this finishes the current token is either , or )
        while self.tokenizer.tokenVal != ')':
            self.writeNode()  # Writes ,
            self.tokenizer.advance()  # Advances to a new expression.
            self.compileExpression()  # After this current node is , or )
        self.current_node = parent











