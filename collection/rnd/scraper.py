import sys
sys.path = ['.', '..', '../src'] + sys.path

from newspaper import Article
import newspaper
from newspaper import fulltext
from src.utils import *
import requests

# url = "https://arquivo.pt/noFrame/replay/20090930101020/http://www.novacimangola.com/"
# url = "https://arquivo.pt/noFrame/replay/20091222224516/http://padoca.org/index.php?option=com_mtree&task=viewlink&link_id=386&Itemid=26"
url = "https://arquivo.pt/noFrame/replay/20121210213406/http://expresso.sapo.pt/blogues?p=index&mid1=ex.menus/23&m2=42&op=view"
t = try_request(url).text
# r = requests.get(url)
# print(r.encoding)
# r.encoding  ="utf-8"
# r.encoding  ="iso-8859-1"
# r.encoding = r.apparent_encoding
# t = r.text
# print(t)
# print(fulltext(t))

# url = 'https://arquivo.pt/noFrame/replay/20110124171216/http://www.jornaldenegocios.pt/index.php?template=SHOWNEWS&id=462991'
# # # url = 'https://m.arquivo.pt/noFrame/replay/20181229202018/https://expresso.sapo.pt/palavra/entity/people/Isabel-dos-Santos'

article = Article(url, _language="pt")
# # # article.build()
article.download(input_html=t)

# # # print(article.html)
article.parse()

# # # print(article.publish_date)
text = assert_valid_article(article)
print(text, flush=True)
print("-"*40)
print(article.top_image)

# # article.nlp()

# # print(article.summary)
# # print(article.keywords)

# import spacy

# nlp = spacy.load("pt_core_news_sm")

# # # doc = nlp("A empresa Nova Cimangola foi comprada por Isabel e Pedro")
# doc = nlp(article.text)

# for ent in doc.ents:
#     # print(ent.text, ent.start_char, ent.end_char, ent.label_)
#     print(ent.text, ent.label_)