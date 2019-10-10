from crawler import MarriotReviewsScraper
import json

reviews = MarriotReviewsScraper(4).call()
print(json.dumps(reviews))