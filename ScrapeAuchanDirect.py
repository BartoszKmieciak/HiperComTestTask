import requests
from lxml import html


def scrape_from_auchan_direct(product_name):
    product_name = str(product_name)

    page_content = requests.get('https://www.auchandirect.pl/auchan-warszawa/pl/search?text='
                                + product_name.replace(' ', '+'))
    html_tree = html.fromstring(page_content.content)

    products_data = []

    products_list_html_object = html_tree.xpath('//*[@id="search-product-list"]')
    # If no products were found, return empty list.
    if not products_list_html_object:
        return products_data
    else:
        products_list = products_list_html_object[0]

    for product in products_list:
        if product.tag == 'article':
            product_data = {}

            product_data['title'] = product.xpath('div/div/a/strong/text()')[0] + product.xpath('div/div/a/text()')[1]
            product_data['price'] = float(product.xpath('div/div/aside[2]/p/span[1]/text()')[0]
                                          + '.' + product.xpath('div/div/aside[2]/p/span[2]/text()')[0])
            product_data['price_currency'] = product.xpath('div/div/aside[2]/p/span[3]/text()')[0]
            product_data['packaging'] = product.xpath('div/div/p/strong/text()')[0]
            product_data['image'] = 'https://www.auchandirect.pl' \
                                    + product.xpath('div/a/span/div/img')[0].attrib['data-src']

            products_data.append(product_data)

    return products_data


auchan_direct_pepsi_cola = scrape_from_auchan_direct('pepsi cola')








