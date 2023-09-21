from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from libs.SipebiMiniStructs import SipebiMiniText, SipebiMiniParagraph, SipebiMiniWordDivision, SipebiMiniPreWordPunctuation, SipebiMiniPostWordPunctuation

class PySipebiDiagAturanTandaBacaPadaDialog(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']
    ERROR_CODE_1 = 'TB07'
    ERROR_CODE_2 = 'TB08'

    def setup(self):
        self.isReady = True

    def create_shared_resources(self, text, input_resources):
        output_resources = {}
        sipebi_text_division = SipebiMiniText(text)
        output_resources['sipebi_text_division'] = sipebi_text_division
        return output_resources

    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: SipebiMiniText = shared_resources['sipebi_text_division']
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: SipebiMiniParagraph = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: SipebiMiniWordDivision = word_div

                pre_word: SipebiMiniPreWordPunctuation = word.pre_word
                post_word: SipebiMiniPostWordPunctuation = word.post_word

                if pre_word.contains('"'):
                    prev_word = word.prev_word_div
                    if prev_word and not prev_word.has_post_word:
                        hasilDiagnosis = self.add_diagnostics(prev_word, paragraph, self.ERROR_CODE_1)
                        hasilDiagnosis.OriginalElement = prev_word.clean_word_string
                        hasilDiagnosis.CorrectedElement = prev_word.clean_word_string + ","

                if post_word.contains('"'):
                    if not post_word.ended_with('"'):
                        if not post_word.start_with('"'):
                            hasilDiagnosis = self.add_diagnostics(word, paragraph, self.ERROR_CODE_2)
                            hasilDiagnosis.OriginalElement = word.clean_post_word
                            hasilDiagnosis.CorrectedElement = word.clean_post_word[:-1]
                        else:
                            hasilDiagnosis = self.add_diagnostics(word, paragraph, self.ERROR_CODE_1)
                            hasilDiagnosis.OriginalElement = word.clean_post_word
                            hasilDiagnosis.CorrectedElement = word.clean_word_string + post_word.last_punctuation + post_word.first_punctuation
                    else:
                        if post_word.start_with('"'):
                            hasilDiagnosis = self.add_diagnostics(word, paragraph, self.ERROR_CODE_1)
                            hasilDiagnosis.OriginalElement = word.clean_word_string
                            hasilDiagnosis.CorrectedElement = word.clean_word_string + ','
                        elif not post_word.start_with(',') and post_word.contains(','):
                            hasilDiagnosis = self.add_diagnostics(word, paragraph, self.ERROR_CODE_2)
                            hasilDiagnosis.OriginalElement = word.clean_word_string + post_word.first_punctuation + ','
                            hasilDiagnosis.CorrectedElement = word.clean_word_string + post_word.first_punctuation
        self.isCompleted = True

    def add_diagnostics(self, word: SipebiMiniWordDivision, paragraph: SipebiMiniParagraph, error_code: str):
        hasilDiagnosis = PySipebiDiagnosticsError()
        hasilDiagnosis.ParagraphNo = paragraph.index
        hasilDiagnosis.ElementNo = word.element_no
        hasilDiagnosis.OriginalParagraphOffset = paragraph.offset
        hasilDiagnosis.PositionOffset = word.position_offset
        hasilDiagnosis.CorrectedCharPosition = 0
        hasilDiagnosis.IsAmbiguous = False
        hasilDiagnosis.ErrorCode = error_code
        self.diagList.append(hasilDiagnosis)

        return hasilDiagnosis



# text = 'aku mau "hei bodoh!," kataku'
# text = SipebiMiniText(text)

# diag = PySipebiDiagAturanTandaBacaPadaDialog()

# dict = {
#     'sipebi_text_division': text
# }

# diag.execute_with_shared_resources(text, dict)

