from core.PySipebiAnalyzerBase import PySipebiAnalyzerBase
from core.sipebi_struct import SipebiMiniText, SipebiMiniParagraph, SipebiMiniWordDivision
from core.PySipebiDiagnosticsError import PySipebiDiagnosticsError

class PyTandaKomaPadaAkhirDialog(PySipebiAnalyzerBase):
    def setup(self):
        self.isReady = True
        return super().setup()
    
    def execute(self, text):
        sipebi_text: SipebiMiniText = SipebiMiniText(text)
    
        for i, paragraph_div in enumerate(sipebi_text.paragraph_divs):
            paragraph: SipebiMiniParagraph = paragraph_div
            for j, word_div in enumerate(paragraph.word_divs):
                word: SipebiMiniWordDivision = word_div
                if word.check_post_word_is_double_quote:
                    if word[-2] == '.' or word[-2] == '?' or word[-2] == '!' or word[-2] == ',':
                        hasilDiagnosis = PySipebiDiagnosticsError()
                        hasilDiagnosis.ErrorCode = 'TB07'
                        hasilDiagnosis.OriginalElement = word
                        hasilDiagnosis.CorrectedElement = word[:-2] + ',' + word[-1]
                        hasilDiagnosis.IsAmbiguous = False
                        self.diagList.append(hasilDiagnosis)
                

        return super().execute(text)
    
sample_text = 'Dia mengatakan "Aku tidak tahu apa yang harus aku lakukan" katanya. Namun, dia berkata "Boleh saja!" dan pergi.'

sample_instance = PyTandaKomaPadaAkhirDialog()
sample_instance.setup()
sample_instance.execute(sample_text)

print(sample_instance.diagList)