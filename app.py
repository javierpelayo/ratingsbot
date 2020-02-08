import praw
import configparser
from datetime import datetime, date
from time import sleep
from tkinter import *

root = Tk()
root.title("Ratings Bot")


config = configparser.ConfigParser()
config.read('praw.ini')

reddit = praw.Reddit(client_id=config['DEFAULT']['client_id'],
                     client_secret=config['DEFAULT']['client_secret'],
                     user_agent=config['DEFAULT']['user_agent'],
                     username=config['DEFAULT']['username'],
                     password=config['DEFAULT']['password'])

# The subreddit that we will be scraping posts from
subreddit = reddit.subreddit('rateme')


def done(frame, comments):
    doneFrame = Frame(root)
    doneFrame.grid()
    postLabel = Label(doneFrame, text="Commented On: ")
    numberLabel = Label(doneFrame, text=str(comments))
    back = Button(doneFrame, text="Back",command=lambda: (doneFrame.destroy(), main()))
    postLabel.grid(column=0, row=0)
    numberLabel.grid(column=1, row=0)
    back.grid(columnspan=3, row=1)
    frame.destroy()


def inProgress(posts, frame):

    submissions_id = []
    comments_by_id = []
    comment_content = []
    rating = []
    commented = False
    comments = 0
    ind = 0

    # Append each post id to a list
    for submissions in subreddit.hot(limit=int(posts)):
        submissions_id.append(submissions)

    # This will go through each post and comment the rating
    while ind < int(posts):
        # Get the comment ids from the latest submission
        comment_ids = submissions_id[ind].comments

        # GET DATETIME FOR POST AND FOR TODAYS DATE
        time_of_post = submissions_id[ind].created_utc
        today = date.today()
        day_of_post = datetime.utcfromtimestamp(time_of_post).strftime("%d")
        current_day = today.strftime("%d")
        # If today is past the post's date
        if int(current_day) >= int(day_of_post):

            # Append comment ids to a different list
            comments_by_id = [comment for comment in comment_ids]

            # append comment contents to a list
            comment_content = [comment.body for comment in comments_by_id]

            # check comment content if it has a rating,
            # if it does append the rating
            for content in comment_content:
                for num in range(11):
                    if (str(num) + "/10") in content:
                        rating.append(num)

                # If we already commented on this post
                if "OVERALL RATING:" in content:
                    commented = True

            # Get the sum of rating and divide by len of list to get the mean
            rate_sum = sum(rating)
            rate_len = len(rating)
            try:
                total_rating = rate_sum / rate_len
            except ZeroDivisionError:
                total_rating = 5
            if commented is False:
                # Try to comment on the post,
                # if not possible then it means
                # reddit isnt letting us
                try:
                    submissions_id[ind].reply("**OVERALL RATING:** {0:.1g}/10".format(total_rating))
                    # RESET THE VALUES
                    del comments_by_id[:]
                    del comment_content[:]
                    del rating[:]
                    ind += 1
                    comments += 1
                except praw.exceptions.APIException:
                    print("\nOOPS I'M POSTING TOO OFTEN WAITING 10MINS\n")
                    sleep(600)
            else:
                print("ALREADY EVALUATED THIS POST: {}".format(submissions_id[ind].title))
                # RESET THE VALUES
                del comments_by_id[:]
                del comment_content[:]
                del rating[:]
                commented = False
                ind += 1

        else:
            print("Current Day: {}, Day of Post: {}".format(int(current_day), int(day_of_post)))
            print("THAT POST IS TOO RECENT!\n")
            ind += 1

    done(frame, comments)


def main():
    mainFrame = Frame(root)
    mainFrame.grid()
    subLabel = Label(mainFrame, text="Sub: r/rateme")
    postLabel = Label(mainFrame, text="Posts")
    postEntry = Entry(mainFrame)
    start = Button(mainFrame, text="Start",command=lambda: inProgress(postEntry.get(), mainFrame))
    subLabel.grid(columnspan=3, row=0)
    postLabel.grid(column=0, row=1)
    postEntry.grid(column=1, row=1, columnspan=2)
    start.grid(columnspan=3, row=2)


if __name__ == "__main__":
    main()
    root.mainloop()
