# 綾鷹を選ばせるプログラム

from keras import models
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import os
import requests
from PIL import Image
import io
# 保存したモデルの読み込み
model = model_from_json(open('./all_card_predict.json').read())
# 保存した重みの読み込み
model.load_weights('./all_card_predict.hdf5')

root_dir = './cards_for_learning'
CATEGORIES = os.listdir(f'./{root_dir}')
print(CATEGORIES)

# 画像を読み込む
url = 'https://wing-auctions.c.yimg.jp/sim?furl=auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0107/users/12d09f48eae5ea992f27b2785dfb81c4c9bfa561/i-img500x500-1595768226pimjhb1371076.gif&dc=1&sr.fs=20000'
img = Image.open(io.BytesIO(requests.get(
    'https://wing-auctions.c.yimg.jp/sim?furl=auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0108/users/0fd774ce7e41e5dea219a368b51ec5dbb557bc69/i-img1200x1200-1596632932rae7eq2013897.jpg&dc=1&sr.fs=20000').content))
img = img.resize((250, 250))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

# 予測
features = model.predict(x)

# 予測結果によって処理を分ける
print(features[0])
print(CATEGORIES[features[0].argmax()])

'''
if features[0,0] == 1:
    print ('yamucha')
elif features[0,1] == 1:
    print ('badakku')
elif features[0,2] == 1:
    print ('songoku')
elif features[0,3] == 1:
    print ('bejita')
else:
    print('???')
'''
