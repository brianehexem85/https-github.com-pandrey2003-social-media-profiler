# -*- coding: utf-8 -*-
"""The LinkedIn subjects' subjects' searching module."""

import os
from linkedin_api import Linkedin as LinkedinAPI


class LinkedinSearch:
    """
    The class to search for subjects and put them into `found` and `potential` categories.
    """
    def __init__(self, user_input):
        self.first_name = user_input["first_name"]
        self.last_name = user_input["last_name"]
        self.keyword_company = user_input["company"]
        self.keyword_school = user_input["school"]
        self.keyword_title = user_input["job_title"]
        self._api = None
        self._found_subjects = []
        self._potential_subjects = []

    def linkedin_search(self):
        """
        Call other methods to search for subjects and put them into appropriate categories.
        """
        self.__linkedin_authenticate()
        self.__linkedin_search_for_subjects()

    def __linkedin_authenticate(self):
        """Authenticate using LinkedIn login and password."""
        self._api = LinkedinAPI(os.getenv("LINKEDIN_LOGIN"), os.getenv("LINKEDIN_PASSWORD"))

    def __linkedin_search_for_subjects(self):
        """
        Search for a subject in an ideal case or, if not found, find potential candidates.
        """
        self.__linkedin_search_in_ideal_case()
        if not self._found_subjects:
            self.__linkedin_search_for_potential_candidate()

    def __linkedin_search_in_ideal_case(self):
        """
        Search for a subject in an ideal case if provided all necessary information.
        """
        if self.keyword_company and self.keyword_school and self.keyword_title:
            self._found_subjects = self._api.search_people(
                keyword_first_name=self.first_name,
                keyword_last_name=self.last_name,
                keyword_company=self.keyword_company,
                keyword_school=self.keyword_school,
                keyword_title=self.keyword_title,
            )

    def __linkedin_search_for_potential_candidate(self):
        """
        Search for potential candidates with any provided information.
        """
        for i in range(3):
            try:
                # TODO: allow code duplication, but make code more explicit
                results = self._api.search_people(
                    keyword_first_name=self.first_name,
                    keyword_last_name=self.last_name,
                    keyword_company=None
                    if i != 0
                    else self.keyword_company
                    if self.keyword_company
                    else 1 / 0,
                    keyword_school=None
                    if i != 1
                    else self.keyword_school
                    if self.keyword_school
                    else 1 / 0,
                    keyword_title=None
                    if i != 2
                    else self.keyword_title
                    if self.keyword_title
                    else 1 / 0,
                )
            except ZeroDivisionError:
                continue
            self._potential_subjects.extend(results)
