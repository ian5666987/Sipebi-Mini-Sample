from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from core.PySipebiStructs import PySipebiTextDivision, PySipebiParagraphDivision, PySipebiWordDivision

class PySipebiDiagAturanTandaBacaHubungPadaUnsurBentukUlang(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']
    ERROR_CODE = '[TE02]'

    def setup(self):
        self.isReady = True
    
    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: PySipebiTextDivision = shared_resources['sipebi_text_division'] # konvensi penamaan: sipebi_text_division
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: PySipebiParagraphDivision = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: PySipebiWordDivision = word_div
                current = ''
                next = ''
                if (word.next_word_div != None):
                    current = word.original_string.lower()
                    next = word.next_word_div.original_string.lower()
                    # print(j, current, next)

                if (current in next) or (next in current):
                    if (not word.post_word.contains(".")):
                        # print("BENAR: ", j, current + "-" + next)
                        original_element = word.clean_word_string + " " + word.next_word_div.clean_word_string
                        corrected_element = word.clean_word_string + "-" + word.next_word_div.clean_word_string
                        # print(original_element)
                        # print(corrected_element)

                        self.add_diagnostics(word=word, paragraph=paragraph, error_code=self.ERROR_CODE, original_element=original_element, corrected_element=corrected_element)
                    

    def add_diagnostics(self, word: PySipebiWordDivision, paragraph: PySipebiParagraphDivision, error_code: str, original_element: str, corrected_element: str):
        hasilDiagnosis = PySipebiDiagnosticsError()
        hasilDiagnosis.ParagraphNo = paragraph.index
        hasilDiagnosis.ElementNo = word.element_no
        hasilDiagnosis.OriginalParagraphOffset = paragraph.offset
        hasilDiagnosis.PositionOffset = word.position_offset + word.pre_word.length
        hasilDiagnosis.CorrectedCharPosition = 0
        hasilDiagnosis.IsAmbiguous = False
        hasilDiagnosis.ErrorCode = error_code
        hasilDiagnosis.OriginalElement = original_element
        hasilDiagnosis.CorrectedElement = corrected_element
        self.diagList.append(hasilDiagnosis)

        return hasilDiagnosis

# Untuk test
text = "Kamu sedang apa? Jauh jauh, sana... Aku mau jalan. Jalan hidupku adalah menjadi ninja. Aku lagi mau makan makan sama Alek."
text = PySipebiTextDivision(text)

diag = PySipebiDiagAturanTandaBacaHubungPadaUnsurBentukUlang()

dict = {
    'sipebi_text_division': text
}

diag.execute_with_shared_resources(text, dict)
# for diag in diag.diagList:
#     print("DIAG")
#     print(diag.CorrectedElement)