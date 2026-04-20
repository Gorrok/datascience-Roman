# -*- coding: utf-8 -*-

SOURCES = {
    'rybalkashop.ru': {
        'base_url': 'https://rybalkashop.ru',
        'categories': {
            'vobler': 'https://rybalkashop.ru/shop/category?id=8373',
            'blesna': 'https://rybalkashop.ru/shop/category?id=8360',
        },
        'selectors': {
            'category_links': 'div.product-card__info > a',
            'title': 'h1.product-title',
            'brand_row_dt': 'dl.product-chars__list-item dt',
            'brand_row_dd': 'dl.product-chars__list-item dd',
            'brand_keyword': 'бренд',
            'description': 'div.product-description'
        }
    },
    'rybachek.com.ua': {
        'base_url': 'https://rybachek.com.ua',
        'categories': {
            'vobler': 'https://rybachek.com.ua/c/primanki/voblery/',
            'blesna': 'https://rybachek.com.ua/c/primanki/blesny/',
            'silikon': 'https://rybachek.com.ua/c/primanki/silikon/'
        },
        'selectors': {
            'category_links': 'a.product-card__name',
            'title': 'h1.product__title',
            'brand_row_dt': 'div.properties__item-name',
            'brand_row_dd': 'div.properties__item-value',
            'brand_keyword': 'производитель',
            'description': 'div.product-description__content'
        }
    },
    'spinningline.ru': {
        'base_url': 'https://spinningline.ru',
        'categories': {
            'vobler': 'https://spinningline.ru/voblery-c-3_1185.html',
            'blesna': 'https://spinningline.ru/blesny-c-3_8.html',
            'silikon': 'https://spinningline.ru/myagkie-primanki-c-3_9.html'
        },
        'selectors': {
            'category_links': 'a.b-product-gallery__title',
            'title': 'h1[itemprop="name"]',
            'brand_row_dt': 'div.b-product-params__name',
            'brand_row_dd': 'div.b-product-params__value',
            'brand_keyword': 'производитель',
            'description': 'div[itemprop="description"]'
        }
    }
}
