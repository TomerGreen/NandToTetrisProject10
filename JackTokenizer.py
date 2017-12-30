import re

# my tokenizer

class JackTokenizer:
    # CONSTANTS
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    STRING = 'stringConstant'
    INTEGER = 'integerConstant'
    IDENTIFIER = 'identifier'



    KeywordsCodes = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                 "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    SymbolsCodes = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~'}
    WORDS_REGEX = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    SYMBOL_REGEX = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    INT_REGEX = r'\d+'
    STRING_REGEX = r'"[^"\n]*"'
    IDENTIFIER_REGEX = r'[A-Za-z_]\w*'
    word = re.compile(WORDS_REGEX + '|' + SYMBOL_REGEX + '|' + INT_REGEX + '|' + STRING_REGEX + '|' + IDENTIFIER_REGEX)

    def __init__(self, inputFile):
        """
        Opens the input file/stream and gets ready to tokenize it.
        :param inputFile:
        """
        self.inputFile = open(inputFile, 'r')
        self.lines = self.inputFile.read()
        self.tokens = self.tokenizer()
        self.tokenType = ""
        self.tokenVal = ""

    def distinct_token(self, token):
        if re.match(self.WORDS_REGEX, token):
            return self.KEYWORD, token
        elif re.match(self.IDENTIFIER_REGEX, token):
            return self.IDENTIFIER, token
        elif re.match(self.STRING_REGEX, token):
            return self.STRING, token[1:-1]
        elif re.match(self.INT_REGEX, token):
            return self.INTEGER, token
        elif re.match(self.SYMBOL_REGEX, token):
            return self.SYMBOL, token

    def remove_comments(self):
        """Sets lines to a list of lines without comments"""
        full_text = ''.join(self.lines)
        def ignore_normal_strings(match):
            if match.group(0)[0] == '/':
                return ""
            else:
                return match.group(0)

        pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|'
                             r'"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
        self.lines = re.sub(pattern, ignore_normal_strings, full_text)


    def tokenizer(self):
        self.remove_comments()
        words = re.findall(self.word, self.lines)
        token_list = []
        for line in words:
            token_list.append(self.distinct_token(line))
        return token_list

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
            tokenData = self.tokens.pop(0)
            self.tokenVal = tokenData[1]
            self.tokenType = tokenData[0]

    def tokenVal(self):
        return self.tokenVal

    def tokenType(self):
        return self.tokenType


#test
#push
#Wednesday afternoon
#anthor try
#done


