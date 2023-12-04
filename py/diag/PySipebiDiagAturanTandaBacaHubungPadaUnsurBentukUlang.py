from core.PySipebiDiagnosticsBase import PySipebiDiagnosticsBase
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError
from libs.SipebiMiniStructs import SipebiMiniText, SipebiMiniParagraph, SipebiMiniWordDivision

import os
direktori_script = os.path.dirname(os.path.abspath(__file__))
nama_file_txt = 'contoh-data-kata-dasar.txt'  
absolute_path_txt = os.path.join(direktori_script, 'data', nama_file_txt)

class PySipebiDiagAturanTandaBacaHubungPadaUnsurBentukUlang(PySipebiDiagnosticsBase):
    hasSharedResources = True
    sharedResourcesInputKeys = ['sipebi_text_division']
    
    def setup(self):
        self.isReady = True

    def execute_with_shared_resources(self, text, shared_resources):
        sipebi_text: SipebiMiniText = shared_resources['sipebi_text_division']
        kata_dasar = []
        with open(absolute_path_txt, 'r', encoding='utf-8') as file:
            for line in file:
                kata = line.strip()
                kata_dasar.append(kata)

        # iterasi untuk setiap paragraf
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: SipebiMiniParagraph = paragraph_div
            #print(i, paragraph)
            # iterasi untuk tokenisasi tiap kata di paragraf
            for j, word_div in enumerate(paragraph.word_divs):
                word: SipebiMiniWordDivision = word_div
                print(j, word)
                next_word = str(word.next_word_div).lower()
                word_str = str(word).lower()

                if (word_str in next_word) or (next_word in word_str):
                    print(word_str, next_word)
                    hasilDiagnosis = PySipebiDiagnosticsError()
                    hasilDiagnosis.ErrorCode = 'TE02'
                    hasilDiagnosis.paragraphNo = i
                    hasilDiagnosis.ElementNo = j
                    hasilDiagnosis.OriginalElement = word
                    hasilDiagnosis.CorrectedElement = next_word + "-" + word_str
                    hasilDiagnosis.OriginalParagraphOffset = paragraph.offset
                    hasilDiagnosis.PositionOffset = word.position_offset

                    hasilDiagnosis.IsAmbiguous = False
                    self.diagList.append(hasilDiagnosis)

        self.isCompleted = True
        return self.diagList

text = "Kamu sedang apa? Jauh jauh, sana. Aku lagi mau makan makan sama Alek"
text = SipebiMiniText(text)

diag = PySipebiDiagAturanTandaBacaHubungPadaUnsurBentukUlang()

dict = {
    'sipebi_text_division': text
}

diag.execute_with_shared_resources(text, dict)