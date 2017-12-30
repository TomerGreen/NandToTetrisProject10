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
        self.replaceSymbols()
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
        self.remove_comments()
        # print(self.lines)  # Prints text
        # print (type(self.word))
        # print(type(self.lines
        #       ))
        # print("debug here")
        words = re.findall(self.word, self.lines)
        # print(type(words))
        # print(words)
        # clean_code = ""
        # for word in words:
        #     for thing in word:
        #         if len(thing) > 0:
        #             clean_code += thing + " "
        # print(clean_code)
        token_list = []
        for line in words:
            token_list.append(self.distinct_token(line))
        # print(token_list)
        return token_list

    def replaceSymbols(self):
        replaced_tokens = []
        for token in self.tokens:
            if token[1] == '&':
                replaced_tokens.append((token[0], '&amp;'))
            elif token[1] == '"':
                replaced_tokens.append((token[0], '&quot;'))
            elif token[1] == '>':
                replaced_tokens.append((token[0], '&gt;'))
            elif token[1] == '<':
                replaced_tokens.append((token[0], '&lt;'))
            else:
                replaced_tokens.append(token)
        self.tokens = replaced_tokens

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
#anthor try


