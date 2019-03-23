from textblob import TextBlob


class SentimentClassifier:
    def __init__(self, text):
        classified = TextBlob(text)
        self.polarity = 0
        for sentence in classified.sentences:
            self.polarity += sentence.sentiment.polarity