BaseOAuth
==========

### **Definition**

#### *BaseOAuth(oauth_version, consumer_key, consumer_secret, \*\*kwargs)*

* ***consumer_key*** : Your consumer key
* ***consumer_secret*** : Your consumer secret
* ***kwargs*** :
    - *base_url* : API Base url
    - *callback* : Callback url, by default **'oob'**
    - *from_file*: JSON File containing credentials
    - *acess_token, access_secret, session_handle, token_time* for OAuth1
    - *acess_token, token_type, refresh_token, token_time* for OAuth2

When **from_file** is not provided, **credentials** are saved in ***./secrets.json***

***OAuth1*** and ***OAuth2*** subclass ***BaseOAuth***

### **Methods**

#### *token_is_valid()*
Check if token is still valid

#### *refresh_access_token()*
Refresh access token

#### *handle()*
Get ***request token*** (OAuth1), redirect user to ***authorization url*** and get ***access token***

#### *generate_oauth2_headers*
Generates headers for ***OAuth2***

#### *oauth2_access_parser(raw_access)*
Decode ***raw_access*** response for ***OAuth2*** 
