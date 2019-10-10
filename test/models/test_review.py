from crawler.models import Response, Review
import unittest

class TestResponse(unittest.TestCase):

    def test_as_dict(self):
        response = Response(
            author='Nicolas',
            text='text'
        )

        self.assertDictEqual(
            {'author': 'Nicolas', 'text': 'text'},
            response.as_dict()
        )

        response = Response(
            author='Nicolas',
            text=''
        )

        self.assertDictEqual(
            {'author': 'Nicolas'},
            response.as_dict()
        )


class TestReview(unittest.TestCase):

    def test_as_dict(self):
        review = Review(
            author='Nicolas',
            title='title',
            text='text',
            date='date',
            score=5.0,
            location_score=0.4,
            responses=[
                Response(
                    author='Nicolas',
                    text=''
                )
            ]
        )

        self.assertDictEqual(
            {
                'author': 'Nicolas', 'text': 'text', 'title': 'title',
                'date': 'date', 'score': 5.0, 'location_score': 0.4,
                'responses': [{'author': 'Nicolas'}]
            },
            review.as_dict()
        )

        review = Review(
            author='Nicolas',
            title='title',
            text='',
            date='',
            score=None,
            location_score=0.4,
            responses=[]
        )

        self.assertDictEqual(
            {
                'author': 'Nicolas', 'title': 'title',
                'location_score': 0.4
            },
            review.as_dict()
        )
