# -*- coding: utf-8 -*-
"""The Facebook scraping module saving selectors to find elements on Facebook pages."""

from selenium.webdriver.common.by import By

EMAIL_FIELD = (By.ID, "email")
PASSWORD_FIELD = (By.ID, "pass")
SUBMIT_BUTTON = (By.ID, "u_0_b")

SEARCH_LINK = "https://www.facebook.com/search/top?q="
FOUND_LINKS_USUAL = (By.CSS_SELECTOR, ".d2edcug0.glvd648r.o7dlgrpb a")
FOUND_LINKS_OTHER = (By.CSS_SELECTOR, ".j83agx80 a")
