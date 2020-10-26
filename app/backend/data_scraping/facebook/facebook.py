# -*- coding: utf-8 -*-
from app.backend.data_scraping.facebook.facebook_search \
    import FacebookSearchLinks
from app.backend.data_scraping.scraper.scraping import scraping


def facebook(query):
    results_to_filter = {}
    facebook_obj = FacebookSearchLinks(query)
    facebook_obj.open_home_page()
    facebook_obj.facebook_authenticate()
    facebook_obj.find_scraping_links()
    filtered_items = facebook_obj.regex_matching_items
    scraped_webpages = scraping(filtered_items)
    results_to_filter["facebook"] = scraped_webpages
    return results_to_filter


if __name__ == "__main__":
    print(facebook("ongradient"))