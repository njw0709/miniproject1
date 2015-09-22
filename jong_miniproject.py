import codecs
from pattern.web import *

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
def save_text(urldict):
	fanfic_text={}
	errorstr = "<div class=panel_normal ><span class='gui_normal'>FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found. Please check to see you are not using an outdated url.<p>New chapter/story can take up to 15 minutes to show up.</span></div>"
	for title,url in urldict.iteritems():
		chapter = 1
		endofchapter=False
		while True and chapter <= 1:
				s = URL("https://www.fanfiction.net"+url[0]+"/"+str(chapter)+"/"+url[1],"utf-8").download()
				if errorstr in s:
					print "end of the book"
					break
				else:
					ptext = plaintext(s)
					ptext = save_necessary(ptext)
					while True:
						try:
							fanfic_text[title]+ptext
							print "adding next chapter"
							break
						except KeyError:
							fanfic_text[title]=ptext
							print "new book"
							break
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
					print repr(textline[i])
			break
		except TypeError:
			for i in range(len(fanfic_dic)):
				textline = fanfic_dic[i].split("\n\n")
				textline = delete_empty_list(textline)
				for j in range(len(textline)):
					print repr(textline[j])
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
		textline.remove('')
	return textline

## deletes unnecessary parts of the fanfiction (the first part ends with "Next >" and the ending part starts with "1. Chapter 1")
## returns String
def save_necessary(text):
	res=text.split("Next >")
	res = res[1:]
	s = res[0].split("1. Chapter 1")
	res = s[:-1]
	return res

# s = URL("https://www.fanfiction.net/s/11235451/1/Bitten").download()
# s = plaintext(s)
# print type(s)
# print repr(s)
# a = s.split("\n")
# for i in range(len(a)):
# 	print a[i]
# 	print type(a[i])