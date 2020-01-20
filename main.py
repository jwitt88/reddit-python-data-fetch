from sys import argv
import time

import praw
import config


def query_reddit(target_sub, target_search, date_cutoff):
    """Fetches Reddit data with praw / config credentials."""

    results = reddit.subreddit(target_sub).search(\
    target_search, sort='new', limit=50)

    filter_results(results)

def filter_results(results):
    """Filters the results from query_reddit() and appends to push_list"""

    for post in results:

        if post.created_utc > date_cutoff:

            formatted_title = post.title.replace(',', '')
            print(f"  {post.id} | {formatted_title[:40]} (...)")

            '''
            TO DO:
            - Do something with the below list of comment ids.
            - Consider storing it in the same output, or make a new file:
                for comment in comment_ids:
                    print(comment.body) ...
            '''

            comment_ids = post.comments.list()
            comment_count = len(comment_ids)

            submission_time = convert_from_utc(post.created_utc)
            post_data = f"{post.id}, {post.score}, {comment_count}, {submission_time}, {formatted_title}"
            push_list.append(post_data)

        else:
            pass

def write_to_file(stuff_to_send):
    """Checking for existing files / data, and writing fetched content."""

    if push_list:

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

    else:
        print(f"  - \t\t - \n")
        print(f"  (X) No recent results found!\n")

def convert_from_utc(utc_time):
    """Convert from unix to standard time."""

    fixed_time = time.strftime("%D", time.localtime(int(utc_time)))
    return fixed_time


script, target_sub, target_search, days = argv

reddit = praw.Reddit(client_id=config.cid,
client_secret=config.cs, user_agent=config.ua)

current_time = time.time()
date_cutoff = current_time - int(days) * 86400

file_name = f"{target_sub}-{target_search}.csv"
push_list = []

print(f"\n  SUBREDDIT\n  r/{target_sub}")
print(f"\n  KEYWORD\n  '{target_search}'")
print(f"\n  DATE RANGE\n  < {days} day(s)")
print(f"\n  RESULTS: ")

query_reddit(target_sub, target_search, date_cutoff)
write_to_file(push_list)
