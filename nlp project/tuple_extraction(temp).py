from googleapiclient.discovery import build  # Foreign package # 1
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
from stanfordnlp.server import CoreNLPClient
from _collections import defaultdict
import sys


def search(query):
    '''
    Desc: Func 1
          Use API KEY and Engine KEY and given query to search and collect all related urls
    Input:  query -> str: The query sent to Google Search API
    Output: result -> list[QueryResult]:
    Desc:   Search by calling Google Custom Search API
            with input query terms.
            Return a list of (10) search results.
    '''
    # Call Google Custom Search API
    JSON_API_KEY = "AIzaSyD0WJeVcERv5UqcejEivhphMsl51V57xTo"
    SEARCH_ENGINE_ID = '002371957732170139182:bp5t7qbbl38'
    service = build("customsearch", "v1", developerKey=JSON_API_KEY)
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, ).execute()

    # Parse returned query results
    # print("items", res['items'])
    urls = []
    for item in res['items']:
        # unicode to utf-8
        link = item['link'].strip()
        print("=================Parsed URL==================")
        print(link)
        print("=============================================")
        urls.append(link)
    return urls


def tagVisible(element):
    '''
    Desc: Utility function for Func 2
          This function filter helps Func 2(soup) to filter unwanted tags like <style></style> and so on
    Input: an element which is a child of the whole html document object -> str
    Output: if it contain plain text that we want -> boolean
    '''
    unwantedElements = ['style', 'script', 'head', 'title', 'meta', '[document]']
    if element.parent.name in unwantedElements:
        return False
    if isinstance(element, Comment):
        return False
    return True


def textFromHtml(body):
    '''
    Desc: Utility func for Func 2
          This function help Func 2 to parse given html text and return only plain text
    Input: a html document that may contain js scripts, css styles and other stuff -> str
    Output: a clean text (<20000 characters) that only contains plain text
    '''
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tagVisible, texts)
    cleanText = u" ".join(t.strip() for t in visible_texts)
    if len(cleanText) > 20000:
        return cleanText[:20000]
    print("=================Clean Text==================")
    print(cleanText)
    print("=============================================")
    return cleanText


def soup(urls):
    '''
    Desc: Func 2
          This function will parse k urls and clean each html document, then it will return 
          clean plain text
          We use urllib to make http request and all the parsing job will be assigned to 
          2 util functions to finish 
    Input: 10 url -> list[str]
    Output: Clean(<20000 words) Content -> list[str]
    '''
    cleanText = []
    for url in urls:
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request, timeout=20)
        except Exception as e:
            print("=================Exception===================")
            print("Can not parse this url and skip it.")
            print("=============================================")
            continue
        if not response or response.getcode() != 200:
            continue
        html = response.read()
        text = textFromHtml(html)
        cleanText.append(text)
    return cleanText


def tupleExtraction(c_txt, input_r):
    '''
    Input: cleanText -> list[str] each str is a plain text with character less than 20000
    input_r -> [int] relation type
    Output: tuples ->  {tuple1:confidence1, tuple2:confidence2, ...}
    '''
    annotators_ner = ['tokenize', 'ssplit', 'pos', 'lemma', 'ner']  # custom parameters for annotators
    annotators_kbp = ['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'depparse', 'coref', 'kbp']
    extract_tuples = defaultdict(float)  # initialize the output
    for text in c_txt:
        annot_pre = helper_pipeline1(text, input_r, annotators_ner)
        if annot_pre != '':
            helper_pipeline2(annot_pre, input_r, annotators_kbp, extract_tuples)

    return extract_tuples


def helper_pipeline1(text, relation, annotator):
    """
    Input: text -> str is a plain text with character less than 20000
    relation -> [int] relation type
    annotator -> annotator type
    Output: tuples ->  {tuple1:confidence1, tuple2:confidence2, ...}
    """
    with CoreNLPClient(timeout=30000, memory='8G') as pipeline:  # first pipeline to do some rough notation
        ann_res = pipeline.annotate(text, annotators=annotator)
    filtered_content = ''
    for sentence in ann_res.sentence:  # filter those sentences without targeted token types
        entities = defaultdict(int)
        tokens = sentence.token
        for token in tokens:
            if token.ner != "O":
                entities[token.ner] += 1
        if relation == 1 or relation == 2 or relation == 4 and "ORGANIZATION" in entities and "PERSON" in entities:
            filtered_content += ' '.join([token.word for token in tokens])  # recover sentences from tokens
        elif relation == 3 and "PERSON" in entities:
            if "LOCATION" in entities or "CITY" in entities or "STATE_OR_PROVINCE" in entities or "COUNTRY" in entities:
                filtered_content += ' '.join([token.word for token in tokens])
    return filtered_content


def helper_pipeline2(text, relation, annotator, extract_tuples):
    """
    Input: text -> text with sentences containing wanted type of words
    relation -> [int] relation type
    annotator -> annotator type
    extract_tuples->  {tuple1:confidence1, tuple2:confidence2, ...}
    """
    relation_std = {1: 'per:schools_attended', 2: 'per:employee_or_member_of', 3: 'per:cities_of_residence',
                    4: 'org:top_members_employees'}  # to identify relations of tuples
    with CoreNLPClient(timeout=150000, memory='8G') as pipeline:
        ann_res = pipeline.annotate(text, annotators=annotator)
        for sentence in ann_res.sentence:
            for kbp_triple in sentence.kbpTriple:
                if kbp_triple.relation == relation_std[relation] and extract_tuples[
                    (kbp_triple.subject, kbp_triple.object)] <= kbp_triple.confidence:
                    extract_tuples[(kbp_triple.subject, kbp_triple.object)] = kbp_triple.confidence
        # to extract wanted type of relation tuples and corresponding confidence

def addTuplesToX(tuples, t, X):
    '''
    Desc:  Func 4
           This function will receive tuples extracted from the current iteration.
           Then, for every tuple, it will see if this tuple has already been added into
           X. If it has been added, it will update its confidence if new confidence is higher.
           If it does not, it will add this tuple to X and unused tuples so that we can make up 
           new querys in the next iteration
    Input: tuples in confidence decreasing order -> {tuple1:confidence1, tuple2:confidence2, ...}
           X -> dict
           t -> float ( 0 < t < 1 )
    Output: top K tuples if the number of tuples is greater than K and False to stop looping
            or not used tuple with the highest confidence and True to keep next loop
    '''
    unusedTuples = dict()
    for tup in tuples.keys():
        if tuples[tup] < t:
            continue
        if tup in X.keys() and tuples[tup] > X[tup]:
            X[tup] = tuples[tup]  # update an existing tuple or add new tuple into X
        elif tup not in X.keys():
            print("=================New Tuple===================")
            print(tup)
            X[tup] = tuples[tup]
            unusedTuples[tup] = tuples[tup]
            print("=============================================")

    return X, unusedTuples


if __name__ == '__main__':
    X = dict()  # key: tuple ->  egs: (Gates, 1, "Bill & Melinda Gates Foundation")
                # 1 means per:employee_or_member_of for example
                # value: float -> egs: 0.6693865436176671
                # This float is the extraction confidence
    k = int(sys.argv[4])
    q = sys.argv[3]
    r = int(sys.argv[1])
    t = float(sys.argv[2])
    print("==================Parameters=================")
    print("Client key      = AIzaSyD0WJeVcERv5UqcejEivhphMsl51V57xTo")
    print("Engine key      = 002371957732170139182:bp5t7qbbl38")
    print("Relation        = per:schools_attended")
    print("Threshold       = ", t)
    print("Query           = ", q)
    print("# of Tuples     = ", k)
    print("=============================================")
    print("Loading necessary libraries; This should take a minute or so ...")
    index = 0
    while len(X) < k:
        print("===============Iteration {} start============".format(index))
        urls = search(q)
        cleanText = soup(urls)
        tuples = tupleExtraction(cleanText, r)
        X, unusedTuples = addTuplesToX(tuples, t, X)
        if len(X) < k:
            q += " ".join(
                sorted(unusedTuples.items(), key=lambda item: item[1], reverse=True)[0][0])
        print("===============Iteration {} end==============".format(index))
        index += 1
    topKTuples = sorted(X.items(), key=lambda item: item[1], reverse=True)
    print("================Top {} Tuples================".format(k))
    for i in range(k):
        print(topKTuples[i])
    print("=============================================")

