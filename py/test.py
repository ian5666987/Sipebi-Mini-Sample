from core.sipebi_struct import *


teks = "kamu jelek sekali Bang! (dia menengok ke arahku). HAHAH. \n\nAku juga tidak tau bahwa dia adalah orang itu?? Begitulah ges yak."

sipebi_teks = SipebiMiniText(teks)

for paragraph_div in sipebi_teks.paragraph_divs:
    print(paragraph_div)
    for word_div in paragraph_div.word_divs:
        word: SipebiMiniWordDivision = word_div
        print(word)

# word = 'Tes."'

# sipebi_word: SipebiMiniWordDivision = SipebiMiniWordDivision(word)

# print(sipebi_word.check_post_word_is_double_quote_without_error)