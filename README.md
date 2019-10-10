# Crawler for the web page Marriott

To call it you just need to execute
```bash
$ python .
# or
$ ./crawl.py
```


## Important considerations

Several options have been analysed before starting development of the project.
 - The use of scrapy was discarded because of the way this page loaded the content (ajax).
 - Plain requests and beautifulsoup was also evaluated but discarded because of the complexity of looking inside a JS file and the increase of a risk of changing not only the HTML but the JS.
 - Finally selenium together with the firefox browser was the one that I used because of its capability to load Ajax and its simple and understandable API.

The code is encapsulated in three main classes:
 - The class that holds the driver of selenium is called `SeleniumFacade` and is done in order to encapsulate settings, initialization and tear down.
 - The class that holds the parsing logic is called `MarriottReviewsCrawler` and it catches all the logic that is dependant from the HTML and JS of the web page.
 - Finally model dataclasses are made to hold the simplicity

An important observation is that I am not use to work with virtualenv, I usually work with pipenv and maybe the shebang in `crawl.py` is not ok. In case it is not ok please execute it as a normal python script.

## Running the tests

Some simple unit test cases have been added testing the models and simple logic in the crawler.

To run the tests you just need to execute
```bash
$ python -m unittest discover -s ./test 
```