
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
        paragraph_divs = self.text.split("\n\n")
        for i, paragraph_div in enumerate(paragraph_divs):
            self.add_paragraph_division(SipebiMiniParagraph(i, 0, paragraph_div, len(paragraph_div)))

    # method untuk memproses setiap paragraph division dan memisahkan kata-kata di dalamnya
    def process_paragraph_divisions(self):
        for paragraph_div in self.paragraph_divs:
            paragraph_div.tokenize_words() # tokenisasi kata

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
        # untuk sementara tidak pake sentence division dulu karena belum ada pengecekan untuk menentukan suatu kalimat itu berakhir atau tidak
        # self.sentence_divs: SipebiMiniSentence = [] 

        self.word_divs: SipebiMiniWordDivision = []

    def add_word_division(self, word_division):
        self.word_divs.append(word_division)

    # create a method to split word by one space or more
    def tokenize_words(self):
        word_divs = self.text.split()
        for i, word_div in enumerate(word_divs):
            self.add_word_division(SipebiMiniWordDivision(word_div))

    def __str__(self):
        return self.text

class SipebiMiniWordDivision:
    PRE_CHARS_OMITTED = {'(', '\'', '"', '[', '{', '-'}
    POST_CHARS_OMITTED = {
        '?', ',', '!', '.', ')', ':', '-', '\'', '"', '}',
        ']', ';'
    }
    def __init__(self, original_string):
        self.original_string = original_string
        self.clean_word_string = original_string.strip()
        self.pre_word = ""
        self.post_word = ""
        self.word_position_in_sentence = None
        self.position_offset = 0
        self.element_no = -1
        self.is_handled = False
        self.next_word_div = None

        self.double_quote_error = False # attribute specific to flagging double quote error 

        self.process_word()
    
    def set_next_word(self, word_div):
        self.next_word_div = word_div

    def check_pre_word(self):
        first_char = self.clean_word_string[0]
        if first_char in self.PRE_CHARS_OMITTED:
            self.pre_word = first_char
            self.clean_word_string = self.clean_word_string[1:]

    def check_post_word(self):
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
        new_pre_word = new_pre_word or self.pre_word
        new_post_word = new_post_word or self.post_word
        return new_pre_word + new_clean_word + new_post_word

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