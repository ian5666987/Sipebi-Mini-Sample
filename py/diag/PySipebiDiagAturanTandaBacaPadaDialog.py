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
                if word.check_post_word_is_double_quote:
                    if word.post_word in SipebiMiniWordDivision.POST_CHARS_OMITTED:
                        hasilDiagnosis = PySipebiDiagnosticsError()
                        hasilDiagnosis.ParagraphNo = i
                        hasilDiagnosis.ElementNo = j
                        hasilDiagnosis.ErrorCode = 'TB07'
                        hasilDiagnosis.OriginalElement = word.original_string
                        if j < len(paragraph.word_divs) - 1:
                            hasilDiagnosis.CorrectedElement = word.original_string[:-1] + "," + word.post_word
                        hasilDiagnosis.CorrectedElement = word.original_string[:-1] + "," + word.post_word
                        hasilDiagnosis.CorrectedCharPosition = word.position_offset + len(word.original_string) - 1
                        hasilDiagnosis.IsAmbiguous = False
                        hasilDiagnosis.PositionOffset = word.position_offset
                        self.diagList.append(hasilDiagnosis)

        self.isCompleted = True
        return self.diagList