import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException


class MarriotReviewsScraper(object):
    base_url = 'https://www.marriott.com/hotels/hotel-reviews/miaxr-the-st-regis-bal-harbour-resort/'
    driver_path = '/home/nicolas/workspace/career/bin/geckodriver'

    def __init__(self, max_pages):
        self.browser = webdriver.Firefox(
            executable_path=MarriotReviewsScraper.driver_path)
        self.max_pages = max_pages

    def call(self):
        self.browser.get(MarriotReviewsScraper.base_url)
        parsed_reviews = []
        for _ in range(self.max_pages - 1):
            parsed_reviews += self._parse_reviews()
            self._go_to_next_page()
        return parsed_reviews

    def _go_to_next_page(self):
        self.browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        self.browser.find_element_by_css_selector(
            '.BVRRNextPage > a'
        ).click()

    def _parse_reviews(self):
        reviews = self.browser.find_elements_by_css_selector(
            '#BVRRDisplayContentBodyID > .BVRRContentReview'
        )
        for review in reviews:
            yield {
                ** self._parse_text(review),
                ** self._parse_title(review),
                ** self._parse_date(review),
                ** self._parse_score(review),
                ** self._parse_location_score(review),
                ** self._parse_author(review),
                ** self._parse_responses(review)
            }

    def _parse_text(self, review):
        return {
            'text': review.find_element_by_class_name('BVRRReviewText').text
        }

    def _parse_title(self, review):
        return {
            'title': review.find_element_by_class_name('BVRRReviewTitle').text
        }

    def _parse_date(self, review):
        return {
            'date': review.find_element_by_class_name('BVRRReviewDate').text
        }

    def _parse_score(self, review):
        return {
            'score': float(review.find_element_by_css_selector(
                'div[itemprop=reviewRating] > span.BVRRRatingNumber'
            ).get_attribute('innerHTML').strip())
        }

    def _parse_location_score(self, review):
        return {
            'location_score': float(review.find_element_by_css_selector(
                '.BVRRRatingLocation .BVRRRatingNumber'
            ).get_attribute('innerHTML').strip())
        }

    def _parse_author(self, review):
        return {
            'author': review.find_element_by_class_name('BVRRUserNickname').text
        }

    def _parse_responses(self, review):
        try:
            review.find_element_by_class_name(
                'BVDI_COInsideBodyComments'
            )
        except NoSuchElementException:
            return {}

        responses = review.find_elements_by_css_selector(
            '.BVDI_COInsideBodyComments > div'
        )

        return {
            'responses': [
                self._parse_response(response)
                for response in responses
            ]
        }

    def _parse_response(self, response):
        return {
            'text': response.find_element_by_class_name('BVDI_COCommentText').text,
            'date': response.find_element_by_class_name('BVDI_COCommentDateValue').text
        }
