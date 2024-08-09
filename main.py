import tkinter as tk
from tkinter import messagebox

class Tweet:
    def __init__(self, content):
        self.content = content
        self.likes = 0

class TwitterCloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter Clone")
        self.tweets = []

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        self.input_tweet = tk.Text(self.input_frame, height=3, width=50)
        self.input_tweet.pack(side=tk.LEFT, padx=5)

        self.post_button = tk.Button(self.input_frame, text="Post Tweet", command=self.post_tweet)
        self.post_button.pack(side=tk.LEFT, padx=5)

        self.tweet_list_frame = tk.Frame(root)
        self.tweet_list_frame.pack()

        self.tweet_list = tk.Listbox(self.tweet_list_frame, width=70, height=15)
        self.tweet_list.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(root, text="Like Tweet", command=self.like_tweet)
        self.like_button.pack(pady=10)

    def post_tweet(self):
        content = self.input_tweet.get("1.0", tk.END).strip()
        if content:
            tweet = Tweet(content=content)
            self.tweets.append(tweet)
            self.update_tweet_list()
            self.input_tweet.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Empty Tweet", "Please enter some content to tweet.")

    def update_tweet_list(self):
        self.tweet_list.delete(0, tk.END)
        for tweet in self.tweets:
            self.tweet_list.insert(tk.END, f"{tweet.content}\nLikes: {tweet.likes}")

    def like_tweet(self):
        selected_tweet_index = self.tweet_list.curselection()
        if selected_tweet_index:
            index = selected_tweet_index[0]
            self.tweets[index].likes += 1
            self.update_tweet_list()
        else:
            messagebox.showwarning("No Selection", "Please select a tweet to like.")

if __name__ == '__main__':
    root = tk.Tk()
    app = TwitterCloneApp(root)
    root.mainloop()
