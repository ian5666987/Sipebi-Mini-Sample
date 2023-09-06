
class SipebiMiniText:
    def __init__(self, text=''):
        self.text = text
        self.length = len(text)

        self.paragraph_divs: SipebiMiniParagraph = []

    def add_paragraph_division(self, paragraph_division):
        self.paragraph_divs.append(paragraph_division)

    def separate_paragraph_by_line_break(self):
        paragraph_divs = self.text.split("\n\n")
        for i, paragraph_div in enumerate(paragraph_divs):
            self.add_paragraph_division(SipebiMiniParagraph(i, 0, paragraph_div, len(paragraph_div)))

    def process_paragraph_divisions(self):
        for paragraph_div in self.paragraph_divs:
            paragraph_div.separate_sentence_by_punctuation() # tokenisasi kalimat
            for sentence_div in paragraph_div.sentence_divs:
                sentence_div.separate_word_by_space() # tokenisasi kata

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

        self.sentence_divs: SipebiMiniSentence = []

    def add_sentence_division(self, sentence_division):
        self.sentence_divs.append(sentence_division)

    def separate_sentence_by_punctuation(self):
        sentence_divs = self.text.split(".")
        for i, sentence_div in enumerate(sentence_divs):
            self.add_sentence_division(SipebiMiniSentence(i, 0, sentence_div + ".", len(sentence_div)))

    def __str__(self):
        return self.text

class SipebiMiniSentence:
    def __init__(self, index, offset, text, length):
        self.index = index
        self.offset = offset
        self.text = text
        self.length = length

        self.word_divs: SipebiMiniWordDivision = []

    def add_word_division(self, word_division):
        self.word_divs.append(word_division)

    # create a method to split word by space
    def separate_word_by_space(self):
        word_divs = self.text.split(" ")
        for i, word_div in enumerate(word_divs):
            self.add_word_division(SipebiMiniWordDivision(word_div))
    
    def __str__(self):
        return self.text

class SipebiMiniWordDivision:
    def __init__(self, original_string):
        self.original_string = original_string
        self.clean_word_string = original_string.strip()
        self.pre_word = ""
        self.post_word = ""
        self.word_position_in_sentence = None
        self.position_offset = 0
        self.element_no = -1
        self.is_handled = False

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