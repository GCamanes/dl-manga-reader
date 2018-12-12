## IMPORT
import os, sys
import argparse

## WEBSITE URLS
URL_WEBSITE = "https://www.mangareader.net"
URL_MANGAS_LIST = "/alphabetical"

## CONSTANT VARIABLES
PATH = "."
DICO_MANGAS = {}

# Function to get the complete name of a chapter
# Format : [nameOfManga]_[chap num on 4 digit]
# Used in : chap repository and img file
def getChapName(manga, chap):
	chapName = ""
	if (len(chap.split(".")[0]) == 1):
		chapName = manga+"_chap000"+chap
	elif (len(chap.split(".")[0]) == 2):
		chapName = manga+"_chap00"+chap
	elif (len(chap.split(".")[0]) == 3):
		chapName = manga+"_chap0"+chap
	else:
		chapName = manga+"_chap"+chap
	return chapName

# Function to get the string page number (3 digits)
def getPageName(page):
	strPage = str(page)
	if (len(strPage) == 1):
		strPage = "00"+strPage
	elif (len(strPage) == 2):
		strPage = "0"+strPage
	return strPage

# Function to get all available mangas
# Fill a dictionnary with manga name as key and manga url as value
# return : void
def getMangasDico():
	# Get html content in a file
	os.system("curl -s " + URL_WEBSITE+URL_MANGAS_LIST+ " > "+PATH+"/mangaslist.txt")
	# read the file
	f = open(PATH+'/mangaslist.txt', 'r')
	content = f.readlines()
	f.close()

	boolInMangaDiv = False
	for line in content:
		if ('<ul class="series_alpha">' in line):
			boolInMangaDiv = True

		if ("</ul>" in line):
			boolInMangaDiv = False
			pass

		if (boolInMangaDiv):
			mangaUrl = line.split('<li><a href="')[1].split('">')[0]
			mangaName = mangaUrl.split('/')[1]
			DICO_MANGAS[mangaName] = mangaUrl

# Function to get chapter dico from a manga
# Fill with chapter name as key and chapter url as value
# Return : dictionnary
def getMangaChaptersDico(manga):
	# Get html content in a file
	os.system("curl -s " + URL_WEBSITE+DICO_MANGAS[manga]+ " | grep '" + '<a href="/' + manga + '/' + "'> "+PATH+"/mangaChapterslist.txt")
	# read the file
	f = open(PATH+'/mangaChapterslist.txt', 'r')
	content = f.readlines()
	f.close()

	dico_chapters = {}

	for line in content:
		if ("</li>" not in line):
			chapterUrl = line.split('<a href="')[1].split('">')[0]
			chapterNumber = getChapName(manga, chapterUrl.split('/')[2])
			dico_chapters[chapterNumber] = chapterUrl

	return dico_chapters

# Function to get pages dico from a chapter
# Fill with page name as key and page url as value
# Return : dictionnary
def getMangaChapterPagesDico(chapterUrl):
	dico_pages = {}
	chapterNumber = chapterUrl.split("/")[-1]

	# Get html content in a file
	os.system("curl -s " + URL_WEBSITE+chapterUrl+ " | grep '" + '<option value="' + chapterUrl + "'> "+PATH+"/mangaChapterPageslist.txt")
	# read the file
	f = open(PATH+'/mangaChapterPageslist.txt', 'r')
	content = f.readlines()
	f.close()

	for line in content:
		pageUrl = line.split('<option value="')[1].split('">')[0]
		if ("selected" in pageUrl):
			pageUrl = pageUrl.split('"')[0]
		pageNumber = getPageName(line.split('</option>')[0].split(">")[-1])
		dico_pages[pageNumber] = pageUrl

	return dico_pages

# Function to show all available manga according to a pattern
# Return : void
def showMangaList(pattern):
	for manga in sorted(DICO_MANGAS):
		if (pattern in manga):
			print "%s" % (manga)

# Function to download a page from a chapter
# Return : void
def downloadMangaChapterPage(path, chapter, chapterUrl, page, pageUrl):
	filename = chapter+"_"+page
	# Get html content in a file
	os.system("curl -s " + URL_WEBSITE+pageUrl+ " | grep '" + chapterUrl + "' | grep 'img' > "+PATH+"/mangaChapterPageUrl.txt")
	# read the file
	f = open(PATH+'/mangaChapterPageUrl.txt', 'r')
	content = f.readlines()
	f.close()
	if (len(content) != 1):
		print "ERROR", path, chapter, chapterUrl, page, pageUrl
		sys.exit(1)
	else:
		fileUrl = content[0].split('src="')[-1].split('"')[0]
		extension = fileUrl.split(".")[-1]
		os.system('curl -o '+path+"/"+filename+"."+extension+' '+ fileUrl  +" > /dev/null")

# Function to download a chapter from a manga
# Return : void
def downloadMangaChapter(path, manga, chapter, chapterUrl):
	print "# DL : chapter", str(chapter), "..."

	# Managing chapter folder creation
	try :
		os.mkdir(path+"/"+chapter)
	except :
		pass
	dico_pages = getMangaChapterPagesDico(chapterUrl)
	for page in sorted(dico_pages):
		downloadMangaChapterPage(path+"/"+chapter, chapter, chapterUrl, page, dico_pages[page])

# Function to download a manga
# Return : void
def downloadManga(manga):
	print "## DL", manga, "..."

	if (manga not in DICO_MANGAS.keys()):
		print "ERROR :", manga,"not in available mangas"
	else:
		# Managing manga folder creation
		try :
			os.mkdir(PATH+"/"+manga)
			print "# create a directory"
		except :
			print "# don't need to create a directory"
			pass

	dico_chapters = getMangaChaptersDico(manga)
	for chapter in sorted(dico_chapters):
		downloadMangaChapter(PATH+"/"+manga, manga, chapter, dico_chapters[chapter])

# Function to run the python script
def main():

	print "** Welcome to dlMangaReader **"
	print "... loading ..."
	# Loading mangas list
	getMangasDico()

	# Definition of argument option
	parser = argparse.ArgumentParser(prog="dlScans.py")
	parser.add_argument('-s', '--show', nargs=1, help='list of all available mangas', action='store', type=str)
	parser.add_argument('-m', '--manga', nargs=1, help='select a manga to download', action='store', type=str)
	parser.add_argument('-c', '--chap', nargs=1, help='select a specific chapter to download', action='store', type=str)
	parser.add_argument('-l', '--last', nargs=1, help='select a last X chapter to download', action='store', type=int)
	# Parsing of command line argument
	args = parser.parse_args(sys.argv[1:])

	if (args.show != None):
		print "** List of all available mangas **"
		showMangaList(args.show[0])
		sys.exit()

	elif (args.manga != None):
		if (args.chap == None and args.last == None):
			print "downloading all chapters from", args.manga[0]
			downloadManga(args.manga[0])
			print 1

		elif (args.chap != None):
			#print "downloading chapter", args.chap[0], "from", args.manga[0]
			#dlMangaChap(args.manga[0], args.chap[0])
			print 2
		else:
			#print "downloading the last", args.last[0], "chapter(s) from", args.manga[0]
			#dlMangaLastChap(args.manga[0], args.last[0])
			print 3
	else:
		print "/!\ No arguments"
		parser.print_help()

if __name__ == "__main__":
	main()