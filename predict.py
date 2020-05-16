from joblib import load
from preprocess import prep_data
import time
import os

def predict(s):
    return len(s.split(' '))

def predict_e(s):
    model = load(os.path.join("individual work","clf_is_Extrovert.joblib"))
    X = prep_data(s)
    return model.predict(X)

if __name__ == "__main__":
    t = time.time()
    string = "I just wanna to go home!!!!!! :sadpanda: https://www.youtube.com/watch?v=TQP20LTI84A"
    print(string)
    print(predict_e(string))
    print(f"Preprocessing Time: {time.time() - t} seconds")