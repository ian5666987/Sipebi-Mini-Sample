from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from core.PySipebiStructs import PySipebiTextDivision, PySipebiParagraphDivision, PySipebiWordDivision, PySipebiNumericDivision

class PySipebiDiagAturanAngkaBilanganBesar(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']
    ERROR_CODE_1 = '[KG05]'

    def setup(self):
        self.isReady = True

    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: PySipebiTextDivision = shared_resources['sipebi_text_division'] # konvensi penamaan: sipebi_text_division
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: PySipebiParagraphDivision = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: PySipebiWordDivision = word_div

                # TODO: implementasi aturan angka bilangan besar
                if not isinstance(word, PySipebiNumericDivision):
                    continue
                dot_index = word.clean_word_string.find('.')
                if dot_index != -1:
                    if word.greater_than(9999):
                        dot_index = word.clean_word_string.find('.')
                        count_dot = word.clean_word_string.count('.')
                        string_repr = ""
                        if count_dot == 1:
                            string_repr = "ribu"
                        elif count_dot == 2:
                            string_repr = "juta"
                        elif count_dot == 3:
                            string_repr = "miliar"
                        elif count_dot == 4:
                            string_repr = "triliun"
                        
                        original_element = word.clean_word_string
                        corrected_element = word.clean_word_string[:dot_index] + " " + string_repr
                        self.add_diagnostics(word=word, paragraph=paragraph, error_code=self.ERROR_CODE_1
                                                            , original_element=original_element, corrected_element=corrected_element)

        self.isCompleted = True

    # add_diagnostics: fungsi untuk menambahkan kesalahan ke dalam daftar kesalahan
	# fungsi ini harus dipanggil setiap kali sebuah kesalahan ditemukan
	# word: kata awal yang yang mengandung kesalahan
	# paragraph: paragraf yang mengandung kesalahan
	# error_code: kode kesalahan
	# original_element: elemen yang salah
	# corrected_element: elemen yang benar
    def add_diagnostics(self, word: PySipebiWordDivision, paragraph: PySipebiParagraphDivision, error_code: str
                        , original_element: str, corrected_element: str):
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
    
# text = "Dia berhasil mengumpulkan donasi 11.000 rupiah biaya sekolah anak-anak kurang mampu di desanya."

# test = PySipebiTextDivision(text)

# shared_resources = {
#     'sipebi_text_division': test
# }

# test2 = PySipebiAturanAngkaBilanganBesar()
# test2.execute_with_shared_resources(text, shared_resources)

# for diag in test2.diagList:
#     print("ElementNo: ", diag.ElementNo)
#     print(diag.OriginalElement, diag.CorrectedElement)