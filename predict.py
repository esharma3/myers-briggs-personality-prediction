from joblib import load
from preprocess import prep_data
import time
import os

def predict_e(s):

    X = prep_data(s)

    # loading the 4 models
    EorI_model = load(os.path.join("models","clf_is_Extrovert.joblib"))
    SorN_model = load(os.path.join("models","clf_is_Sensing.joblib"))
    TorF_model = load(os.path.join("models","clf_is_Thinking.joblib"))
    JorP_model = load(os.path.join("models","clf_is_Judging.joblib"))

    # predicting
    EorI_pred = EorI_model.predict(X)
    SorN_pred = SorN_model.predict(X)
    TorF_pred = TorF_model.predict(X)
    JorP_pred = JorP_model.predict(X)

    # combining the predictions from the 4 models
    result = combine_classes(EorI_pred, SorN_pred, TorF_pred, JorP_pred)

    return result

if __name__ == "__main__":
    t = time.time()
    string = "I just wanna to go home!!!!!! :sadpanda: https://www.youtube.com/watch?v=TQP20LTI84A"
    print(string)
    print(predict_e(string))
    print(f"Preprocessing Time: {time.time() - t} seconds")