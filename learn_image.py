import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
import numpy as np
from keras.utils import np_utils
from keras import optimizers
from keras import layers, models
import os

root_dir = './cards_for_learning'
CATEGORIES = os.listdir(f'./{root_dir}')
NB_CLASSES = len(CATEGORIES)
EPOCHS = 50
# モデルの構築


model = models.Sequential()
model.add(
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(250, 250, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation="relu"))
model.add(layers.Dense(NB_CLASSES, activation="sigmoid"))

# モデル構成の確認
model.summary()

# モデルのコンパイル


model.compile(
    loss="binary_crossentropy",
    optimizer=optimizers.RMSprop(lr=1e-4),
    metrics=["acc"]
)

# データの準備


earlystopper = EarlyStopping(min_delta=0.01, patience=5)

X_train, X_test, y_train, y_test = np.load(
    "./all_card.npy", allow_pickle=True)

# データの正規化
X_train_split = np.array_split(X_train, 10)
X_train_split_index = 0
for one_X_train in X_train_split:
    one_X_train = one_X_train.astype("float32") / 255
    X_train_split_index += 1
    print(X_train_split_index)
X_train = np.concatenate(
    [X_train_split[0], X_train_split[1], X_train_split[2],
     X_train_split[3], X_train_split[4], X_train_split[5],
     X_train_split[6], X_train_split[7], X_train_split[8],
     X_train_split[9]])

X_test_split = np.array_split(X_test, 10)
X_test_split_index = 0
for one_X_test in X_test_split:
    one_X_test = one_X_test.astype("float32") / 255
    X_test_split_index += 1
    print(X_test_split_index)
X_test = np.concatenate(
    [X_test_split[0], X_test_split[1], X_test_split[2],
     X_test_split[3], X_test_split[4], X_test_split[5],
     X_test_split[6], X_test_split[7], X_test_split[8],
     X_test_split[9]])

# kerasで扱えるようにcategoriesをベクトルに変換
y_train = np_utils.to_categorical(y_train, NB_CLASSES)
y_test = np_utils.to_categorical(y_test, NB_CLASSES)
# model.layers.Conv2D.input_shape=(150,150,3)
print(len(X_train))
print(len(y_train))
# モデルの学習
model = model.fit(X_train, y_train, epochs=EPOCHS, validation_data=(
    X_test, y_test), callbacks=[earlystopper])

# 学習結果を表示


acc = model.history['acc']
val_acc = model.history['val_acc']
loss = model.history['loss']
val_loss = model.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.savefig('accuracy.jpg')

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.savefig('loss.jpg')

# モデルの保存

json_string = model.model.to_json()
open('./all_card_predict.json', 'w').write(json_string)  # only yamucha

# 重みの保存

hdf5_file = "./all_card_predict.hdf5"  # only yamucha
model.model.save_weights(hdf5_file)
