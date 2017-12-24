import re

# my tokenizer

class JackTokenizer:
    # CONSTANTS
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    STRING = 'stringConstant'
    INTEGER = 'integerConstant'
    IDENTIFIER = 'identifier'

    symbol_dict = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}


    INTEGER_REGEX = '\d+'
    STRING_REGEX = '"[^"\n]*."'
    SYMBOL_REGEX = '(\[\]\\\*<>=~|&{}\(\)\.,;\+-)'
    IDENTIFIER_REGEX = '[\w_]*'
    WORD_REGEX = '((class)|(constructor)|(function)|(method)|(field)|(static)' \
                 '|(var)|(int)|(char)|(boolean)|(void)|(true)|(false)|(null)' \
                 '|this|let|do|if|else|while|return))'
    LEXICAL_ANALYSIS = re.compile('{}|{}|{}|{}|{}'.format(WORD_REGEX,
                                      SYMBOL_REGEX, INTEGER_REGEX,
                                           STRING_REGEX, IDENTIFIER_REGEX))


    "Opens the input file/stream and gets ready to tokenize it."
    def __init__(self, inputFile):
        self.inputFile = open(inputFile, 'r')
        self.lines = self.inputFile.read()
        self.tokens = list()
        self.tokenType = ""
        self.tokenVal = ""

    def distinct_token(self, token):
        if re.match(self.WORD_REGEX, token):
            return "keyword", token
        elif re.match(self.IDENTIFIER_REGEX, token):
            return "identifier", token
        elif re.match(self.STRING_REGEX, token):
            return "string", token[1:-1]
        elif re.match(self.INTEGER_REGEX, token):
            return "integer", token
        elif re.match(self.SYMBOL_REGEX, token):
            return "symbol", token


    def remove_comments(self):
        currentIndex = 0
        text_with_no_comments = ''
        while currentIndex < len(self.lines):
            currentChar = self.lines[currentIndex]
            if currentChar == "\"":
                endIndex = self.lines.find("\"", currentIndex + 1)
                text_with_no_comments += self.lines[currentIndex:endIndex + 1]
                currentIndex = endIndex + 1
            elif currentChar == "/":
                if self.lines[currentIndex + 1] == "/":
                    endIndex = self.lines.find("\n", currentIndex + 1)
                    currentIndex = endIndex + 1
                    text_with_no_comments += " "
                elif self.lines[currentIndex + 1] == "*":
                    endIndex = self.lines.find("*/", currentIndex + 1)
                    currentIndex = endIndex + 2
                    text_with_no_comments += " "
                else:
                    text_with_no_comments += self.lines[currentIndex]
                    currentIndex += 1
            else:
                text_with_no_comments += self.lines[currentIndex]
                currentIndex += 1
        self.lines = text_with_no_comments


    def tokenizer(self):
        filter_lines = self.LEXICAL_ANALYSIS.findall(self.lines)
        for word in filter_lines:
            self.tokens.append(word)
        return self.tokens

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        :return: boolean
        """
        return len(self.tokens) != 0


    def advance(self):
        """
        Gets the next token from the input and
    makes it the current token. This method
    should only be called if hasMoreTokens()
    is true. Initially there is no current token.
        :return:
        """
        if self.hasMoreTokens():
            tokenData = self.tokens.pop()
            self.tokenVal = tokenData[1]
            self.tokenType = tokenData[0]

    def tokenVal(self):
        return self.tokenVal

    def tokenType(self):
        return self.tokenType
