"""CSCA08 Assignment 3: arxiv.org"""

import copy  # needed in examples of functions that modify input dict
from typing import TextIO, Dict, Union, List, Tuple

from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleValueType, ArticleType, ArxivType)


EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

EXAMPLE_ARXIV2 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Tafliovich', 'Anya Y.'),
                    ('Breuss', 'Nataliya')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

EXAMPLE_ARXIV3 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}

EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}

EXAMPLE_BY_AUTHOR2 = {
    ('Ponce', 'Marcelo'): ['008'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031', '827'],
    ('Pancer', 'Richard'): ['067']
}

EXAMPLE_BY_AUTHOR3 = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031']
}


def make_author_to_articles(
        id_to_article: ArxivType) -> dict[NameType, list[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in arxiv data id_to_article.

    Precondition: id_to_article is in correct format.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles(EXAMPLE_ARXIV2) == EXAMPLE_BY_AUTHOR2
    True
    >>> make_author_to_articles(EXAMPLE_ARXIV3) == EXAMPLE_BY_AUTHOR3
    True

    """

    author_to_articles = {}

    for article_id, article_info in id_to_article.items():
        authors = article_info.get(AUTHORS, [])
        for author in authors:
            if author not in author_to_articles:
                author_to_articles[author] = []
            author_to_articles[author].append(article_id)

    for articles in author_to_articles.values():
        articles.sort()

    return author_to_articles


def get_coauthors(
        id_to_article: ArxivType, author_name: NameType) -> list[NameType]:
    """Return a list of coauthors of the author specified by authors_name in
    arxiv data id_to_article.

    Precondition: id_to_article is in correct format.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]
    >>> get_coauthors(EXAMPLE_ARXIV2, ('Breuss', 'Nataliya'))
    [('Bretscher', 'Anna'), ('Tafliovich', 'Anya Y.')]
    >>> get_coauthors(EXAMPLE_ARXIV3, ('Breuss', 'Nataliya'))
    []

    """

    author_to_articles = make_author_to_articles(id_to_article)
    coauthors = set()

    if author_name in author_to_articles:
        articles_by_author = author_to_articles[author_name]
        for article_id in articles_by_author:
            authors = id_to_article[article_id][AUTHORS]
            coauthors.update(coauthor for coauthor in authors if
                             coauthor != author_name)

    coauthors = sorted(list(coauthors))
    return coauthors


def get_most_published_authors(id_to_article: ArxivType) -> list[NameType]:
    """Return a list of authors who published the most articles in
    arxiv data id_to_article.

    Precondition: id_to_article is in correct format.

    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> get_most_published_authors(EXAMPLE_ARXIV2)
    [('Bretscher', 'Anna'), ('Breuss', 'Nataliya'), ('Tafliovich', 'Anya Y.')]
    >>> get_most_published_authors(EXAMPLE_ARXIV3)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]

    """

    author_to_articles = make_author_to_articles(id_to_article)
    authors_article_count = {}

    for author, articles in author_to_articles.items():
        authors_article_count[author] = len(articles)

    max_count = 0
    most_published_authors = []

    for author, count in authors_article_count.items():
        if count > max_count:
            most_published_authors = [author]
            max_count = count
        elif count == max_count:
            most_published_authors.append(author)

    most_published_authors.sort()

    return most_published_authors


def suggest_collaborators(
        id_to_article: ArxivType, author_name: NameType) -> list[NameType]:
    """Returns a list of authors with whom the author specificed, authors_name,
    is encouraged to collaborate in arxiv data id_to_article.

    Precondition: id_to_article is in correct format.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> suggest_collaborators(EXAMPLE_ARXIV2, ('Ponce', 'Marcelo'))
    [('Bretscher', 'Anna'), ('Breuss', 'Nataliya')]
    >>> suggest_collaborators(EXAMPLE_ARXIV3, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna')]

    """

    coauthors = get_coauthors(id_to_article, author_name)
    suggested_collaborators = set()

    for coauthor in coauthors:
        coauthor_of_coauthor = get_coauthors(id_to_article, coauthor)
        suggested_collaborators.update(suggested for
                                       suggested in coauthor_of_coauthor if
                                       suggested != author_name and
                                       suggested not in coauthors)

    suggested_collaborators = sorted(list(suggested_collaborators))
    return suggested_collaborators


def has_prolific_authors(
        author_articles: dict[NameType, list[str]], information: ArticleType,
        min_publications: int) -> bool:
    """Returns True if and only if the article, author_articles, and ID,
    information, has at least one author who is considered prolific based on
    the minimum number of publications required, min_publications.

    Precondition: author_articles is in correct format.

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['008'], 2)
    True
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['031'], 2)
    False
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV['031'], 5)
    False

    """

    for author in information[AUTHORS]:
        if len(author_articles[author]) >= min_publications:
            return True
    return False


def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update the articles data id_to_article so that it contains only
    articles published by authors with min_publications or more
    articles published. As long as at least one of the authors has
    min_publications, the article is kept.

    Precondition: id_to_article is in correct format

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True

    >>> arxiv_copy2 = copy.deepcopy(EXAMPLE_ARXIV2)
    >>> keep_prolific_authors(arxiv_copy2, 1)
    >>> len(arxiv_copy2)
    4
    >>> '008' in arxiv_copy2 and '067' in arxiv_copy2 and '827' in arxiv_copy2
    True

    >>> arxiv_copy3 = copy.deepcopy(EXAMPLE_ARXIV3)
    >>> keep_prolific_authors(arxiv_copy3, 2)
    >>> len(arxiv_copy3)
    3
    >>> '008' in arxiv_copy3 and '067' in arxiv_copy3 and '827' in arxiv_copy3
    True

    """

    author_to_articles = make_author_to_articles(id_to_article)
    prolific_authors = set()

    for author, articles in author_to_articles.items():
        if len(articles) >= min_publications:
            prolific_authors.add(author)

    articles_to_remove = []
    for article_id, article_info in id_to_article.items():
        article_authors = article_info.get(AUTHORS, [])
        has_prolific = set(article_authors).intersection(prolific_authors)
        if not has_prolific:
            articles_to_remove.append(article_id)

    for article_id in articles_to_remove:
        id_to_article.pop(article_id)


def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout.
    """
    ids = {}

    articles = afile.read().split(END + '\n')[:-1]

    for article in articles:
        info = article.split('\n')[:-1]
        article_id = info[0]
        ids[article_id] = {
            ID: article_id, TITLE: info[1] if info[1] != '' else None,
            CREATED: info[2] if info[2] != '' else None,
            MODIFIED: info[3] if info[3] != '' else None, AUTHORS: [],
            ABSTRACT: None}

        other_info = info[4:]
        ref_end = other_info.index('')

        for line in other_info[:ref_end]:
            author_details = line.split(SEPARATOR)
            author_name = author_details[0]
            author_affiliation = author_details[1]

            author_info = (author_name, author_affiliation)
            ids[article_id][AUTHORS].append(author_info)

        ids[article_id][AUTHORS].sort()

        ids[article_id][ABSTRACT] = '\n'.join(other_info[ref_end + 1:])

    return ids
