import argparse
import json
import logging
from typing import List, Dict, Tuple, Optional

import requests
from bs4 import BeautifulSoup, Tag

from consts import CAR_BRANDS, BRAND_CODE, BRAND_TYPES
from url_creator import URLCreator, Country


def get(url: str) -> str:
    """
    Call requests get method with given URL and hardcoded headers

    :param url: URL to call get request
    :return: String with page content
    """
    response = requests.get(
        url,
        headers={
            'authority': 'suchen.mobile.de',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'referer': url,
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
    )
    return response.text


def get_ads_urls(url: str) -> List[str]:
    """
    Extracts URLs to car's ads from search page

    :param url: URL to page with search results
    :return: List of extracted urls
    """
    content = get(url)
    soup = BeautifulSoup(content, features="html.parser")
    results = soup.findAll('a', class_="link--muted no--text--decoration result-item")
    return [ad_url.attrs['href'] for ad_url in results if 'suchen.mobile.de' in ad_url.attrs['href']]


def extract_max_page_number(url: str) -> int:
    """
    Extract number of pages with search results

    :param url: URL to main page with search's results
    :return:
    """
    content = get(url)
    soup = BeautifulSoup(content, features="html.parser")
    tmp = soup.find_all('span', {'class': 'btn btn--muted btn--s'})
    values = [int(value.text) for value in tmp]
    if values:
        return max(values)
    return 1


def search_urls(url: str) -> List[str]:
    """
    Iterate across pages with search results and extract ad's urls

    :param url: URL to page with search results (without page selection)
    :return: List of URLs to car's ads
    """
    urls = []
    n = extract_max_page_number(url)

    for page_n in range(1, n+1):
        page_url = url + f'&pageNumber={page_n}'
        tmp_urls = get_ads_urls(page_url)

        if len(tmp_urls) == 0:
            logging.warning(f'No URLs found under {page_url}. You may be blocked!')

        urls += tmp_urls

    return urls


def extract_single_value(features_tag: Tag) -> Tuple[str, str]:
    """
    Extract single value from structured form of tag (like technical features)

    :param features_tag: Tag with structured form of data
    :return: Tuple of name and value
    """
    res = features_tag.find_all('div', class_='g-col-6')
    name = res[0].text
    value = res[1].text
    return name, value


def extract_technical_data(technical_data: Tag) -> Dict[str, str]:
    """
    Extract car's technical data (common structure across different ads)

    :param technical_data: Tag with div g-col-6 vip-price-rating__tech-details class
    :return: Dict with technical data key words and values
    """
    results = {}
    price_results = technical_data.find_all('div', class_='g-col-6 vip-price-rating__tech-details')

    if len(price_results) == 1:
        price = technical_data \
            .find_all('div', class_='g-col-6 vip-price-rating__tech-details')[0] \
            .text.split('€')[0] \
            .rstrip()
        results['price'] = price

    else:
        logging.warning('Price was not identified')

    rest_info = technical_data.find_all('div', class_='g-row u-margin-bottom-9')
    for tag in rest_info:
        name, value = extract_single_value(tag)
        results[name] = value

    return results


def extract_rbt_features(rbt_features: Tag) -> List[str]:
    """
    Extract rbt features from provided tag

    :param rbt_features: Tag with div g-col-6 class
    :return: List of car's features
    """
    results = []
    for tag in rbt_features.find_all('div', {'class': 'g-col-6'}):
        results.append(tag.text)

    return results


def save_scraped_results(results):
    with open(f'ad_{results["id"]}.json', 'w+') as file:
        json.dump(results, file)


def scrape_car(url: str) -> Optional[Dict]:
    """
    Scrape info about car from provided url

    :param url: URL with mobile.de ad
    :return: Bool if ad was successfully scraped
    """
    content = get(url)
    soup = BeautifulSoup(content, features="html.parser")
    technical_data = soup.find('div', class_='cBox-body cBox-body--technical-data')
    rbt_features = soup.find('div', {"id": "rbt-features"})

    if not technical_data and not rbt_features:
        return None

    ad_title = soup.find('h1', {'id': 'rbt-ad-title'}).text

    loc = soup.find('p', {'id': 'rbt-seller-address'}).text

    if technical_data:
        technical_data = extract_technical_data(technical_data)

    if rbt_features:
        rbt_features = extract_rbt_features(rbt_features)

    ad_id = url.split('id=')[1].split('&')[0]
    results = {
        'id': ad_id,
        'title': ad_title,
        'rbt_features': rbt_features,
        'technical_data': technical_data,
        'loc': loc
    }
    return results


def extract_unique_ads(urls: List[str]) -> List[str]:
    """
    Extract unique urls (sometimes duplicated ad's urls can be attached)

    :param urls: List of scraped ad's links
    :return: List of unique ad's links
    """
    ids = set([url.split('id=')[1].split('&')[0] for url in urls])

    results = []
    for ad_id in ids:
        results.append(list(filter(lambda url: ad_id in url, urls))[0])

    return results


def main():
    parser = argparse.ArgumentParser(description='Scrape car ads from mobile.de service')
    parser.add_argument(
        '--car-brand',
        help="Lowercase car's brand name ex. audi, opel",
        type=str,
        required=True
    )
    parser.add_argument(
        '--car-type',
        help="Lowercase car's brand name ex. a1, astra",
        type=str,
        required=True
    )
    parser.add_argument(
        '--seller-type',
        help="Type of seller - private/seller/company",
        type=str
    )
    parser.add_argument(
        '--base-url',
        help="Base search URL to which code will add expected filters",
        type=str
    )
    parser.add_argument(
        '--min-price',
        help="Min price in Euro",
        type=int
    )
    parser.add_argument(
        '--min-horse-power',
        help="Min horse power",
        type=int
    )
    parser.add_argument(
        '--max-horse-power',
        help="Max horse power",
        type=int
    )
    parser.add_argument(
        '--min-first-registration',
        help="Min value of first registration year",
        type=int
    )
    parser.add_argument(
        '--max-first-registration',
        help="Max value of first registration year",
        type=int
    )
    parser.add_argument(
        '--min-mileage',
        help="Min mileage in km",
        type=int
    )
    parser.add_argument(
        '--max-mileage',
        help="Max mileage in km",
        type=int
    )
    args = parser.parse_args()

    search_pages_urls = URLCreator().get_search_page_links(
        car_brand=CAR_BRANDS[args.car_brand][BRAND_CODE],
        car_type=CAR_BRANDS[args.car_brand][BRAND_TYPES][args.car_type],
        min_price=args.min_price,
        max_price=args.max_price,
        base_url=args.base_url,
        seller_type=args.seller_type,
        country=args.country,
        min_horse_power=args.min_horse_power,
        max_horse_power=args.max_horse_power,
        max_first_registration=args.max_first_registration,
        min_first_registration=args.min_first_registration,
        min_mileage=args.min_mileage,
        max_mileage=args.max_mileage,
    )

    ads_urls = []
    for url in search_pages_urls:
        ads_urls += search_urls(url)

    ads_urls = extract_unique_ads(ads_urls)

    urls_number = len(ads_urls)
    for n, link in enumerate(ads_urls):
        scraped_ad = scrape_car(link)
        if scraped_ad:
            save_scraped_results(scraped_ad)
        logging.info(f'Completed {round(n/urls_number)}%')


if __name__ == '__main__':
    main()

