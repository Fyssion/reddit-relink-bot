import praw

reddit = praw.Reddit(client_id='fRymMJayGXty1g',
                     client_secret='xMt_lwbyy6tMDyYyWZ47zdeyVPY',
                     user_agent='my user agent')

print(reddit.read_only)  # Output: True
'''
subreddit = reddit.subreddit('redditdev')
print("Subreddit:")
print("r/" + subreddit.display_name)  # Output: redditdev
print("Title:")
print(subreddit.title)         # Output: reddit Development
print("Description:")
print(subreddit.description)   # Output: A subreddit for discussion of ... 
'''

sub = input("Type subreddit here: ")
subreddit_search = reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=False)
print(subreddit_search)
if sub in subreddit_search:
    print("success")
'''
subreddit = reddit.subreddit(subreddit_search)
print("Subreddit:")
print("r/" + subreddit.display_name)  # Output: redditdev
print("Title:")
print(subreddit.title)         # Output: reddit Development
print("Description:")
print(subreddit.description)   # Output: A subreddit for discussion of ... 
'''
