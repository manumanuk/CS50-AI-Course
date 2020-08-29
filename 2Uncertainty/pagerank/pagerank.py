import os
import random
import re
import sys
import copy

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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    transitionModel = dict()
    randomizedAddition = (1-damping_factor)/len(corpus)

    if len(links) == 0:
        for thisPage in corpus:
            transitionModel[thisPage] = 1/len(corpus)
        return transitionModel

    for thisPage in corpus:
        transitionModel[thisPage] = 0
        transitionModel[thisPage] += (damping_factor/len(links) + randomizedAddition) if (thisPage in links) else (randomizedAddition)
    return transitionModel
    

        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    visited = dict()
    for page in pages:
        visited[page] = 0
    currentPage = pages[random.randint(0, len(pages)-1)]
    
    for i in range(0, n-1):
        visited[currentPage] += 1
        transitionModel = transition_model(corpus, currentPage, damping_factor)
        randomizer = random.randint(0, 100)/100
        for page in transitionModel:
            randomizer -= transitionModel[page]
            if randomizer <= 0:
                currentPage = page
                break
            
    for page in visited:
        visited[page] = visited[page]/n

    return visited


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    FORMULA_BASIC = (1-damping_factor)/len(corpus)
    
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())
    PAGES_THAT_LINK = dict()
    for page in corpus:
        PAGES_THAT_LINK[page] = set()
        for linkPage in corpus:
            if page in corpus[linkPage]:
                PAGES_THAT_LINK[page].add(linkPage)

    prevRankVal = dict()
    currentRankVal = dict()
    for page in corpus:
        currentRankVal[page] = 1/len(corpus)
    
    def converged():
        if len(prevRankVal) == 0:
            return False
        for page in currentRankVal:
            if abs(currentRankVal[page] - prevRankVal[page]) >= 0.001:
                return False
        return True

    def applyFormula(page):
        formula_summation = 0
        for pointer in PAGES_THAT_LINK[page]:
            formula_summation += prevRankVal[pointer]/len(corpus[pointer])
        currentRankVal[page] = FORMULA_BASIC + formula_summation*damping_factor
        return

    while not converged():
        prevRankVal = copy.deepcopy(currentRankVal)
        for page in currentRankVal:
            applyFormula(page)
    return currentRankVal


if __name__ == "__main__":
    main()
