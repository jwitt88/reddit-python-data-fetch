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

    results = reddit.subreddit(target_sub).search(target_search, sort='new', limit=request_count)
    print("\n  DATE\t\t\t THREAD TITLE")

    for post in results:
        submission_time = convert_from_utc(post.created_utc)
        print(" ", submission_time, "\t", post.title[:45], "(...)")

        post_data = f"{post.id}, {submission_time}, {post.title}"
        push_list.append(post_data)


def write_to_file(stuff_to_send):
    """Writing fetched data to a csv file."""

    try:
        with open(file_name, 'r+') as f:
            existing_contents = f.read()
            for item in stuff_to_send:
                if item not in existing_contents:
                    f.write(f"{item} \n")

            print(f"\n  (!) Updating {file_name} w/ fetched content. (!)\n")

    except FileNotFoundError:
        with open(file_name, 'w') as f:
            f.write(f"Post ID, Post Date, Post Title \n")
            for item in stuff_to_send:
                f.write(f"{item} \n")

            print(f"\n  (~) {file_name} not found - writing w/ fetched content. (~)\n")


def convert_from_utc(utc_time):
    """Convert from unix to standard time."""

    fixed_time = time.strftime("%D %H:%M", time.localtime(int(utc_time)))
    return fixed_time

reddit_scrape(target_sub, target_search, request_count)
write_to_file(push_list)
