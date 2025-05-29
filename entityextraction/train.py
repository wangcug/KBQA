from entityextraction.data import load_data, sent2label
from entityextraction.crf import CRFmodel
import pickle


def train_model():
    # Load training data
    training_data = load_data('./train.txt')
    print(training_data)

    # Extract label lists from training data
    label_lists = [sent2label(sent) for sent in training_data]

    # Initialize the CRF model
    crf_model = CRFmodel()

    # Train the CRF model
    crf_model.train(training_data, label_lists)

    # Save the trained model
    save_model(crf_model, './model/crf_c2.pkl')


def save_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)


def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model
