import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor=DAMPING):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_prob = {}
    page_links_number = len(corpus[page])
    corpus_pages = len(corpus)
    if page_links_number == 0:
        for corpus_page in corpus:
            pages_prob[corpus_page] = 1.0 / corpus_pages
    else:
        starting_prob = (1 - damping_factor) / (page_links_number + 1)
        pages_prob = dict.fromkeys(corpus, starting_prob)
        for link in corpus[page]:
            pages_prob[link] = starting_prob + (damping_factor / page_links_number)
    return pages_prob

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_pagerank_dict = dict.fromkeys(corpus, 0)
    random_page = random.choice(list(corpus))
    for _ in range(0, n):
        model = transition_model(corpus, random_page, damping_factor)
        sample_pagerank_dict[random_page] += 1
        prob_values = list(model.values())
        # choose random page based on probability weights
        random_page = (random.choices(list(model), weights=prob_values, k=1))[0]
    total_inverse = 1.0 / sum(sample_pagerank_dict.values())
    for key, val in sample_pagerank_dict.items():
        sample_pagerank_dict[key] = val * total_inverse
    return sample_pagerank_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pagerank = dict.fromkeys(corpus, 1.0 / num_pages)
    converged = False
    
    while not converged:
        new_pagerank = {}
        for page in corpus:
            links_sum = 0
            for link in corpus:
                if page in corpus[link]:
                    links_sum += pagerank[link] / len(corpus[link])
                elif len(corpus[link]) == 0:
                    links_sum += pagerank[link] / num_pages
            
            new_pagerank[page] = ((1 - damping_factor) / num_pages) + (damping_factor * links_sum)
        
        # Normalize to ensure sum to 1
        total_inverse = 1.0 / sum(new_pagerank.values())
        for key, val in new_pagerank.items():
            new_pagerank[key] = val * total_inverse

        # Check for convergence
        if check_dict(new_pagerank, pagerank) == True:
                return pagerank
        pagerank = new_pagerank
    

def check_dict(new_dict, old_dict):
    """
    Returns True if both dictionaries are convergent i.e. difference between corresponding values is less than 0.001
    """
    for (k1, v1), (k2, v2) in zip(new_dict.items(), old_dict.items()):
        if k1 == k2:
            if (v1 - v2) > 0.001:
                return False
    return True

if __name__ == "__main__":
    main()
