import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = dict()

    corpus = os.path.join(os.getcwd(), directory)
    
    for text in os.listdir(corpus):
        f = open(os.path.join(corpus, text), "r", encoding="utf8")
        content = f.read()
        data[text] = content
    
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenizedDoc = nltk.word_tokenize(document)
    tokenizedWords = list()
    for word in tokenizedDoc:
        word = word.lower()
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            tokenizedWords.append(word)
    
    return tokenizedWords


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfsDict = dict()
    for document in documents:
        for word in documents[document]:
            if word in idfsDict:
                continue
            docFreq = 0
            for document2 in documents:
                docFreq = docFreq+1 if word in documents[document2] else docFreq
            idfsDict[word] = math.log(len(list(documents.keys()))/docFreq)
    return idfsDict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    for document in files:
        wordsList = files[document].copy()
        tf_idfs[document] = 0
        for word in query:
            tf = 0
            while word in wordsList:
                tf+=1
                wordsList.remove(word)
            tf_idfs[document] += tf*idfs[word]

    return sorted(list(tf_idfs.keys()), key=tf_idfs.__getitem__, reverse=True)[0:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentenceRank = dict()

    for sentence in sentences:
        sentenceRank[sentence] = { 'idf' : 0, 'qtd' : 0 }

        sentenceCopy = sentences[sentence].copy()
        
        idfVal = 0
        qtd = 0
        
        for word in query:
            if word in sentences[sentence]:
                idfVal+=idfs[word]
            while word in sentenceCopy:
                qtd += 1
                sentenceCopy.remove(word)
        sentenceRank[sentence]['idf'] = idfVal
        sentenceRank[sentence]['qtd'] = qtd/len(sentences[sentence])
        
    return sorted(list(sentenceRank.keys()), key=lambda x: (sentenceRank[x]['idf'], sentenceRank[x]['qtd']), reverse=True)[0:n]


if __name__ == "__main__":
    main()
