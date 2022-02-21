#Evan Dartt
#Lab Practical 2
#3-1-19
import urllib.request, re, webbrowser
#Section 1 - open and parse the webpage

web_page = urllib.request.urlopen("http://cgi.soic.indiana.edu/~dpierz/news.html")
contents = web_page.read().decode(errors="replace")
web_page.close()
base = "http://cgi.soic.indiana.edu/~dpierz/news.html"

#Section 2 - produce list of all news articles and headlines
body = re.findall('(?<=<body).+?(?=</html>)', contents, re.DOTALL)[0]
headlines = re.findall('(?<="headline">).+?(?=</span>)', body)
articles = [article for article in headlines]
print("Searching:", base)
print()
for article in articles:
    print("\t", article)
    print()
    print()
#Section 3 - Input user for a word/phrase and display articles with input in word/phrase from the website
print("Searching:", base)
print()
userInp = input("Please enter a word to search for: ")
wordSearch = [article for article in headlines if userInp.lower() in 
article.lower()]

for article in wordSearch:
        print("\t", article)
#Section 4 - Bonus: Pull up a link to news articles with the word the user input
links = [article for article in wordSearch if article in headlines]
for article in links:
    webbrowser.open_new_tab(article)