from .core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from .core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from .core.PySipebiStructs import PySipebiTextDivision, PySipebiParagraphDivision, PySipebiWordDivision

class PySipebiDiagAturanPartikelLahKahTah(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']
    ERROR_CODE_1 = '[KE01]'

    def setup(self):
        self.isReady = True

    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: PySipebiTextDivision = shared_resources['sipebi_text_division'] # konvensi penamaan: sipebi_text_division
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: PySipebiParagraphDivision = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: PySipebiWordDivision = word_div

                # TODO: implementasi aturan partikel lah, kah, tah
                next_word = word.next_word_div
                # jika kata berikutnya adalah partikel lah, kah, atau tah, misal: apa kah
                # maka gabungkan kata tersebut menjadi: apakah
                if next_word and (next_word.pre_clean_word == "lah" 
                                or next_word.pre_clean_word == "kah" 
                                or next_word.pre_clean_word == "tah"):
                    original_element = word.clean_word_string + " " + next_word.pre_clean_word
                    corrected_element = word.clean_word_string + next_word.pre_clean_word
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