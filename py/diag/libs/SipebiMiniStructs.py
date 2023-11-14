
# This class are representation of text in Sipebi Mini
class SipebiMiniText:
    def __init__(self, text=''):
        self.text = text
        self.length = len(text) 
        self.paragraph_divs: SipebiMiniParagraph = []
        
        self.process_text()

    def add_paragraph_division(self, paragraph_division):
        self.paragraph_divs.append(paragraph_division)

    # method untuk memisahkan paragraph berdasarkan line break
    def separate_paragraph_by_line_break(self):
        paragraph_divs = self.text.split("\n")
        offset = 0
        for i in range(len(paragraph_divs)):
            if i > 0:
                # 2 merupakan panjang karakter line break
                offset += len(paragraph_divs[i-1]) + 2
            self.add_paragraph_division(SipebiMiniParagraph(i+1, offset, paragraph_divs[i], len(paragraph_divs[i])))

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


class SipebiMiniParagraph:
    def __init__(self, index, offset, text, length):
        self.index = index
        self.offset = offset
        self.text = text
        self.length = length

        self.is_pre_char_occured = False

        self.word_divs: SipebiMiniWordDivision = []
        self.size = 0

    def add_word_division(self, word_division):
        self.word_divs.append(word_division)
        self.size += 1

    # create a method to split word by one space or more
    def tokenize_words(self):
        word_divs = self.text.split()
        # tokenize word by space and set the next and previous word division
        offset = 0
        for i in range(len(word_divs)):
            word_div = SipebiMiniWordDivision(original_string=word_divs[i])

            if i > 0:
                # 1 is the length of space character
                offset += len(word_divs[i-1]) + 1

                # setting next and previous word divisionrr
                word_div.prev_word_div = self.word_divs[self.size-1]
                word_div.prev_word_div.next_word_div = word_div

                # checking if a word only contains punctuation
                if not word_div.clean_word_string:
                    if word_div.has_post_word:
                        ori_string = word_div.prev_word_div.clean_post_word
                        new_word = word_div.pre_clean_word + ori_string + word_div.clean_post_word
                        offset -= 1
                        self.word_divs[self.size-1] = SipebiMiniWordDivision(element_no=self.size, original_string=new_word, offset=self.word_divs[self.size-1].position_offset)
                    else:
                        if i < len(word_divs) - 1:
                            offset -= 2
                            word_divs[i+1] = word_div.pre_clean_word + word_divs[i+1]
                    
                    continue
                

            word_div.position_offset = offset
            word_div.element_no = self.size + 1
            self.add_word_division(word_div)
        

    def __str__(self):
        return self.text
    
class SipebiMiniWordDivision:
    def __init__(self, element_no=-1, original_string='', offset=-1):
        self.original_string = original_string
        self.element_no = element_no
        self.position_offset = offset
        self.clean_word_string = original_string.strip()
        self.pre_word: SipebiMiniPreWordPunctuation = SipebiMiniPreWordPunctuation()
        self.post_word: SipebiMiniPostWordPunctuation = SipebiMiniPostWordPunctuation()

        self.is_handled = False
        
        self.next_word_div: SipebiMiniWordDivision = None
        self.prev_word_div: SipebiMiniWordDivision = None

        self.process_word()

    def _check_pre_word(self):
        self.pre_word = SipebiMiniPreWordPunctuation()
        for char in self.clean_word_string:
            if char in SipebiMiniPunctuationDivision.PRE_CHARS_OMITTED:
                self.pre_word.add_punctuation_division(char)
            else:
                break
        self.clean_word_string = self.clean_word_string[self.pre_word.length:]

    def _check_post_word(self):
        self.post_word = SipebiMiniPostWordPunctuation()
        for char in reversed(self.clean_word_string):
            if char in SipebiMiniPunctuationDivision.POST_CHARS_OMITTED:
                self.post_word.add_punctuation_division(char)
            else:
                break
        if self.post_word.length > 0:
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
    
    def start_with(self, character):
        return self.clean_word_string.startswith(character)

    @property
    def pre_clean_word(self):
        return self.pre_word.string_repr + self.clean_word_string

    @property
    def clean_post_word(self):
        return self.clean_word_string + self.post_word.string_repr
    
    def first_char_is(self, char_type):
        return self.clean_word_string and char_type(self.clean_word_string[0])

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
    def word_with_no_pre_word(self):
        return not self.pre_word.has_punctuation_div and bool(self.clean_word_string.strip())

    @property
    def is_null_or_empty(self):
        return not self.original_string

    def __str__(self):
        return self.original_string
    
class SipebiMiniPunctuationDivision:
    PRE_CHARS_OMITTED = {'(', '\'', '"', '[', '{', '-'}
    POST_CHARS_OMITTED = {
        '?', ',', '!', '.', ')', ':', '\'', '"', '}',
        ']', ';', '-'
    }

    def __init__(self):
        self.punctuation_div = []

    @property
    def string_repr(self):
        str = ""
        return str.join(self.punctuation_div)

    @property
    def length(self):
        return len(self.punctuation_div)

    def add_punctuation_division(self, char):
        self.punctuation_div.append(char)

    def punctuation_div_contains(self, char):
        for char in self.punctuation_div:
            if char in self.punctuation_div:
                return True
            
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


class SipebiMiniPreWordPunctuation(SipebiMiniPunctuationDivision):
    pass

class SipebiMiniPostWordPunctuation(SipebiMiniPunctuationDivision):
    # override method
    def add_punctuation_division(self, char):
        return self.punctuation_div.insert(0, char)

