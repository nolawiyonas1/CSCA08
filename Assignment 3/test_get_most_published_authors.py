"""CSCA08 Assignment 3: arxiv.org"""

from copy import deepcopy
import unittest
from arxiv_functions import get_most_published_authors as get_mpas


class TestGetMostPublishedAuthors(unittest.TestCase):
    """Test the function get_most_published_authors."""

    def setUp(self):
        self.example = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
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
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [('Bretscher', 'Anna'),
                            ('Ponce', 'Marcelo'),
                            ('Tafliovich', 'Anya Y.')],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example1 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
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
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [('Bretscher', 'Anna'),
                            ('Ponce', 'Marcelo')],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example2 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
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
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [('Ponce', 'Marcelo'),
                            ('Tafliovich', 'Anya Y.')],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example3 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
            '031': {
                'identifier': '031',
                'title': 'Calculus is the best course ever',
                'created': None,
                'modified': '2021-09-02',
                'authors': [],
                'abstract': '''We discuss the reasons why Calculus I
                is the best course.'''},
            '067': {'identifier': '067',
                    'title': 'Discrete Mathematics is the best course ever',
                    'created': '2021-09-02',
                    'modified': '2021-10-01',
                    'authors': [],
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example4 = {
        }

        self.example5 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
            '031': {
                'identifier': '031',
                'title': 'Calculus is the best course ever',
                'created': None,
                'modified': '2021-09-02',
                'authors': [],
                'abstract': '''We discuss the reasons why Calculus I
                is the best course.'''},
            '067': {'identifier': '067',
                    'title': 'Discrete Mathematics is the best course ever',
                    'created': '2021-09-02',
                    'modified': '2021-10-01',
                    'authors': [],
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example6 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
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
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [('Ponce', 'Marcelo')],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [('Pancer', 'Richard')],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

        self.example7 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.'),
                            ('Ponce', 'Marcelo')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')}
        }

        self.example8 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.'),
                            ('Ponce', 'Marcelo')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')}
        }


    def test_handout_example(self):
        """Test get_most_published_authors with the handout example."""

        arxiv_copy = deepcopy(self.example)
        expected = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(self.example)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_2_authors(self):
        """Test get_most_published_authors with 2 authors that published the
        most. """

        arxiv_copy1 = deepcopy(self.example1)
        expected1 = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo')]
        actual1 = get_mpas(self.example1)
        msg1 = message(arxiv_copy1, expected1, actual1)
        self.assertEqual(actual1, expected1, msg1)

    def test_1_authors(self):
        """Test get_most_published_authors with 1 author that published the
        most. """

        arxiv_copy2 = deepcopy(self.example2)
        expected2 = [('Tafliovich', 'Anya Y.')]
        actual2 = get_mpas(self.example2)
        msg2 = message(arxiv_copy2, expected2, actual2)
        self.assertEqual(actual2, expected2, msg2)

    def test_0_authors(self):
        """Test get_most_published_authors with 0 authors that published the
        most. """

        arxiv_copy3 = deepcopy(self.example3)
        expected3 = []
        actual3 = get_mpas(self.example3)
        msg3 = message(arxiv_copy3, expected3, actual3)
        self.assertEqual(actual3, expected3, msg3)

    def test_empty_dictionary(self):
        """Test get_most_published_authors with an empty dictionary """

        arxiv_copy4 = deepcopy(self.example4)
        expected4 = []
        actual4 = get_mpas(self.example4)
        msg4 = message(arxiv_copy4, expected4, actual4)
        self.assertEqual(actual4, expected4, msg4)

    def test_1_author_in_dict(self):
        """Test get_most_published_authors with only 1 author in the
        dictionary"""

        arxiv_copy5 = deepcopy(self.example5)
        expected5 = [('Tafliovich', 'Anya Y.')]
        actual5 = get_mpas(self.example5)
        msg5 = message(arxiv_copy5, expected5, actual5)
        self.assertEqual(actual5, expected5, msg5)

    def test_all_author_same_publication(self):
        """Test get_most_published_authors with all authors with the same
        number of publications dictionary"""

        arxiv_copy6 = deepcopy(self.example6)
        expected6 = [('Bretscher', 'Anna'),
                     ('Breuss', 'Nataliya'),
                     ('Pancer', 'Richard'),
                     ('Ponce', 'Marcelo'),
                     ('Tafliovich', 'Anya Y.')]
        actual6 = get_mpas(self.example6)
        msg6 = message(arxiv_copy6, expected6, actual6)
        self.assertEqual(actual6, expected6, msg6)

    def test_one_article(self):
        """Test get_most_published_authors with one article in the dictionary"""

        arxiv_copy7 = deepcopy(self.example7)
        expected7 = [('Ponce', 'Marcelo'),
                     ('Tafliovich', 'Anya Y.')]
        actual7 = get_mpas(self.example7)
        msg7 = message(arxiv_copy7, expected7, actual7)
        self.assertEqual(actual7, expected7, msg7)

    def test_mutation(self):
        """Confirm that get_most_published_authors does not mutate the input
        dict."""

        arxiv_copy8 = deepcopy(self.example8)
        expected8 = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Tafliovich', 'Anya Y.'),
                            ('Ponce', 'Marcelo')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')}
        }
        get_mpas(self.example8)
        msg8 = message(arxiv_copy8, expected8, arxiv_copy8)
        self.assertEqual(arxiv_copy8, expected8, msg8)


def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ('When we called get_most_published_authors(' + str(test_case)
            + ') we expected ' + str(expected)
            + ', but got ' + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)

