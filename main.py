import time

import praw
import config #contains client_id, client_secret, and user_agent


def query_reddit(target_sub, target_search, target_count):
    """Fetches Reddit data with praw / config credentials."""

    try:
        results = reddit.subreddit(target_sub).search(\
        target_search, sort='new', limit=target_count)

    except:
        print(f"\n  (X) Authentication failed - check credentials!\n")

    else:
        print("\n  [POST]   [TITLE]")
        filter_results(results, target_search)

def filter_results(results, target_search):
    """Filters the results from query_reddit() and appends to push_list"""

    for post in results:

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
        post_data = f"{post.id},{target_search},{post.score},{comment_count},{submission_time},{formatted_title}"
        push_list.append(post_data)

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
                        f.write(f"{item}\n")

                print(f"\n  (+) Updating {file_name} w/ fetched content.")
                print(f"      Write successfully completed.\n")

        except FileNotFoundError:
            with open(file_name, 'w') as f:
                f.write(f"Post ID,Keyword,Score,Comments,Date,Title\n")
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


#params for querying with praw
sub_to_search = input("\n  > Subreddit: ")
terms_to_search = input("  > Search terms: ")
count_to_pull = int(input("  > Pull count: "))

#authentication with praw
reddit = praw.Reddit(client_id=config.cid,
client_secret=config.cs, user_agent=config.ua)

#used in time conversion from unix
current_time = time.time()

#file name for export and push list
file_name = f"{sub_to_search}-results.csv"
push_list = []

#runs the query and writes to output
query_reddit(sub_to_search, terms_to_search, count_to_pull)
write_to_file(push_list)
