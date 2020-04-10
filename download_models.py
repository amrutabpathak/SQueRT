import requests
import os.path

def getModels():
    url_Albert_bin = 'https://s3.amazonaws.com/models.huggingface.co/bert/ktrapeznikov/albert-xlarge-v2-squad-v2/pytorch_model.bin'
    if os.path.isfile("./Albert Question Answering/pytorch_model.bin"):
        print("File is already downloaded skipping")
    else:
        print("Albert is downloading...")
        r = requests.get(url_Albert_bin, allow_redirects=True)
        print("Albert is writing to file...")
        open("./Albert Question Answering/pytorch_model.bin", 'wb').write(r.content)
        print("Albert is finished downloading!")

