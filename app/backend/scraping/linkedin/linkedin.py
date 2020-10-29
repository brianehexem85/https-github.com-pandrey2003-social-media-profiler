from app.backend.scraping.linkedin.linkedin_search_info import (
    LinkedinSearchSubjects,
)


def caller_linkedin(first_name, last_name, job_title=None, company=None, school=None):
    results_to_filter = {}
    linkedin_obj = LinkedinSearchSubjects(
        first_name, last_name, job_title, company, school
    )
    linkedin_obj.linkedin_search()
    linkedin_obj.linkedin_filter()
    linkedin_obj.linkedin_search_for_info()
    results_to_filter["linkedin"] = list_of_all_items = []
    list_of_all_items.append({"found_subjects": linkedin_obj.found_subjects_info})
    list_of_all_items.append(
        {
            "potential_subjects_after_filtering": linkedin_obj.potential_subjects_after_filtering_info
        }
    )
    return results_to_filter


if __name__ == "__main__":
    print(
        caller_linkedin(
            "Dmytro",
            "Ovchynnykov",
            job_title="Software Engineer",
            company="Xenoss",
            school="Michigan",
        )
    )
