import urllib.request
from zipfile import ZipFile 

print("Downloading movie metadata")
url = "https://www.kaggle.com/rounakbanik/the-movies-dataset/download/"
filename, _ = urllib.request.urlretrieve(url)
print(filename)

with ZipFile(filename, 'r') as zip:
    print("Extracting files in ./src/web/data")
    zip.extractall(path="./src/web/data")