from pytesseract import pytesseract
from PIL import Image
import cv2

# 読み込み対象ファイルの指定

img = cv2.imread('test2.png', 0)#画像読み込み
img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)#ノイズ処理
# tesseractコマンドのインストールパス
pytesseract.tesseract_cmd = "/usr/bin/tesseract"#tesseractの指定
# 文字列として出力できる。
ocr_result = pytesseract.image_to_string(img, lang="eng+jpn")#文字を抽出
print(ocr_result)