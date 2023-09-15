
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
                    # previous_word = word_div.prev_word_div
                    # previous_word.reconstruct_string(new_clean_word=previous_word.clean_post_word, 
                    #                                 new_pre_word=word_div.pre_clean_word, 
                    #                                 new_post_word=word_div.clean_post_word)

                    # checking if punctuation is PRE_CHARS_OMITTED or POST_CHARS_OMITTED
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
    PRE_CHARS_OMITTED = {'(', '\'', '"', '[', '{', '-'}
    POST_CHARS_OMITTED = {
        '?', ',', '!', '.', ')', ':', '-', '\'', '"', '}',
        ']', ';'
    }
    def __init__(self, element_no=-1, original_string='', offset=-1):
        self.original_string = original_string
        self.element_no = element_no
        self.position_offset = offset
        self.clean_word_string = original_string.strip()
        self.pre_word = ""
        self.post_word = ""
        self.word_position_in_sentence = None

        self.is_handled = False
        
        self.next_word_div: SipebiMiniWordDivision = None
        self.prev_word_div: SipebiMiniWordDivision = None

        self.double_quote_error = False # attribute specific to flagging double quote error 

        self.process_word()

    def check_pre_word(self):
        first_char = self.clean_word_string[0]
        if first_char in self.PRE_CHARS_OMITTED:
            self.pre_word = first_char
            self.clean_word_string = self.clean_word_string[1:]

    def check_post_word(self):
        if not self.clean_word_string:
            return
        last_char = self.clean_word_string[-1]
        if last_char in self.POST_CHARS_OMITTED:
            # checking if last char is a double quote
            if last_char == '"':
                if (self.clean_word_string[-2] in self.POST_CHARS_OMITTED):
                    self.post_word = self.clean_word_string[-2] + last_char
                    self.clean_word_string = self.clean_word_string[:-2]
                else:
                    self.double_quote_error = True
                    self.post_word = last_char
                    self.clean_word_string = self.clean_word_string[:-1]
            else:
                self.post_word = last_char
                self.clean_word_string = self.clean_word_string[:-1]

    def process_word(self):
        self.check_pre_word()
        self.check_post_word()

    @property
    def check_post_word_is_double_quote(self):
        if self.post_word:
            return self.post_word[-1] == '"'
        return False
    
    @property   
    def check_post_word_is_double_quote_without_error(self):
        return self.check_post_word_is_double_quote and not self.double_quote_error

    @property
    def has_pre_word(self):
        return bool(self.pre_word.strip())

    @property
    def has_post_word(self):
        return bool(self.post_word.strip())
    
    def ended_with(self, character):
        return self.clean_word_string.endswith(character)
    
    def start_with(self, character):
        return self.clean_word_string.startswith(character)

    @property
    def ended_with_dot(self):
        return self.ended_with(".")

    @property
    def ended_with_comma(self):
        return self.ended_with(",")

    @property
    def ended_with_question_mark(self):
        return self.ended_with("?")

    @property
    def ended_with_exclamation(self):
        return self.ended_with("!")

    @property
    def pre_clean_word(self):
        return self.pre_word + self.clean_word_string

    @property
    def clean_post_word(self):
        return self.clean_word_string + self.post_word
    
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
        return not self.clean_word_string and bool(self.post_word.strip())

    @property
    def word_with_no_pre_word(self):
        return not self.pre_word.strip() and bool(self.clean_word_string.strip())

    @property
    def is_null_or_empty(self):
        return not self.original_string

    def reconstruct_string(self, new_clean_word, new_pre_word=None, new_post_word=None):
        self.clean_word_string = new_clean_word
        self.pre_word = new_pre_word or self.pre_word
        self.post_word = new_post_word or self.post_word
        self.original_string = self.pre_word + new_clean_word + self.post_word

    def space_combine(self, another_word_div):
        return self.original_string + " " + another_word_div.original_string

    @staticmethod
    def space_combine_list(other_word_divs):
        return " ".join([x.original_string for x in other_word_divs if x])

    def pre_post_combine(self, mid_string, another_word_div):
        return self.pre_clean_word + mid_string + another_word_div.clean_post_word

    def pre_post_combine_without_mid(self, another_word_div):
        return self.pre_clean_word + another_word_div.clean_post_word

    def __str__(self):
        return self.original_string