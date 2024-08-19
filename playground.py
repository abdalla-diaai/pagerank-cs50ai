from pagerank import *
import random

pages = {'1': {'2'}, '2': {'3', '1'}, '3': {'4', '2'}, '4': {'2'}, '5': {'6'}, '6': {'7', '5'}, '7': {'6', '8'}, '8': {'6'}}

print(sample_pagerank(pages, 0.85, 100))



