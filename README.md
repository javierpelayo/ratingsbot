# RATINGS BOT #

This bot scrapes a subreddits posts, then scrapes the posts comments and looks for ratings. Once those ratings are found they are appended to a list where we can get the average rating from.

The bot currently takes the "hot" top 10 posts but this limit can be adjusted. From there it iterates through the 10 posts looking to see whether it already commented, if not then it comments the posts overall rating.

The day of the post is also taken into account, if the post is older or equal to todays date than it will comment on it. I originally wanted to make it so it wouldn't comment on a post if it was less than a day old since there would not be many comments but this can also be adjusted.

If you wish to use configparser simply make a praw.ini file and create the file structure such as:

[DEFAULT]  
client_id = 123  
client_secret = 123  
user_agent = example.ratingsbot.v1.2.3 (by /u/example)  
username = example  
password = 123456  

app.py should read from it with no problems so long as you don't put parenthesis around the information.
