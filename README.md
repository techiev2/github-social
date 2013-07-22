#### github-social ####

Analyzer to determine the metrics of how starring/forking events of influential githubbers affects repositories' starring/forking. An alternative implementation of https://github.com/geekypunk/GitHubTrends, the current implementation looks at other factors including the usage of the current repository's domain by the starrer/forker and weighted influence scores based on their repo forks to arrive at social clout an influencer's forking/starring activity has in Github.

* Base class of Popular contains the following instance methods currently.
    1. get_current_user : Returns current session user's data.
                            Uses the credentials at init.
    2. get_top_repos: Returns a list of top forked/starred repositories matching
                        a user query.
                     `:param: user: Boolean. Switches context between repos/users
                        matching query.`
    3. get_top_repo_users: Returns a list of owners for top repos returned by the
                        previous instance method.
                        Depends on instance value of repo_data to get repos list.
    4. get_user_activity: Returns a list of public activities for a specific user.
                            `:param: username: Search username`
                            `:param: fork: Boolean. Include fork activities`
                            `:param: follow: Boolean. Include following activities`
                            `:param: watch: Boolean. Include watching activities`

* Helper methods:
    1. usable_json : Returns a JSON string of return data that is normalized
                    for use with JS clients which can't work with datetime
                    objects.
                    `:param: json_string: JSON data as string/dict. Is stringified
                            if it is a dict.`
                    `:param: stringify: Boolean. Specifies if the response must be
                            stringified for use with clients that depend on strigified
                            datetime data/others.`