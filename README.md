

# reddit-python-data-fetch

A simple Python 3 script with the [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/) to retrieve and store recent posts made in a specific subreddit.

The script takes three arguments (desired subreddit, keyword, and number of days) to query the API write the output to a .csv file.

## Running the script

To run the script, make sure you've got PRAW [installed on your machine](https://praw.readthedocs.io/en/latest/getting_started/installation.html).

Additionally, [create an app](https://www.reddit.com/prefs/apps/) for use with the Reddit API to get your Client ID, Client Secret, and User Agent and place these values within "config<i></i>.py" in the same directory:

```
#config.py
cid = 'CLIENT ID'
cs = 'CLIENT SECRET'
ua = 'USER AGENT'
```

When you've added your details to the config file, you're good to navigate to the directory and run the script with your desired search terms.

Here's a sample:

```
python3 main.py austin homeless 14
```
Running the above will pull the most recent posts from the <b><u>austin</u></b> subreddit containing '<b><u>homeless</u></b>' in the title or body that were created within the last <b><u>14 days</u></b>.

These results will then be stored in a file titled <i>austin-homeless.csv</i> which will be created (or updated if it already exists) in the same directory.
