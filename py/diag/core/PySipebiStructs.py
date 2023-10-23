
# This file contains the struct of text, paragraph, word, and punctuation


class PySipebiTextDivision:
    def __init__(self, text=''):
        self.text = text
        self.length = len(text) 
        self.paragraph_divs: PySipebiParagraphDivision = []
        
        self.process_text()

    # method for adding paragraph division to the list
    def add_paragraph_division(self, paragraph_division):
        self.paragraph_divs.append(paragraph_division)

    # method for separating paragraph by line break
    def separate_paragraph_by_line_break(self):
        paragraph_divs = self.text.split("\n")
        offset = 0
        for i in range(len(paragraph_divs)):
            if i > 0:
                # 2 is the length of line break character
                offset += len(paragraph_divs[i-1]) + 2
            self.add_paragraph_division(PySipebiParagraphDivision(i+1, offset, paragraph_divs[i], len(paragraph_divs[i])))

    # method for tokenizing words in all paragraphs
    def process_paragraph_divisions(self):
        for paragraph_div in self.paragraph_divs:
            paragraph_div.tokenize_words()

    # method for creating struct of text (including tokenizing), called when the object is created
    def process_text(self):
        self.separate_paragraph_by_line_break()
        self.process_paragraph_divisions()

    def __str__(self):
        return self.text


class PySipebiParagraphDivision:
    def __init__(self, index, offset, text, length):
        self.index = index
        self.offset = offset
        self.text = text
        self.length = length

        self.word_divs: PySipebiWordDivision = [] # list of word divisions in this paragraph
        self.size = 0 # number of word divisions in this paragraph

    def add_word_division(self, word_division):
        self.word_divs.append(word_division)
        self.size += 1

    # create a method to split word by one space or more
    def tokenize_words(self):
        word_divs = self.text.split()
        offset = 0
        for i in range(len(word_divs)):
            # create a word division object
            word_div = PySipebiWordDivision(original_string=word_divs[i])

            if i > 0:
                # 1 is the length of space character
                offset += len(word_divs[i-1]) + 1

                # setting next and previous word division
                word_div.prev_word_div = self.word_divs[self.size-1]
                word_div.prev_word_div.next_word_div = word_div

                # checking if a word only contains punctuation
                if not word_div.clean_word_string:
                    if word_div.has_post_word:
                        ori_string = word_div.prev_word_div.clean_post_word
                        new_word = word_div.pre_clean_word + ori_string + word_div.clean_post_word
                        offset -= 1
                        self.word_divs[self.size-1] = PySipebiWordDivision(element_no=self.size, original_string=new_word, offset=self.word_divs[self.size-1].position_offset)
                    else:
                        if i < len(word_divs) - 1:
                            offset -= 2
                            word_divs[i+1] = word_div.pre_clean_word + word_divs[i+1]
                    
                    continue
                

            word_div.position_offset = offset
            word_div.element_no = self.size + 1
            self.add_word_division(word_div)
        
    # def tokenize_words_modified(self):
        # word_divs = self.text.split()
        # word_divs_modified = word_divs.copy()
        # # tokenize word by space and set the next and previous word division
        # offset = 0
        # counter = 0
        # while counter < len(word_divs_modified):
        #     word_div = PySipebiWordDivision(original_string=word_divs_modified[counter])
        #     if len(word_div.get_analyzed_word_divs()) > 1:
        #         word_divs_modified.pop(counter)
        #         for i in range(len(word_div.get_analyzed_word_divs())):
        #             word_divs_modified.insert(counter+i, word_div.get_analyzed_word_divs()[i])
        #         continue

            
        #     if counter > 0:
        #         offset += len(word_divs_modified[counter-1]) + 1
        #         word_div.prev_word_div = self.word_divs[self.size-1]
        #         word_div.prev_word_div.next_word_div = word_div
        #         if not word_div.clean_word_string:
        #             if word_div.has_post_word:
        #                 ori_string = word_div.prev_word_div.clean_post_word
        #                 new_word = word_div.pre_clean_word + ori_string + word_div.clean_post_word
        #                 offset -= 1
        #                 self.word_divs[self.size-1] = PySipebiWordDivision(element_no=self.size, original_string=new_word, offset=self.word_divs[self.size-1].position_offset)
        #             else:
        #                 if counter < len(word_divs_modified) - 1:
        #                     offset -= 2
        #                     word_divs_modified[counter+1] = word_div.pre_clean_word + word_divs_modified[counter+1]
        #             continue
        #     word_div.position_offset = offset
        #     word_div.element_no = self.size + 1
        #     self.add_word_division(word_div)
        #     counter += 1

    def __str__(self):
        return self.text
    
class PySipebiWordDivision:
    DOUBLE_QUOTE_APPEAR = False

    def __init__(self, element_no=-1, original_string='', offset=-1):
        self.original_string = original_string # original word
        self.element_no = element_no # element number in the paragraph
        self.position_offset = offset # position offset in the paragraph
        self.clean_word_string = original_string.strip() # word without punctuation
        self.pre_word: PySipebiPreWordPunctuation = PySipebiPreWordPunctuation() # punctuation before the word
        self.post_word: PySipebiPostWordPunctuation = PySipebiPostWordPunctuation() # punctuation after the word

        self.is_handled = False # flag to indicate if the word has been handled
        
        self.next_word_div: PySipebiWordDivision = None # next word division
        self.prev_word_div: PySipebiWordDivision = None # previous word division

        self.process_word()

    # Method for checking if a word contains punctuation in middle of word, example: 'aku,"mau,kamu."'
    # Pisahkan 'aku,"mau,kamu."' menjadi 'aku,"', 'mau,', 'kamu."', kemudian cek setiap kata
    # def get_analyzed_word_divs(self):
    #     analyzed_word_divs = []

    #     i = 0
    #     while i < len(self.clean_word_string): 
    #         if self.clean_word_string[i] == '"':
    #             if not self.DOUBLE_QUOTE_APPEAR:
    #                 analyzed_word_divs.append(self.clean_word_string[:i])
    #                 analyzed_word_divs.append(self.clean_word_string[i:])
    #             else:
    #                 analyzed_word_divs.append(self.clean_word_string[:i+1])
    #                 analyzed_word_divs.append(self.clean_word_string[i+1:])
    #             self.DOUBLE_QUOTE_APPEAR = not self.DOUBLE_QUOTE_APPEAR
    #         else:
    #             if self.clean_word_string[i] in PySipebiPunctuationDivision.PRE_CHARS_OMITTED:
    #                 analyzed_word_divs.append(self.clean_word_string[:i])
    #                 analyzed_word_divs.append(self.clean_word_string[i:])
    #             if self.clean_word_string[i] in PySipebiPunctuationDivision.POST_CHARS_OMITTED:
    #                 for j in range(i+1, len(self.clean_word_string)):
    #                     if self.clean_word_string[j].isalnum() or self.clean_word_string[j] == '"' and not self.DOUBLE_QUOTE_APPEAR:
    #                         self.DOUBLE_QUOTE_APPEAR = True
    #                         i = j - 1
    #                         break;
    #                 analyzed_word_divs.append(self.clean_word_string[:i+1])
    #                 analyzed_word_divs.append(self.clean_word_string[i+1:])
    #         i += 1
    #     return analyzed_word_divs

    def _check_pre_word(self):
        for char in self.clean_word_string:
            self.DOUBLE_QUOTE_APPEAR = char == '"' and not self.DOUBLE_QUOTE_APPEAR
            if char in PySipebiPunctuationDivision.PRE_CHARS_OMITTED:
                self.pre_word.add_punctuation_division(char)
            else:
                break
        if self.pre_word.has_punctuation_div:
            self.clean_word_string = self.clean_word_string[self.pre_word.length:]

    def _check_post_word(self):
        for char in reversed(self.clean_word_string):
            self.DOUBLE_QUOTE_APPEAR = char == '"' and not self.DOUBLE_QUOTE_APPEAR
            if char in PySipebiPunctuationDivision.POST_CHARS_OMITTED:
                self.post_word.add_punctuation_division(char)
            else:
                break
        if self.post_word.has_punctuation_div:
            self.clean_word_string = self.clean_word_string[:-self.post_word.length]

    def process_word(self):
        self._check_pre_word()
        self._check_post_word()

    @property
    def has_pre_word(self):
        return self.pre_word.has_punctuation_div
    
    @property
    def has_post_word(self):
        return self.post_word.has_punctuation_div
    
    def ended_with(self, character):
        return self.clean_word_string.endswith(character)
    
    def start_with(self, substring):
        return self.clean_word_string.startswith(substring)

    @property
    def pre_clean_word(self):
        return self.pre_word.string_repr + self.clean_word_string

    @property
    def clean_post_word(self):
        return self.clean_word_string + self.post_word.string_repr

    @property
    def first_char_is_letter(self):
        return self.first_char_is(str.isalpha)

    @property
    def first_char_is_capitalized(self):
        return self.first_char_is(str.isupper)

    @property
    def only_has_post_word(self):
        return not self.clean_word_string and self.post_word.has_punctuation_div

    @property
    def is_null_or_empty(self):
        return not self.original_string

    def __str__(self):
        return self.original_string
    
class PySipebiPunctuationDivision:
    PRE_CHARS_OMITTED = {'(', '\'', '"', '[', '{', '-'}
    POST_CHARS_OMITTED = {
        '?', ',', '!', '.', ')', ':', '\'', '"', '}',
        ']', ';', '-'
    }

    def __init__(self):
        self.punctuation_div = []

    @property
    def string_repr(self):
        return "".join(self.punctuation_div)

    @property
    def length(self):
        return len(self.punctuation_div)

    def add_punctuation_division(self, char):
        self.punctuation_div.append(char)
            
    def ended_with(self, character):
        return self.last_punctuation == character
    
    def start_with(self, character):
        return self.first_punctuation == character
    
    def contains(self, character):
        return character in self.punctuation_div
    
    def index(self, character):
        return self.punctuation_div.index(character)

    @property
    def last_punctuation(self):
        if self.has_punctuation_div:
            return self.punctuation_div[-1]
        return None
    @property
    def first_punctuation(self):
        if self.has_punctuation_div:
            return self.punctuation_div[0]
        return None
    
    @property
    def has_punctuation_div(self):
        return self.length != 0

    def __str__(self):
        return self.punctuation_div


class PySipebiPreWordPunctuation(PySipebiPunctuationDivision):
    pass

class PySipebiPostWordPunctuation(PySipebiPunctuationDivision):
    # override method
    def add_punctuation_division(self, char):
        return self.punctuation_div.insert(0, char)

class PySipebiNumericDivision(PySipebiWordDivision):
    pass
