import praw
import configparser
from datetime import datetime, date
from time import sleep

config = configparser.ConfigParser()
config.read('praw.ini')

reddit = praw.Reddit(client_id=config['DEFAULT']['client_id'],
                     client_secret=config['DEFAULT']['client_secret'],
                     user_agent=config['DEFAULT']['user_agent'],
                     username=config['DEFAULT']['username'],
                     password=config['DEFAULT']['password'])

## The subreddit that we will be scraping posts from
subreddit = reddit.subreddit('rateme')

submissions_id = []
comments_by_id = []
comment_content = []
rating = []
commented = False
ind = 0

## Append each post id to a list
for submissions in subreddit.hot(limit=10):
    submissions_id.append(submissions)

## This will go through each post and comment the ugly level
while ind != 10:
    ## Get the comment ids from the latest submission
    comment_ids = submissions_id[ind].comments

    ## GET DATETIME FOR POST AND FOR TODAYS DATE ##
    time_of_post = submissions_id[ind].created_utc
    today = date.today()
    day_of_post = datetime.utcfromtimestamp(time_of_post).strftime("%d")
    current_day = today.strftime("%d")
    ## IF today is past the post's date ##
    if int(current_day) >= int(day_of_post):

        ## Append comment ids to a different list
        comments_by_id = [comment for comment in comment_ids]

        ## append comment contents to a list
        comment_content = [comment.body for comment in comments_by_id]

        ## check comment content if it has a rating, if it does append the rating
        for content in comment_content:
            if "1/10" in content:
                rating.append(1)
            elif "4.5/10" in content:
                rating.append(5)
            elif "5.5/10" in content:
                rating.append(6)
            elif "6.5/10" in content:
                rating.append(7)
            elif "7.5/10" in content:
                rating.append(8)
            elif "8.5/10" in content:
                rating.append(9)
            elif "9.5/10" in content:
                rating.append(10)
            elif "2/10" in content:
                rating.append(2)
            elif "3/10" in content:
                rating.append(3)
            elif "4/10" in content:
                rating.append(4)
            elif "5/10" in content:
                rating.append(5)
            elif "6/10" in content:
                rating.append(6)
            elif "7/10" in content:
                rating.append(7)
            elif "8/10" in content:
                rating.append(8)
            elif "9/10" in content:
                rating.append(9)
            elif "10/10" in content:
                rating.append(10)

            ## If we already commented on this post
            if "OVERALL RATING:" in content:
                commented = True

        ## Get the sum of rating and divide by len of list to get the mean
        rate_sum = sum(rating)
        rate_len = len(rating)
        total_rating = rate_sum / rate_len

        if commented == False:
            ## Try to comment on the post, if not possible then it means reddit isnt letting us
            try:
                submissions_id[ind].reply("**OVERALL RATING:** {}/10".format(total_rating))
                ## RESET THE VALUES
                del comments_by_id[:]
                del comment_content[:]
                del rating[:]
                ind += 1
            except:
                print("\nOOPS I'M POSTING TOO OFTEN WAITING 10MINS\n")
                sleep(600)
        else:
            print("ALREADY EVALUATED THIS POST: {}".format(submissions_id[ind].title))
            ## RESET THE VALUES
            del comments_by_id[:]
            del comment_content[:]
            del rating[:]
            commented = False
            ind += 1

    else:
        print("Current Day: {}, Day of Post: {}".format(int(current_day), int(day_of_post)))
        print("THAT POST IS TOO RECENT!\n")
        ind += 1
