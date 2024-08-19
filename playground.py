from pagerank import *

pages = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}, "4.html":{}}
print(len(pages))
for page in pages:
    print(len(pages[page]))

print(transition_model(pages, "1.html"))
print(transition_model(pages, "2.html"))

