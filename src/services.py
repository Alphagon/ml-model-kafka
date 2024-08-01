from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import load_model


#Parameters
max_len = 100
max_features = 10000

word_to_index = imdb.get_word_index()
model = load_model("model/sentiment-model.h5")

def preprocess_review(review, word_to_index, max_len, max_features):
    tokenizer = Tokenizer(num_words=max_features)
    tokenizer.word_index = word_to_index
    sequences = tokenizer.texts_to_sequences([review])
    padded_sequence = sequence.pad_sequences(sequences, maxlen=max_len)
    return padded_sequence

def make_predictions(review):
    preprocessed_review = preprocess_review(review, word_to_index, max_len, max_features)
    prediction = model.predict(preprocessed_review)
    probability = prediction[0][0]
    predicted_label = (prediction > 0.5).astype("int32")
    sentiment = 'positive' if predicted_label[0][0] == 1 else 'negative'
    result = {"Sentiment": sentiment, "Probability": float(probability)}
    return result