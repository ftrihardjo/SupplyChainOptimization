from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, NumericProperty

class Tweet(BoxLayout):
    content = StringProperty()
    likes = NumericProperty(0)

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def like_tweet(self):
        self.likes += 1

class TwitterCloneApp(App):
    def build(self):
        self.tweets = []

        layout = BoxLayout(orientation='vertical')

        self.input_tweet = TextInput(hint_text="What's happening?", size_hint_y=None, height=100)
        layout.add_widget(self.input_tweet)

        post_button = Button(text="Post Tweet", size_hint_y=None, height=50)
        post_button.bind(on_press=self.post_tweet)
        layout.add_widget(post_button)

        self.tweet_container = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tweet_container.bind(minimum_height=self.tweet_container.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.tweet_container)
        layout.add_widget(scroll_view)

        return layout

    def post_tweet(self, instance):
        content = self.input_tweet.text.strip()
        if content:
            tweet = Tweet(content=content)
            self.tweet_container.add_widget(tweet)
            self.input_tweet.text = ''
        else:
            pass  # In a real app, you would show an error message here.

class Tweet(BoxLayout):
    content = StringProperty()
    likes = NumericProperty(0)

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def like_tweet(self):
        self.likes += 1

class TwitterCloneApp(App):
    def build(self):
        self.tweets = []

        layout = BoxLayout(orientation='vertical')

        self.input_tweet = TextInput(hint_text="What's happening?", size_hint_y=None, height=100)
        layout.add_widget(self.input_tweet)

        post_button = Button(text="Post Tweet", size_hint_y=None, height=50)
        post_button.bind(on_press=self.post_tweet)
        layout.add_widget(post_button)

        self.tweet_container = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tweet_container.bind(minimum_height=self.tweet_container.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.tweet_container)
        layout.add_widget(scroll_view)

        return layout

    def post_tweet(self, instance):
        content = self.input_tweet.text.strip()
        if content:
            tweet = Tweet(content=content)
            self.tweet_container.add_widget(tweet)
            self.input_tweet.text = ''
        else:
            pass  # In a real app, you would show an error message here.

if __name__ == '__main__':
    TwitterCloneApp().run()
