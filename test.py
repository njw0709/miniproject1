from pattern.web import *
from jong_miniproject import*
s = URL("https://www.fanfiction.net/s/11235451/1/Bitten").download()
s = plaintext(s)
s = save_necessary(s)
print_text(s)

# book_dict = save_text(save_url(1))
# print_text(book_dict)
