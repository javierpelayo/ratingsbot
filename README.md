# RATINGS BOT #

This simple bot scrapes a subreddits posts, then scrapes the posts comments and looks for ratings. Once those ratings are found they are appended to a list where we can get the average rating from.

The bot currently takes the "hot" top 10 posts from Reddit but this limit can be adjusted. From there it iterates through the 10 posts looking to see whether it already commented, if not then it comments the posts overall rating.

The day of the post is also taken into account, if the post is older or equal to todays date than it will comment on it.
