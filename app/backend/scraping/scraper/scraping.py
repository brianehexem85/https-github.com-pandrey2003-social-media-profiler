# -*- coding: utf-8 -*-
"""The main XPATH scraping module."""

import asyncio
import aiohttp
import nest_asyncio

from lxml import html


def scraping(list_of_links_and_configs: list) -> list:
    """
    Take the list of links and configurations (XPATH selectors) \
    and return scraped elements from webpages.

    Args:
         list_of_links_and_configs: the list of links to webpages with XPATH selectors from params files.
    Returns:
         list: the list of links with elements that are scraped using XPATH selectors.
    """
    results = []
    loop = asyncio.get_event_loop()
    nest_asyncio.apply(loop)
    responses = loop.run_until_complete(
        _organize_tasks(loop, *list_of_links_and_configs)
    )
    for response in responses:
        results.append(response)
    return results


async def _organize_tasks(loop, *tuples_of_links_and_configs) -> list:
    """
    Take asyncio event loop and tuples of links and configs, \
    and organise asyncio.gather asynchronous activity.

    Args:
        loop: asyncio event loop.
        *tuples_of_links_and_configs: tuples of links to webpages with XPATH selectors \
        from params files.

    Returns:
        list: asyncio-controlled tasks using Future.
    """
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for tuple_of_link_and_config in tuples_of_links_and_configs:
            tasks.append(_scraper(session, tuple_of_link_and_config))
        return await asyncio.gather(*tasks)


async def _scraper(session, tuple_of_link_and_config: tuple) -> dict:
    """
    Using aiohttp session and tuple of links to webpages with XPATH selectors, scrape the webpage.

    Args:
        session: aiohttp session.
        tuple_of_link_and_config: link to the desired webpage with XPATH selectors to elements on it.
    Returns:
        dict: the dictionary with link to the webpage and XPATH-scraped values.
    """
    link, config = tuple_of_link_and_config
    html_string = await _get_html_string(session, link)
    html_tree = await _get_html_tree(html_string)
    result = await _find_elements(link, html_tree, config)
    return result


async def _get_html_string(session, link):
    """
    Get HTML string from the URL using aiohttp session.

    Args:
        session: aiohttp session.
        link: link to the desired webpage.
    """
    async with session.get(link) as response:
        return await response.text()


async def _get_html_tree(html_string: str):
    """
    Get a HTML tree from a HTML string.

    Args:
        html_string: HTML contents of the webpage represented as a string.
    Returns:
        html_tree: HTML tree of the webpage.
    """
    return html.fromstring(html_string)


async def _find_elements(link: str, html_tree, conf: dict) -> dict:
    """
    Find elements with XPATH selectors on the webpage.

    Args:
        link: the link to the desired webpage.
        html_tree: HTML tree of the webpage.
        conf: keys and XPATH selectors to run scraping against.
    Returns:
        dict: the dictionary of links with values that are scraped using XPATH selectors.
    """
    result = {"service_name": conf["service_name"], "link": link}
    service_name = conf.pop("service_name", None)
    for field in conf:
        xpath_or_with_endpoint = conf[field]
        if isinstance(xpath_or_with_endpoint, dict):
            ((endpoint, xpath),) = xpath_or_with_endpoint.items()
        else:
            xpath = xpath_or_with_endpoint
            endpoint = None
        scraped = html_tree.xpath(xpath)
        if not scraped:
            continue
        try:
            scraped = list(map(lambda x: x.text, scraped))
        except AttributeError:
            scraped = list(scraped)
        for i, scraped_item in enumerate(scraped):
            scraped[i] = scraped_item if endpoint is None else endpoint + scraped_item
        if len(scraped) == 1:
            scraped = scraped[0]
        result[field] = scraped
    conf["service_name"] = service_name
    return result


if __name__ == "__main__":
    from app.backend.scraping.google_search._google_mining import mining
    from app.backend.scraping.google_search._google_filter import filtering

    findings = mining("pythad")
    filtered = filtering(findings)
    print(scraping(filtered))
