from .core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from .core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from .core.PySipebiStructs import PySipebiTextDivision, PySipebiParagraphDivision, PySipebiWordDivision, PySipebiPreWordPunctuation, PySipebiPostWordPunctuation

class PySipebiDiagAturanTandaBacaPadaDialog(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesOutputKeys = ['sipebi_text_division']
    
    ERROR_CODE_1 = '[TB07]'
    ERROR_CODE_2 = '[TB08]'

    def setup(self):
        self.isReady = True

    def create_shared_resources(self, text, input_resources):
        output_resources = {}
        sipebi_text_division = PySipebiTextDivision(text)
        output_resources['sipebi_text_division'] = sipebi_text_division
        return output_resources

    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: PySipebiTextDivision = shared_resources['sipebi_text_division'] # konvensi penamaan: sipebi_text_division
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: PySipebiParagraphDivision = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: PySipebiWordDivision = word_div

                pre_word: PySipebiPreWordPunctuation = word.pre_word
                post_word: PySipebiPostWordPunctuation = word.post_word

                # jika tanda baca kutip dua (") terdapat di awal kata
                if pre_word.contains('"'):
                    prev_word = word.prev_word_div
                    # jika terdapat kata sebelumnya dan kata tersebut tidak memiliki tanda baca di akhir kata, misal : kamu "aku
                    # maka tambahkan tanda baca koma (,) di akhir kata sebelumnya sebelum tanda baca kutip dua (") menjadi: kamu, "aku
                    if prev_word and not prev_word.has_post_word: 
                        original_element = prev_word.clean_word_string
                        corrected_element = prev_word.clean_word_string + ','
                        self.add_diagnostics(word=prev_word, paragraph=paragraph, error_code=self.ERROR_CODE_1
                                            , original_element=original_element, corrected_element=corrected_element)

                # jika tanda baca kutip dua (") terdapat di akhir kata
                if post_word.contains('"'):
                    # jika ada tanda baca lain setelah kutip dua (")
                    if not post_word.ended_with('"'):
                        original_element = word.clean_post_word
                        # jika tanda baca kutip dua (") berada di tengah tengah tanda baca lain, misal : aku!",
                        # maka hapus tanda baca setelah tanda baca kutip dua (") menjadi: aku!""
                        if not post_word.start_with('"'):  
                            corrected_element = word.clean_word_string + post_word.string_repr[:post_word.string_repr.index('"') + 1]
                        # jika tanda baca kutip dua (") berada di awal tanda baca lain, misal: aku".
                        # maka pindahkan tanda baca setelah tanda baca kutip dua (") ke sebelum tanda baca petik dua (") menjadi: aku."
                        else:
                            corrected_element = word.clean_word_string + post_word.last_punctuation + post_word.first_punctuation
                            
                        self.add_diagnostics(word=word, paragraph=paragraph, error_code=self.ERROR_CODE_1
                                            , original_element=original_element, corrected_element=corrected_element)
                    # jika tidak ada tanda baca lain setelah kutip dua (")
                    else:
                        # jika hanya ada tanda baca kutip dua ("), misal: aku"
                        # maka tambahkan tanda baca koma (,) sebelum tanda kutip dua (") menjadi : aku,"
                        if post_word.start_with('"'):
                            original_element = word.clean_word_string
                            corrected_element = word.clean_word_string + ','
                            self.add_diagnostics(word=word, paragraph=paragraph, error_code=self.ERROR_CODE_1
                                            , original_element=original_element, corrected_element=corrected_element)
                        # jika terdapat tanda baca koma (,) pada tengah - tengah tanda baca lain, misal: aku!,"
                        # maka hapus tanda baca koma (,) menjadi: aku!"
                        elif not post_word.start_with(',') and post_word.contains(','):
                            original_element = word.clean_word_string + post_word.first_punctuation + ','
                            corrected_element = word.clean_word_string + post_word.first_punctuation
                            self.add_diagnostics(word=word, paragraph=paragraph, error_code=self.ERROR_CODE_2
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


# text = 'alo aku disini "menang"'
# text = PySipebiTextDivision(text)

# diag = PySipebiDiagAturanTandaBacaPadaDialog()

# dict = {
#     'sipebi_text_division': text
# }
# diag.execute_with_shared_resources(text, dict)

# for diag in diag.diagList:
#     print(diag.OriginalElement)
#     print(diag.CorrectedElement)

