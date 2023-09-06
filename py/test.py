from core.sipebi_struct import *


teks = "kamu jelek sekali Bang! (dia menengok ke arahku). HAHAH. \n\nAku juga tidak tau bahwa dia adalah orang itu?? Begitulah ges yak."

sipebi_teks = SipebiMiniText(teks)
sipebi_teks.process_text()

for paragraph_div in sipebi_teks.paragraph_divs:
    print(paragraph_div)
    for sentence_div in paragraph_div.sentence_divs:
        sentence: SipebiMiniSentence = sentence_div
        print(sentence)
        for word_div in sentence_div.word_divs:
            word: SipebiMiniWordDivision = word_div
            print(word.first_char_is_capitalized)
