from pagerank import *
import random

pages = {'1': {'2'}, '2': {'1', '3'}, '3': {'4', '2'}, '4': {'2'}}

result = iterate_pagerank(pages, 0.85)
print(result)
