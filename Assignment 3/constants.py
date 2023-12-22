"""CSCA08 Assignment 3: arxiv.org"""

ID = 'identifier'
TITLE = 'title'
CREATED = 'created'
MODIFIED = 'modified'
AUTHORS = 'authors'
ABSTRACT = 'abstract'
END = 'END'
SEPARATOR = ','

# We store names as tuples of two strs: (last-name, first-name(s)).
NameType = tuple[str, str]

# ArticleValueType is the type for valid values in the ArticleType
# dict.  All values are None or str, except for the value associated
# with key AUTHORS, which is a list of NameType.
ArticleValueType = None | str | list[NameType]

# ArticleType is a dict that maps keys ID, TITLE, CREATED, MODIFIED,
# AUTHORS, and ABSTRACT to their values (of type ArticleValueType).
ArticleType = dict[str, ArticleValueType]

# ArxivType is a dict that maps article identifiers to articles,
# i.e. to values of type ArticleType.
ArxivType = dict[str, ArticleType]
