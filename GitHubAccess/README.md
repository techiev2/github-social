##GitHubAccess##
Package that provides access class and helper methods to authenticate a GitHub API session and operate with the API end points including fetch user/repository/event information.

###Package exports###
####Module : utils####
- ```get_auth : method```
Provides a base loader for authentication data from a JSON(ic) data construct with the below data structure. Could be replaced with custom data loader to provide authentication credentials and client data to GitHubAccess object invocation. Would be internally calling load_json_file method after a future changeset.

    Data structure for creds_file
    ```python
    {
        "uname": <github username> [required],
        "upass": <github user password> [required],
        "client_id": <client id for an existing registered app on Github> [optional],
        "client_secret": <client secret for existing client> [optional]
    }
    ```

- ```load_json_file : method```
Provides a base loader for JSON(ic) data construct with the below data structure. Could be replaced with custom data loader to provide authentication credentials and client data to GitHubAccess object invocation.
	+ Depends on soft tabbing with the input files (4 soft tabs/spaces) per level
	+ Excludes inline commented lines

####Module : GitHub####
- ```GitHub : Class```
Provides base class for accessing various GitHub API end points.

	####GitHub instance init params#####
	```python
	{
		creds : <tuple>,
	    config : {
	        'reverse': <boolean>,
	        'auth': <boolean>,
	        'safe_json': <boolean>,
	        'client_data': <dict>
	    }
	}
	```
	
	- _creds:_
		Tuple of username and password to authenticate a GitHub API session.
	- _config:_
		- config.reverse - Boolean toggle specifying if the password is reversed. 
		- config.auth - Boolean to specify call to _auth_session on init.
		- config.safe_json - Not implemented. Boolean toggle for Javascript friendly JSON if required.
		- config.client_data - GitHub client data if a registered GitHub API client is available. Helps increase rate limiting bounds.
	
	###GitHub instance members###
	- ```response```
	Contains the response for the previous API call and is updated whenever an API access method is invoked.
	- ```session```
	Requests session instance that contains authorization information updated during _auth_session call.
	
	###GitHub instance methods###
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
	
	#####- _get_data####
	+ ```:param url:str```                       URL for a known API end point to hit.
	+ ```:param method:<HTTP Method string>```   ['GET', 'POST', 'PUT', 'HEAD', 'DELETE'] as accepted by the end point.
	+ ```:param data:dict```                     HTTP Request data as a dictionary. Would be stringified prior to submission.
	+ ```:param returns: bool```                 Boolean kwarg to specify if the method needs to return response after updating the instance response member.
	
	#####- search_repos####
	+ ```:param query:dict```                    Search query as dictionary with the following structure.
		```{
			keyword: <str>
		}```
	+ ```:param fields:iterable```               List of fields to return from search_repos method's API response.
	+ ```:param returns: bool```                 Boolean kwarg to specify if the method needs to return response after updating the instance response member.

	#####- get_user_events####
	+ ```:param user_name:str```                 Username to get a list of events. Method returns a list of events created by the user.
	+ ```:param organization:str```              Organization name to restrict the list of user events for the requested user.
	+ ```:param event_types:iterable```          List of events to restrict the response to. Takes in standard GitHub user activity events.
	+ ```:param returns: bool```                 Boolean kwarg to specify if the method needs to return response after updating the instance response member.

	#####- get_user_stars####
	+ ```:param user_name:str```                 Username to get a list of starred repositories.
	+ ```:param repo_language:str```             Language string to restrict the list of user starred repositories to.
	+ ```:param returns: bool```                 Boolean kwarg to specify if the method needs to return response after updating the instance response member.

####Requirements: #####
Uses the following modules/builtins
+ ```requests``` _Uses requests module for HTTP access to GitHub API end points. Simple reason, convenience. Not considering a fallback httplib2_
+ ```json``` _JSON loader for response data._
