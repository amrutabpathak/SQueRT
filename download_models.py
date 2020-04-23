import requests
import os.path
import os

def getModels():
    url_Albert_bin = 'https://s3.amazonaws.com/models.huggingface.co/bert/ktrapeznikov/albert-xlarge-v2-squad-v2/pytorch_model.bin'
    albert_model_path = os.path.join(os.getcwd(), "albert_models/")
    albert_model_model_path = os.path.join(albert_model_path, "pytorch_model.bin")
    if os.path.exists(albert_model_model_path):
        pass
    else:
        print("Albert model is downloading to " + albert_model_path)
        r = requests.get(url_Albert_bin, allow_redirects=True)
        print("Albert is writing to file " + albert_model_model_path)
        open(albert_model_model_path, 'wb').write(r.content)
        print("Albert is finished downloading!")

