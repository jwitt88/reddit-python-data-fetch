from sys import argv
import time

import praw
import config

reddit = praw.Reddit(client_id=config.cid,
client_secret=config.cs, user_agent=config.ua)

script, target_sub, target_search, request_count = argv
request_count = int(request_count)

file_name = f"{target_sub}-{target_search}.csv"
push_list = []


def reddit_scrape(target_sub, target_search, request_count):
    """Fetching Reddit data with praw."""

    results = reddit.subreddit(target_sub).search(\
    target_search, sort='new', limit=request_count)
    print("\n  DATE\t\t\t THREAD TITLE")

    for post in results:

        submission_time = convert_from_utc(post.created_utc)
        formatted_title = post.title.replace(',', '')
        print(f"  {submission_time} \t {formatted_title[:40]} (...)")

        '''
        TO DO: do something with the below list of comment ids.
        Consider storing it in the same output, or make a new file.
        '''
        comment_ids = post.comments.list()
        comment_count = len(comment_ids)
        '''
        TO DO: add read/export support for individual comments:
        for comment in comment_ids:
            print(comment.body) ...
            '''

        post_data = f"{post.id}, {post.score}, {comment_count}, {submission_time}, {formatted_title}"
        push_list.append(post_data)


def write_to_file(stuff_to_send):
    """Checking for existing files / data, and writing fetched content."""

    try:
        with open(file_name, 'r+') as f:
            existing_contents = f.read()
            for item in stuff_to_send:

                """
                NOTE: Because the upvote scores change frequently,
                we only check for the presence of the first six
                characters of each line (the post ID) to avoid dupes.
                """
                if item[:6] not in existing_contents:
                    f.write(f"{item} \n")

            print(f"\n  (+) Updating {file_name} w/ fetched content.")
            print(f"      Write successfully completed.\n")

    except FileNotFoundError:
        with open(file_name, 'w') as f:
            f.write(f"Post ID, Score, Comments, Date, Title \n")
            for item in stuff_to_send:
                f.write(f"{item} \n")

            print(f"\n  (!) Creating {file_name} w/ fetched content.")
            print(f"      Write successfully completed.\n")

    except:
        print(f"  (X) Write failed - unexpected error!\n")


def convert_from_utc(utc_time):
    """Convert from unix to standard time."""

    fixed_time = time.strftime("%D %H:%M", time.localtime(int(utc_time)))
    return fixed_time


print(f"\n  SUBREDDIT\n  r/{target_sub}")
print(f"\n  KEYWORD\n  '{target_search}'")

reddit_scrape(target_sub, target_search, request_count)
write_to_file(push_list)
