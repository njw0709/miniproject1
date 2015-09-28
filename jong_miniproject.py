import codecs
from pattern.web import *
from pattern.vector import *
from pattern.graph import *

## saves all harry potter url. Returns dictionary with title as key and the latter part of url as items
def save_url(pages):
	i = 1
	listurl = {}
	while i <= pages:
		Potter_Fan_fic = URL("https://www.fanfiction.net/book/Harry-Potter/?&srt=1&r=103&p="+str(i)).download()
		s ="class=stitle href=\"" 
		url = Potter_Fan_fic.split(s)
		url = url[1:]
		for j in range(len(url)):
			url[j]=url[j].split("\"")[0]
			title = url[j].split("/")[-1]
			if title in listurl.iteritems():
				if listurl[title] == url[j]:
					pass
				else:
					listurl[title].append(url[j])

			else:
				listurl[title]=url[j].split("/1/")
		i = i+1
	return listurl

## saves all the chapters of each fan fiction from url dictionary. Returns 
def save_text(urldict,chaptnum):
	fanfic_text={}
	errorstr1 = "<div class=panel_normal ><span class='gui_normal'>FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found. Please check to see you are not using an outdated url.<p>New chapter/story can take up to 15 minutes to show up.</span></div>"
	errorstr2 = "Story Not Found"
	for title,url in urldict.iteritems():
		chapter = 1
		while True and chapter <= chaptnum:
				s = URL("https://www.fanfiction.net"+url[0]+"/"+str(chapter)+"/"+url[1],"utf-8").download()
				if errorstr1 in s or errorstr2 in s:
					print "end of the book"
					break
				else:
					ptext = plaintext(s).encode('ascii','ignore')
					ptext = save_necessary(ptext)
					try:
						fanfic_text[title] = fanfic_text[title]+ptext
						print "adding next chapter"
					except KeyError:
						fanfic_text[title]=ptext
						print "new book"
					chapter=chapter+1
	return fanfic_text

## prints either list or dictionary of fanfictions in readable format
def print_text(fanfic_dic):
	while True:
		try:	
			for title in fanfic_dic:
				textline = fanfic_dic[title].split("\n\n")
				textline = delete_empty_list(textline)				
				for i in range(len(textline)):
					print textline[i]
			break
		except TypeError:
			for i in range(len(fanfic_dic)):
				textline = fanfic_dic[i].split("\n\n")
				textline = delete_empty_list(textline)
				for j in range(len(textline)):
					print textline[j]
			break

## deletes blank line from list of textlines
def delete_empty_list(textline):
	print len(textline)
	for i in range(len(textline)):
		blank_instance = 0
		if textline[i]=='':
			blank_instance=blank_instance+1
		else:
			pass

	print "blank:", blank_instance
	for i in range(blank_instance+1):
		try:
			textline.remove('')
		except ValueError:
			pass

	return textline

## deletes unnecessary parts of the fanfiction (the first part ends with "Next >" and the ending part starts with "1. Chapter 1")
## returns String
def save_necessary(text):
	try:
		beginningstring = "\nBooksHarry Potter\n"
		endingstring = "\n\nFavorite"
		res = text.split(beginningstring)
		res = res[1].split(endingstring)
		return res[0]
	except IndexError:
		print text

## Takes dictionary {title:text} and returns word count dictionary (nested) {title: {'word':#ofwordsintext...}...}
def count_word(text_dict):
	word_count_dict = {}
	for title,text in text_dict.iteritems():
		word_count_dict[title] = count(words(text))
	return word_count_dict

##Takes dictionary {title:text} of fanfiction and returns instances of Document Class (from pattern) stored
## in dictionary {title:Document_instance}. Document class has attributes such as word count, stem, language, vector etc.
def convert2doc(text_dict):
	doc_list = []
	i=1
	for title,text in text_dict.iteritems():
		d = Document(text,name=title,type="HarryPotterFanF",language="en",id = i)
		doc_list.append(d)
		print d.name
		i=i+1
	return doc_list

##Create Hierarchy of books
def create_cluster(doc_list):
	model = Model(doc_list)
	cluster = model.cluster(method=KMEANS, k=10, iterations= 10, distance=COSINE, seed=RANDOM, p=0.8)
	return cluster

# takes cluster and draws graph. exports to 'graph' file
def make_graph(cluster):
	g=Graph(layout = SPRING, distance = 5.0)
	c = []
	for i in range(len(cluster)):
		g.add_node(str(i))
		m = Model(cluster[i])
		v=centroid(vectors=m.vectors)
		c.append(v)
		for docs in cluster[i]:
			g.add_node(docs.name)
			g.add_edge(docs.name,str(i))

	for i in range(len(cluster)):
		if i ==len(cluster)-1:
			g.add_edge(str(i),str(0))
		else:
			g.add_edge(str(i),str(i+1))

	layout = GraphLayout(g)
	g.export('graph',directed=False)