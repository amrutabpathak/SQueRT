import requests
import os.path
import os

def getModels():
    url_Albert_bin = 'https://s3.amazonaws.com/models.huggingface.co/bert/ktrapeznikov/albert-xlarge-v2-squad-v2/pytorch_model.bin'
    albert_model_path = os.path.join(os.getcwd(), "Albert Question Answering/")
    albert_model_model_path = os.path.join(albert_model_path, "pytorch_model.bin")
    if albert_model_model_path:
        print("File is already downloaded skipping")
    else:
        print("Albert is downloading...")
        r = requests.get(url_Albert_bin, allow_redirects=True)
        print("Albert is writing to file...")
        open(albert_model_model_path, 'wb').write(r.content)
        print("Albert is finished downloading!")

