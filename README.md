## github-social ##

Analyzer to determine the metrics of how starring/forking events of influential githubbers affects repositories' starring/forking. An alternative implementation of https://github.com/geekypunk/GitHubTrends, the current implementation looks at other factors including the usage of the current repository's domain by the starrer/forker and weighted influence scores based on their repo forks to arrive at social clout an influencer's forking/starring activity has in Github.

####Usage: #####
```python main.py --creds <creds_file>```

+ main picks up get_auth from GitHubAccess which is a base loader for authentication and client data. Could be replaced with custom data loaders for implementations.

+ If creds argument is missing main's get_auth method defaults to terminal based input using raw_input and getpass.

+ main currently provides a basic run through of all[/required] instance methods from a GitHub instance towards a coverage check/assertion testing. Data for methods to run are loaded with load_json_file from GitHubAccess module and are required to be of the specified format.
	Data structure for load_json target file for main.
    ```python
    {
        "methods": {
        	"<GitHub instance method name>": "<method params>"
        }
    }
    ```

####Requirements: #####
Uses the following modules/builtins
+ ```getpass``` _For password entry in case of a creds file absence_
+ ```argparse``` _Argument parsing for credentials._
+ ```json``` _JSON loader for creds file data._


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/techiev2/github-social/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

