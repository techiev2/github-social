## github-social ##

Analyzer to determine the metrics of how starring/forking events of influential githubbers affects repositories' starring/forking. An alternative implementation of https://github.com/geekypunk/GitHubTrends, the current implementation looks at other factors including the usage of the current repository's domain by the starrer/forker and weighted influence scores based on their repo forks to arrive at social clout an influencer's forking/starring activity has in Github.

###GitHubAccess###
Base class that provides helper methods to authenticate a session and fetch user/repository/event information. Exposes the following instance methods

####Instance methods####
#####- _auth_session#####
Session authorization method. Depends on creds instance member for username/password and config member for client data. Class init calls this method and is exposed only for tests.

#####- get_user_info#####
+ ```:param user_name:str``` Username to get information for.
+ ```:param action:str```    Action currently limited to repos search for user.
+ ```:param returns:bool```  Boolean kwarg to specify if the method needs to return response after updating the instance response member.

#####- get_repo_info#####
+ ```:param user_name:str```        Username for scoping the search repository
+ ```:param repo_name:str```        Repository name to search for, scoped under <user_name>'s repos
+ ```:param fields:(list, tuple)``` Fields to return in query response.
+ ```:param returns: bool```        Boolean kwarg to specify if the method needs to return response after updating the instance response member.

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
