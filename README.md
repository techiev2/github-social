## github-social ##

Analyzer to determine the metrics of how starring/forking events of influential githubbers affects repositories' starring/forking. An alternative implementation of https://github.com/geekypunk/GitHubTrends, the current implementation looks at other factors including the usage of the current repository's domain by the starrer/forker and weighted influence scores based on their repo forks to arrive at social clout an influencer's forking/starring activity has in Github.

####Usage: #####
```python main.py --creds <creds_file>```

+ If creds argument is missing main's get_auth method defaults to terminal based input using raw_input and getpass.

+ Structure for creds_file
```json
{
    "uname": <github username> [required],
    "upass": <github user password> [required],
    "client_id": <client id for an existing registered app on Github> [optional],
    "client_secret": <client secret for existing client> [optional]
}
```

####Requirements: #####
Uses the following modules/builtins
+ ```getpass``` _For password entry in case of a creds file absence_
+ ```argparse``` _Argument parsing for credentials._
+ ```json``` _JSON loader for creds file data._
