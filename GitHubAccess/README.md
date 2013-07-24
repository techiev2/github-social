###GitHubAccess###
Base class that provides helper methods to authenticate a session and fetch user/repository/event information. Exposes the following instance methods

####Instance members####
- ```response```
Contains the response for the previous API call and is updated whenever an API access method is invoked.
- ```session```
Requests session instance that contains authorization information updated during _auth_session call.

####Instance methods####
#####- _auth_session#####
Session authorization method. Depends on creds instance member for username/password and config member for client data. Class init calls this method and is exposed only for tests.

#####- get_user_info#####
+ ```:param user_name:str``` Username to get information for.
+ ```:param action:str```    Action currently limited to repos search for user.
+ ```:param returns:bool```  Boolean kwarg to specify if the method needs to return response after updating the instance response member.

#####- get_repo_info#####
+ ```:param user_name:str```        Username for scoping the search repository.
+ ```:param repo_name:str```        Repository name to search for, scoped under <user_name>'s repos.
+ ```:param fields:(list, tuple)``` Fields to return in query response.
+ ```:param returns: bool```        Boolean kwarg to specify if the method needs to return response after updating the instance response member.

####- _get_data####
+ ```:param url:str```                       URL for a known API end point to hit.
+ ```:param method:<HTTP Method string>```   ['GET', 'POST', 'PUT', 'HEAD', 'DELETE'] as accepted by the end point.
+ ```:param data:dict```                     HTTP Request data as a dictionary. Would be stringified prior to submission.
+ ```:param returns: bool```                 Boolean kwarg to specify if the method needs to return response after updating the instance response member.

####Requirements: #####
Uses the following modules/builtins
+ ```requests``` _Uses requests module for HTTP access to GitHub API end points. Simple reason, convenience. Not considering a fallback httplib2_
+ ```json``` _JSON loader for response data._