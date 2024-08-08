import PySimpleGUI as sg

class Tweet:
    def __init__(self, content):
        self.content = content
        self.likes = 0

def update_tweet_list(window, tweets):
    tweet_list = [f"{tweet.content}\nLikes: {tweet.likes}" for tweet in tweets]
    window['-TWEETLIST-'].update(tweet_list)

def main():
    sg.theme('DarkAmber')

    layout = [
        [sg.Text("What's happening?")],
        [sg.Multiline(size=(50, 3), key='-TWEETINPUT-')],
        [sg.Button('Post Tweet')],
        [sg.Listbox(values=[], size=(50, 10), key='-TWEETLIST-', enable_events=True)],
        [sg.Button('Like Tweet'), sg.Button('Exit')]
    ]

    window = sg.Window('Twitter Clone', layout)

    tweets = []

    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        if event == 'Post Tweet':
            content = values['-TWEETINPUT-'].strip()
            if content:
                tweet = Tweet(content)
                tweets.append(tweet)
                update_tweet_list(window, tweets)
                window['-TWEETINPUT-'].update('')
            else:
                sg.popup('Please enter some content to tweet.')

        if event == 'Like Tweet':
            selected_tweet = values['-TWEETLIST-']
            if selected_tweet:
                index = window['-TWEETLIST-'].get_indexes()[0]
                tweets[index].likes += 1
                update_tweet_list(window, tweets)
            else:
                sg.popup('Please select a tweet to like.')

    window.close()

if __name__ == '__main__':
    main()
