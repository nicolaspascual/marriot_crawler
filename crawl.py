#!/usr/bin/env python
import json

from crawler import MarriotReviewsScraper

reviews = MarriotReviewsScraper(4).call()
reviews = [review.as_dict() for review in reviews]
print(json.dumps(reviews))
