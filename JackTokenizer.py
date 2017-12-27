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
    keywordsRegex = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbolsRegex = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    integerRegex = r'\d+'
    stringsRegex = r'"[^"\n]*"'
    identifiersRegex = r'[\w]+'
    word = re.compile(keywordsRegex + '|' + symbolsRegex + '|' + integerRegex + '|' + stringsRegex + '|' + identifiersRegex)

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
        if re.match(self.keywordsRegex, token):
            return self.KEYWORD, token
        elif re.match(self.identifiersRegex, token):
            return self.IDENTIFIER, token
        elif re.match(self.stringsRegex, token):
            return self.STRING, token[1:-1]
        elif re.match(self.integerRegex, token):
            return self.INTEGER, token
        elif re.match(self.symbolsRegex, token):
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


    """
    def remove_comments(self):
        text_with_no_comments = ''
        for i in range(len(self.lines)):
            char = self.lines[i]
            if char == "\"":
                end = self.lines.find("\"", i +1)
                text_with_no_comments += self.lines[i:end + 1]
            elif char == "/":
                if self.lines[i + 1] == "/":
                    text_with_no_comments += " "
                elif self.lines[i + 1] == "*":
                    text_with_no_comments += " "
                else:
                    text_with_no_comments += self.lines[i]
            else:
                text_with_no_comments += self.lines[i]
        return text_with_no_comments
    """

    def tokenizer(self):
        print ("PRINTING REMOVE COMMENTS")
        self.remove_comments()
        print(self.lines)  # Prints text
        print (type(self.word))
        print(type(self.lines
              ))
        print("debug here")
        words = re.findall(self.word, self.lines)
        print(type(words))
        print(words)
        # clean_code = ""
        # for word in words:
        #     for thing in word:
        #         if len(thing) > 0:
        #             clean_code += thing + " "
        # print(clean_code)
        token_list = []
        for line in words:
            print(line)
            token_list.append(self.distinct_token(line))
        print(token_list)
        return token_list

    def replace(self):
        for token in self.tokens:
            if token[1] == '&':
                return token[0], '&amp;'
            elif token[1] == '"':
                return token[0],'&quot;'
            elif token[1] == '>':
                return token[0], '&gt;'
            elif token[1] == '<':
                return token[0],'&lt'

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



#test
#push
#Wednesday afternoon

