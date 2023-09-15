from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from libs.SipebiMiniStructs import SipebiMiniText, SipebiMiniParagraph, SipebiMiniWordDivision

class PySipebiDiagAturanTandaBacaPadaDialog(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']

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

                if word.pre_word == '"': 
                    prev_word = word.prev_word_div
                    if prev_word and not prev_word.has_post_word:
                        hasilDiagnosis = PySipebiDiagnosticsError()
                        hasilDiagnosis.ParagraphNo = paragraph.index
                        hasilDiagnosis.ElementNo = prev_word.element_no
                        hasilDiagnosis.ErrorCode = 'TB07'
                        hasilDiagnosis.OriginalElement = prev_word.clean_word_string
                        hasilDiagnosis.CorrectedElement = prev_word.clean_word_string + ","
                        hasilDiagnosis.CorrectedCharPosition = 0
                        hasilDiagnosis.IsAmbiguous = False
                        hasilDiagnosis.OriginalParagraphOffset = paragraph.offset
                        hasilDiagnosis.PositionOffset = prev_word.position_offset
                        self.diagList.append(hasilDiagnosis)

                if word.check_post_word_is_double_quote:
                    if word.post_word in SipebiMiniWordDivision.POST_CHARS_OMITTED and word.next_word_div:
                        hasilDiagnosis = PySipebiDiagnosticsError()
                        hasilDiagnosis.ParagraphNo = paragraph.index
                        hasilDiagnosis.ElementNo = word.element_no
                        hasilDiagnosis.ErrorCode = 'TB07'
                        hasilDiagnosis.OriginalElement = word.clean_word_string
                        hasilDiagnosis.CorrectedElement = word.clean_word_string + ","
                        hasilDiagnosis.CorrectedCharPosition = 0
                        hasilDiagnosis.IsAmbiguous = False
                        hasilDiagnosis.OriginalParagraphOffset = paragraph.offset
                        hasilDiagnosis.PositionOffset = word.position_offset
                        self.diagList.append(hasilDiagnosis)

        self.isCompleted = True

# text = 'aku mau "aku mau" katanya'
# text = SipebiMiniText(text)

# diag = PySipebiDiagAturanTandaBacaPadaDialog()

# dict = {
#     'sipebi_text_division': text
# }

# diag.execute_with_shared_resources(text, dict)

