
# reddit-api-data-fetch (Jan, 2020)

A simple Python 3 script with the [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/) to fetch and store post data from Reddit.

The script takes three arguments (desired subreddit, keyword, and number of posts) and writes the fetched content to a .csv file.

## Running the script

To run the script, make sure you've got PRAW [installed on your machine](https://praw.readthedocs.io/en/latest/getting_started/installation.html).

If you haven't done so already, [create an app](https://www.reddit.com/prefs/apps/) for use with the Reddit API to get your Client ID, Client Secret, and User Agent and place those values in a "config<i></i>.py" file in the same directory:

```
#config.py
cid = 'CLIENT ID'
cs = 'CLIENT SECRET'
ua = 'USER AGENT'
```

When you've done the above, you're good to cd into the directory with main.<i></i>py and config<i></i>.py, and run the script with some arguments:

```
python3 main.py austin homeless 100
```
Running the above will pull down the latest 100 posts in the Austin subreddit containing the keyword 'homeless' in their title or body.

These results will then be stored in a file titled <i>austin-homeless.csv</i> which will be created (or updated if it already exists) in the same directory.

## To do:

- Provide more options (beyond .csv) to customize how data is stored.
- Think about other options for date / retrieved-at values.
- Explore ways to utilize this in data vis!
