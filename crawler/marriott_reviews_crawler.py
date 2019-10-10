from .selenium_facade import SeleniumFacade
from .models import Response, Review
from retry import retry


class MarriotReviewsScraper(object):
    base_url = 'https://www.marriott.com/hotels/hotel-reviews/miaxr-the-st-regis-bal-harbour-resort/'

    def __init__(self, max_pages):
        self.browser = SeleniumFacade()
        self.max_pages = max_pages

    def call(self):
        """
        Main loop of the algorithm which just parses the HTML while passing
        pages
        """
        self.browser.get(MarriotReviewsScraper.base_url)
        parsed_reviews = self._parse_reviews()
        for _ in range(self.max_pages - 1):
            self._go_to_next_page()
            parsed_reviews += self._parse_reviews()
        return parsed_reviews

    def _go_to_next_page(self):
        """
        Goes to next page by clicking on the a element at the bottom of the page
        """
        self.browser.find_element_by_css_selector(
            '.BVRRNextPage > a'
        ).click()

    def _parse_reviews(self):
        """
        Parses the review of the page
        """
        self.browser.scroll_bottom()  # In order to make sure that everything is loaded
        reviews = self.browser.find_elements_by_css_selector(
            '#BVRRDisplayContentBodyID > .BVRRContentReview'
        )
        return [
            Review(
                title=self._parse_title(review),
                author=self._parse_author(review),
                text=self._parse_text(review),
                date=self._parse_date(review),
                score=self._parse_score(review),
                location_score=self._parse_location_score(review),
                responses=self._parse_responses(review)
            )
            for review in reviews
        ]

    def _parse_text(self, review):
        """
        Parses the text of the review 
        """
        return review.find_element_by_class_name('BVRRReviewText').text

    def _parse_title(self, review):
        """
        Parses the title of the review 
        """
        return review.find_element_by_class_name('BVRRReviewTitle').text

    def _parse_date(self, review):
        """
        Parses the date of the review 
        """
        return review.find_element_by_class_name('BVRRReviewDate').text

    def _parse_score(self, review):
        """
        Parses the score of the review and casts it.

        Special retrieval method is used becouse of malformation in the HTML.
        For this reason get_attribute is used instead of text
        """
        return self._to_float(review.find_element_by_css_selector(
            'div[itemprop=reviewRating] > span.BVRRRatingNumber'
        ).get_attribute('innerHTML').strip())

    def _parse_location_score(self, review):
        """
        Parses the location score of the revie and casts it.

        Special retrieval method is used becouse of malformation in the HTML.
        For this reason get_attribute is used instead of text
        """
        return self._to_float(review.find_element_by_css_selector(
            '.BVRRRatingLocation .BVRRRatingNumber'
        ).get_attribute('innerHTML').strip())

    def _to_float(self, string):
        """
        Tries to cast a float, in case there is a problem it returns None.
        """
        try:
            return float(string)
        except ValueError:
            return None

    def _parse_author(self, review):
        """
        Parses the author of the review.
        """
        return review.find_element_by_class_name('BVRRUserNickname').text

    def _parse_responses(self, review):
        """
        Parses the responses of the review.
        """
        responses = review.find_elements_by_css_selector(
            '.BVDI_COInsideBodyComments > div'
        )

        return [
            self._parse_response(response)
            for response in responses
        ]

    def _parse_response(self, response):
        """
        Parse each specific response.
        """
        return Response(
            text=response.find_element_by_class_name(
                'BVDI_COCommentText').text,
            author=response.find_element_by_class_name(
                'BVDI_COCommentDateValue').text
        )
