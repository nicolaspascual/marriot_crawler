from dataclasses import dataclass
from typing import List


@dataclass
class Response:
    """
    Class to hold the response of the reviews
    """
    author: str
    text: str

    def as_dict(self):
        """
        Casts to dict erasing empty values
        """
        response_json = {}
        if self.author:
            response_json['author'] = self.author
        if self.text:
            response_json['text'] = self.text
        return response_json


@dataclass
class Review:
    """
    Class to hold the reviews
    """
    author: str
    title: str
    text: str
    date: str
    score: float
    location_score: float
    responses: List[Response]

    def as_dict(self):
        """
        Casts to dict erasing empty values
        """
        review_json = {}
        if self.author:
            review_json['author'] = self.author
        if self.title:
            review_json['title'] = self.title
        if self.text:
            review_json['text'] = self.text
        if self.date:
            review_json['date'] = self.date
        if self.score:
            review_json['score'] = self.score
        if self.location_score:
            review_json['location_score'] = self.location_score
        if self.responses:
            review_json['responses'] = [
                response.as_dict()
                for response in self.responses
            ]
        return review_json
