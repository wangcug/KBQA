# ------------------------------
# 作者：23668
# 日期：2023年04月30日
# ------------------------------
from sklearn_crfsuite import CRF
from entityextraction.data import sent2feature
import pickle


class CRFmodel(object):
    def __init__(self,
                 algorithm='lbfgs',
                 c1=0.25,
                 c2=0.018,
                 max_iterations=200,
                 all_possible_transitions=True,
                 verbose=True):
        self.model = CRF(
            algorithm=algorithm,
            c1=c1,
            c2=c2,
            max_iterations=max_iterations,
            all_possible_transitions=all_possible_transitions,
            verbose=verbose
        )

    def train(self, sentences, labellists):
        feature = [sent2feature(sent) for sent in sentences]
        self.model.fit(feature, labellists)

    def predict(self, sentences):
        features = [sent2feature(s) for s in sentences]
        labellist = self.model.predict(features)
        return labellist

    def test(self, sentences):
        features = [sent2feature(s) for s in sentences]
        pred_tag_lists = self.model.predict(features)
        return pred_tag_lists


def save_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)


def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model
