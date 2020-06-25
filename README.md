# Scraping-Scrapy

### Indeed_scrap:

Here is a scrap of Indeed website extracting review details of a random company.

It demonstrates the use of scrapy crawler and Rules. An alternative could <br>
have been to use the absolute URLs and a Request object to get to the <br>
next page but I wanted to show how LinkExtractor could give same result.

Please note in order to yield all items in a structured manner the below code line has been entered in the settings.py file. <br>
FEED_EXPORT_FIELDS = ['job_title', 'location', 'date', 'rating', 'title', 'comment', 'pros', 'cons']

Do not hesistate to contact me if you find a more efficient way to get <br>
the same result or if any improvements can be made.

### Glassdoor_scrap:

Here is a scrap of Glassdoor website extracting same details as above. <br>

It demonstrates the use of scrapy splash to handle javascript pages,<br>
and also the use of the FormRequest.from_response to handle the login page.<br>

