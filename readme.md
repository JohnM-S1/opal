The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

# OSCAL Policy Administration Library (opal)
Provides a simple web application for managing System Security Plans and related documents.  The data model is based on the OSCAL standard and objects can be imported and exported in OSCAL compliant JSON. 

The OSCAL Model Reference can be found at, https://pages.nist.gov/OSCAL/reference/latest/complete/

1. Python >=3.8
2. apache
3. postgres client if using a postgres database

# Deployment Instructions
## Running a local development version using sqlite
1. Clone the repository to your local directory\
   `git clone https://github.com/eop-omb/opal.git`
1. It is recommended to run the application from a virtual environment. To do so navigate to the application directory in a terminal and enter the following commands:\
   `python3 -m venv venv`\
   `source venv/bin/activate`
1. Install the required python modules by running:\
   `pip install -r requirements.txt`
1. Run the initial migration to create the database objects:\
   `python manage.py makemigrations`\
   `python manage.py migrate`
1. Create a superuser:\
   `python manage.py createsuperuser`
1. Start the Server\
   `python manage.py runserver`
## Start the app in a docker container using sqlite
1. Clone the repository to your local directory
   `git clone https://gitlab.max.gov/max-security/opal.git`
3. Build the image\
    `docker build -t opal .`
1. Run the container\
    `docker run --rm -it --name opal -p 8000:8000 -e DB_HOST=localhost -e DB_NAME=db.sqlite3 -e LOG_LEVEL=DEBUG -e opal`
    

## Setting environment variables
OPAL is designed to run well in a containerized environment. It is recommended to set any desired environment variables using your chosen container orchestration solution (kubernetes, docker-compose, etc.).  You can also set environment variables in a .env file which should be placed in the opal subdirectory. All variables are optional and will be populated with reasonable defaults if not provided. 

**NOTE: defaults will be applied if the environment variable is NOT provided, but if you provide an empty string or something similar the application will not overwrite that with the default value.**

The available environment variables are: 


| Variable                        | Values                                                 | Description                                                                                                                                                                                                                                                                                                                                          |
|---------------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENVIRONMENT                     | production                                             | If omitted defaults to "development"                                                                                                                                                                                                                                                                                                                 |
| OPAL_SECRET_KEY                 | a valid 50 character django secret key                 | secret key used to create sessions. If excluded a random key will be generated each time the app starts                                                                                                                                                                                                                                              |
| DEBUG                           | True or False                                          | enables some debugging features. If omitted defaults to True                                                                                                                                                                                                                                                                                         |
| ALLOWED_HOSTS                   | comma seperated list of FQDNs or hostnames             | Can be a list such as "localhost,127.0.0.1", If omitted defaults to * which will respond to any hostname.                                                                                                                                                                                                                                            |
 | DATABASE                        | sqlite or postgres                                     | defines the kind of database to use.  Defaults to sqlite                                                                                                                                                                                                                                                                                             |
| DB_NAME                         | name of db in postgres or filename if using sqlite     | can be blank if using sqlite                                                                                                                                                                                                                                                                                                                         |
| DB_PASSWORD                     | password the app should use to connect to the database | can be blank or omitted if using sqlite                                                                                                                                                                                                                                                                                                              |
| DB_USER                         | username the app should use to connect to the database | can be blank if using sqlite                                                                                                                                                                                                                                                                                                                         |
| DB_HOST                         |                                                        | can be blank if using sqlite                                                                                                                                                                                                                                                                                                                         |
| DB_PORT                         |                                                        | can be blank if using sqlite                                                                                                                                                                                                                                                                                                                         |
| LOG_LEVEL                       | DEBUG, INFO, WARNING, ERROR, or CRITICAL               | Defaults to INFO                                                                                                                                                                                                                                                                                                                                     |

| Variable                        | Values                                                 | Description                                                                                                                                                                                                                                                                                                                                          |
|---------------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENABLE_OIDC                     | True or False                                          | set this to True to enable OIDC Authentication. If enabled, the following additional variables are required:                                                                                                                                                                                                                                         |
| OIDC_RP_CLIENT_ID               |                                                        | client ID from your SAML Provider                                                                                                                                                                                                                                                                                                                    |
| OIDC_RP_CLIENT_SECRET           |                                                        | Secret provided by your SAML IDP                                                                                                                                                                                                                                                                                                                     |
| OIDC_OP_AUTHORIZATION_ENDPOINT  |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_OP_TOKEN_ENDPOINT          |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_OP_USER_ENDPOINT           |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_RP_SIGN_ALGO               |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_OP_JWKS_ENDPOINT           |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_OP_LOGIN_REDIRECT_URL              |                                                        |                                                                                                                                                                                                                                                                                                                                                      |
| OIDC_OP_LOGOUT_REDIRECT_URL             |                                                        |                                                                                                                                                                                                                                                                                                                                                      |

| Variable                           | Values        | Description                                                                                                                                                                                                                                                                                                                                          |
|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENABLE_SAML                        | True or False | set this to True to enable OIDC Authentication. If enabled, the following additional variables are required:                                                                                                                                                                                                                                         |
| SOCIAL_AUTH_SAML_SP_ENTITY_ID      |               | The SAML Entity ID for your app. This should be a URL that includes a domain name you own. It doesn’t matter what the URL points to. Example: http://saml.yoursite.com                                                                                                                                                                               |
| SOCIAL_AUTH_SAML_SP_PUBLIC_CERT    |               | The X.509 certificate string for the key pair that your app will use. You can generate a new self-signed key pair with: <pre>openssl req -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.key</pre> The contents of saml.crt should then be used as the value of this setting (you can omit the first and last lines, which aren’t required). |
| SOCIAL_AUTH_SAML_SP_PRIVATE_KEY    |               | The private key to be used by your app. If you used the example openssl command given above, set this to the contents of saml.key (again, you can omit the first and last lines).                                                                                                                                                                    |
| SOCIAL_AUTH_SAML_ORG_INFO          |               | A dictionary that contains information about your app. You must specify values for English at a minimum. Each language’s entry should specify a name (not shown to the user), a displayname (shown to the user), and a URL.                                                                                                                          |
| SOCIAL_AUTH_SAML_TECHNICAL_CONTACT |               | A dictionary with two values, givenName and emailAddress, describing the name and email of a technical contact responsible for your app.                                                                                                                                                                                                             |
| SOCIAL_AUTH_SAML_SUPPORT_CONTACT   |               | A dictionary with two values, givenName and emailAddress, describing the name and email of a support contact for your app.                                                                                                                                                                                                                           |
| SOCIAL_AUTH_SAML_ENABLED_IDPS      |               | The most important setting. List the Entity ID, SSO URL, and x.509 public key certificate for each provider that your app wants to support. The SSO URL must support the HTTP-Redirect binding. You can get these values from the provider’s XML metadata.                                                                                           | 


