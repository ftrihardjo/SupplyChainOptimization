import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QFormLayout, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

class Tweet:
    def __init__(self, content, likes=0):
        self.content = content
        self.likes = likes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitter Clone")
        self.setGeometry(100, 100, 400, 600)

        self.tweets = []

        # Set up the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Form for posting a tweet
        self.formLayout = QFormLayout()
        self.tweetInput = QTextEdit()
        self.postButton = QPushButton("Post Tweet")
        self.postButton.clicked.connect(self.post_tweet)

        self.formLayout.addRow("What's happening?", self.tweetInput)
        self.formLayout.addWidget(self.postButton)

        # List to display tweets
        self.tweetList = QListWidget()

        # Add form layout and tweet list to the main layout
        self.layout.addLayout(self.formLayout)
        self.layout.addWidget(self.tweetList)

    def post_tweet(self):
        content = self.tweetInput.toPlainText().strip()
        if content:
            tweet = Tweet(content)
            self.tweets.append(tweet)
            self.display_tweets()
            self.tweetInput.clear()
        else:
            QMessageBox.warning(self, "Empty Tweet", "Please enter some content to tweet.")

    def display_tweets(self):
        self.tweetList.clear()
        for tweet in self.tweets:
            item = QListWidgetItem(f"{tweet.content}\nLikes: {tweet.likes}")
            item.setTextAlignment(Qt.AlignLeft)
            item.setData(Qt.UserRole, tweet)
            self.tweetList.addItem(item)
            likeButton = QPushButton("Like")
            likeButton.clicked.connect(lambda _, t=tweet: self.like_tweet(t))
            self.tweetList.setItemWidget(item, likeButton)

    def like_tweet(self, tweet):
        tweet.likes += 1
        self.display_tweets()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
