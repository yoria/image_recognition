import time
import requests
from bs4 import BeautifulSoup
import os
import glob
from PIL import Image
import json

JSON_ROOT_DIR = 'all_cards_infos'

rarity4_cards_path = f'./{JSON_ROOT_DIR}/rarity4_cards.json'
all_cards_json = open(rarity4_cards_path, 'r', encoding='utf-8')
all_cards = json.load(all_cards_json)

promotion_cards_path = f'./{JSON_ROOT_DIR}/promotion_cards.json'
promotion_cards_json = open(promotion_cards_path, 'r', encoding='utf-8')
promotion_cards = json.load(promotion_cards_json)

rarity3_cards_path = f'./{JSON_ROOT_DIR}/rarity3_cards.json'
rarity3_cards_json = open(rarity3_cards_path, 'r', encoding='utf-8')
rarity3_cards = json.load(rarity3_cards_json)

ALL_CARDS_DECT = {'4': all_cards, '3': rarity3_cards, 'P': promotion_cards}

RAKUMA_LAST_BUTTON_SELECTOR = "div.search_tab > div.hidden-xs > nav>span.last"
YAFUOKU_LAST_BUTTON_SELECTOR = "li.Pager__list.Pager__list--next > a"

ROOT_DIR = 'cards_for_management'

LEARNING_ROOT_DIR = 'cards_for_learning'


def download_file_easy(url, card_dir, img_id, flema_name):
    response = requests.get(url)
    image = response.content
    with open(f'{card_dir}/{flema_name}{str(img_id)}.jpg', 'wb') as aaa:
        aaa.write(image)


def update_resize_image(card_dir):
    files = glob.glob(card_dir + '/*.jpg')
    for f in files:
        '''
        try:
            img = Image.open(f)
            print(f)
            img_resize = img.resize((250, 250))
            title, ext = os.path.splitext(f)
            img_resize.save(title + ext)
        except Exception as e:
            print('error', f)
            print(e)
            os.remove(f)
        '''
        img = Image.open(f)
        print(f)
        img_resize = img.resize((250, 250))
        title, ext = os.path.splitext(f)
        img_resize.save(title + ext)


def add_sample_img(card_number, card_dir):
    card_number_for_url = card_number.replace(' ', '')
    sdbh_url = 'https://www.carddass.com/dbh/sdbh_bm/images/cardlist/dummys' \
        f'/{card_number_for_url}.png'
    response = requests.get(sdbh_url)
    image = response.content
    with open(f'{card_dir}/0sample.jpg', 'wb') as aaa:
        aaa.write(image)


def load_rakuma(card_name, card_number, card_dir):
    rakuma_current_page = 1
    rakuma_img_id = 0
    parameter = card_name+'%20'+card_number
    if not os.path.exists(card_dir):
        os.makedirs(card_dir)
        print(f'create {card_number} dir')
    while True:
        time.sleep(3)  # important
        rakuma = {}
        rakuma["url"] = f'https://fril.jp/search/ドラゴンボールヒーローズ%20{parameter}'\
            f'/page/{str(rakuma_current_page)}?order=desc&sort=relevance'
        rakuma["origin_data"] = requests.get(rakuma["url"])
        rakuma["soup"] = BeautifulSoup(
            rakuma["origin_data"].content, "html.parser")
        rakuma["products"] = rakuma["soup"].select("div.item")
        for product in rakuma["products"]:
            origin_image_url = product.select("img")
            image_url = origin_image_url[1].get("src")
            download_file_easy(image_url, card_dir, rakuma_img_id, 'r')
            rakuma_img_id += 1

        # nothing last button
        if rakuma["soup"].select(RAKUMA_LAST_BUTTON_SELECTOR) == []:
            break
        rakuma_current_page += 1
    print(f'rakuma {card_number} completed ({str(rakuma_current_page)}p)')


def load_yafuoku(card_name, card_number, card_dir):
    yafuoku_current_page = 1
    yafuoku_img_id = 0
    p_param = card_name+'+'+card_number
    if not os.path.exists(card_dir):
        os.makedirs(card_dir)
        print(f'create {card_number} dir')
    while True:
        time.sleep(3)  # important
        yafuoku = {}
        b_param = str(100*(yafuoku_current_page-1)+1)
        yafuoku["url"] = f'https://auctions.yahoo.co.jp/closedsearch/'\
            f'closedsearch?p={p_param}&va={p_param}&b={b_param}&n=100'
        yafuoku["origin_data"] = requests.get(yafuoku["url"])
        yafuoku["soup"] = BeautifulSoup(
            yafuoku["origin_data"].content, "html.parser")
        yafuoku["products"] = yafuoku["soup"].select("li.Product")
        for product in yafuoku["products"]:
            origin_image_url = product.select("img")
            image_url = origin_image_url[0].get("src")
            download_file_easy(image_url, card_dir, yafuoku_img_id, 'y')
            yafuoku_img_id += 1

        # disabled last button
        if yafuoku['soup'].select(YAFUOKU_LAST_BUTTON_SELECTOR) == []:
            break
        yafuoku_current_page += 1
    print(f'yafuoku {card_number} completed ({str(yafuoku_current_page)}p)')


def download_one_img(card_name, card_number, mission_name, rarity):
    card_dir = f'./{ROOT_DIR}/{mission_name}/{rarity}/{card_number} PR'
    load_rakuma(card_name, card_number, card_dir)
    load_yafuoku(card_name, card_number, card_dir)


for card_infos in all_cards['SDBH']['BM'][2]:
    card_dir = f'./cards_for_management/BM/{card_infos["id"]}'
    load_rakuma(card_infos["name"],
                card_infos["id"], card_dir)
    load_yafuoku(card_infos["name"],
                 card_infos["id"], card_dir)
    add_sample_img(card_infos["id"], card_dir)
    # update_resize_image(card_dir)
