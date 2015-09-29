from pattern.web import *
from jong_miniproject import*
book_dict = save_text(save_url(1),11)
print_text(book_dict)
a = convert2doc(book_dict)
cluster = create_cluster(a)
make_graph(cluster)
