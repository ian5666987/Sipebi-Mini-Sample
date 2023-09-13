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
        self.empty_diagnostics_and_reinit()

        sipebi_text: SipebiMiniText = shared_resources['sipebi_text_division']
        char_sum_pos = 0
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: SipebiMiniParagraph = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: SipebiMiniWordDivision = word_div
                if word.check_post_word_is_double_quote:
                    if word.post_word in SipebiMiniWordDivision.POST_CHARS_OMITTED:
                        char_sum_pos += len(word.original_string)
                        hasilDiagnosis = PySipebiDiagnosticsError()
                        hasilDiagnosis.ParagraphNo = i + 1
                        hasilDiagnosis.ElementNo = j + 1
                        hasilDiagnosis.ErrorCode = 'TB07'
                        hasilDiagnosis.OriginalElement = word.clean_word_string
                        hasilDiagnosis.CorrectedElement = word.original_string[:-1] + ","
                        hasilDiagnosis.CorrectedCharPosition = 0
                        hasilDiagnosis.IsAmbiguous = False
                        hasilDiagnosis.OriginalParagraphOffset = char_sum_pos - len(word.original_string)
                        hasilDiagnosis.PositionOffset = word.position_offset
                        self.diagList.append(hasilDiagnosis)

        self.isCompleted = True

text = '"Aku ingin pergi ke pasar" kata dia.'

sipebi_text = SipebiMiniText(text)
dict = {
    'sipebi_text_division': sipebi_text
}

diagnosis = PySipebiDiagAturanTandaBacaPadaDialog()
diagnosis.setup()
diagnosis.execute_with_shared_resources(text, dict)

for diag in diagnosis.diagList:
    print(diag.OriginalElement, diag.CorrectedElement, diag.CorrectedCharPosition, diag.ErrorCode)
    print(diag.OriginalParagraphOffset, diag.PositionOffset, diag.ParagraphNo, diag.ElementNo, diag.IsAmbiguous)