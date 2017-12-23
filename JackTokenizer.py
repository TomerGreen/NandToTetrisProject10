import re
# CONSTANTS
KEYWORD = 'keyword'
SYMBOL = 'symbol'
STRING = 'stringConstant'
INTEGER = 'integerConstant'
IDENTIFIER = 'identifier'

# my tokenizer  VV

class JackTokenizer:

    INTEGER_REGEX = '\d+'
    STRING_REGEX = '"[^"\n]*."'
    SYMBOL_REGEX = '(\[\]\\\*<>=~|&{}\(\)\.,;\+-)'
    IDENTIFIER_REGEX = '[\w_]*'
    WORD_REGEX = '((class)|(constructor)|(function)|(method)|(field)|(static)' \
                 '|(var)|(int)|(char)|(boolean)|(void)|(true)|(false)|(null)' \
                 '|this|let|do|if|else|while|return))'

    "Opens the input file/stream and gets ready to tokenize it."
    def ___init___(self, inputFile):
        self.inputFile = open(inputFile, 'r')
        self.lines = self.inputFile.read()
        self.tokens = list()
        self.tokenData = ""

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
        filteredText = ''
        while currentIndex < len(self.lines):
            currentChar = self.lines[currentIndex]
            if currentChar == "\"":
                endIndex = self.lines.find("\"", currentIndex + 1)
                filteredText += self.lines[currentIndex:endIndex + 1]
                currentIndex = endIndex + 1
            elif currentChar == "/":
                if self.lines[currentIndex + 1] == "/":
                    endIndex = self.lines.find("\n", currentIndex + 1)
                    currentIndex = endIndex + 1
                    filteredText += " "
                elif self.lines[currentIndex + 1] == "*":
                    endIndex = self.lines.find("*/", currentIndex + 1)
                    currentIndex = endIndex + 2
                    filteredText += " "
                else:
                    filteredText += self.lines[currentIndex]
                    currentIndex += 1
            else:
                filteredText += self.lines[currentIndex]
                currentIndex += 1
        self.lines = filteredText
        return

        # re.sub(re.compile("\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+"), "",
        #        lines)
        # finder = re.findall(re.compile("\"[^\n\"]*\/\/[^\n\"]*\""), lines)
        # splittedContent = re.split(re.compile("\"[^\n\"]*\/\/[^\n\"]*\""), lines)
        # text_with_no_comments = re.sub(re.compile("\/\/[^\n]*\n"), "\n", splittedContent[0])
        #
        # # text_with_no_comments = ""
        # for char in self.lines:
        #     cur = self.lines[index]
        #     if cur == "\"":
        #         end = self.lines.find("\"", index+1)
        #         text_with_no_comments += self.lines[index:end]
        #     elif cur == "/":
        #         if self.lines[index +1]== "/":
        #             end = self.lines.find("\n", index +1)
        #             text_with_no_comments +=""
        #         elif self.lines[index +1]== "*":
        #             end = self.lines.find("*/", index+1)
        #             text_with_no_comments+=""
        #         else:
        #             text_with_no_comments += self.lines[index]
        #     else:
        #         text_with_no_comments += self.lines[index]
        # self.lines = text_with_no_comments
        # return self.lines

    def tokenizer(self):
        filter_lines = self.split(self.lines)
        for word in filter_lines:
            self.tokens.append(word)
        return self.tokens
        # for lines in self.lines:
        #     self.remove_comments()

    # def remove_multiLine(self, content):
    #     return re.sub(re.compile("\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/"), "", content)

    # def remove_singleLines(self, content):
    #     finder = re.findall(re.compile("\"[^\n\"]*\/\/[^\n\"]*\""), content)
    #     splittedContent = re.split( re.compile("\"[^\n\"]*\/\/[^\n\"]*\""), content)
    #     newContent = re.sub(False, "\n", splittedContent[0])
    #     for idx, elem in enumerate(splittedContent[1:]):
    #         newContent += finder[idx] + "\n" + re.sub(False, "\n",
    #                                                   elem)
    #     return newContent
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
            self.tokenData =  self.tokens.pop(0)




    def tokenVal(self):
        return self.tokenData[1]

    def tokenType(self):
        return self.tokenData[0]

