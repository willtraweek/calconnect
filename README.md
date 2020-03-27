# Google Calendar API Documentation

Google Doc version of this guide (https://docs.google.com/document/d/1U-PSmfarNPeA_CshZ7gMrug3F85wqPLPHlFFLBw__QQ/edit?usp=sharing)

### 1. Obtain `client_id.json` file

go to console.google.com & log on<br>
Select `Project` > `New Project` > name it whatever > `create` > next to search bar, click the project you just created<br>
search `Google Calendar API` in search bar > click `Enable` <br>
click `Create Credentials` (this will make you create OAuth client ID) > select `Google Calendar API` from dropdown menu, select `Web server` > select `User Data` > create `Authorized redirect URI` and type http://localhost:8080/ > click `set up OAuth Consent Screen` > `External` > `Create` > `Save`<br>
go back to your previous tab where you were setting up credentials and click `Refresh` > `Download`<br>
This will start the download for your `client_id.json` file<br>
Move `client_id.json` into `google_credentials` folder in the project folder<br>

### 2. Install Homebrew (https://brew.sh/)
open terminal & run<br>
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"<br>`

### 3. Install miniconda
`brew cask install miniconda`<br>

### 4. Create virtual environment for miniconda with Python 3.7
`conda create -n py3.7 python=3.7`		// -n stands for name. This virtual env is called “py3.7”<br>
`conda init zsh`					// init your appropriate shell (mine is zsh)<br>
`conda config --set changeps1 true`		// show (<virtual environment name>)<br>
`conda activate py3.7`				// activate virtual environment you just created<br>

### 5. Install Dependencies & Run Application
`pip install google-api-python-client`		// install necessary python packages<br>
`python Google_Calendar_API_Interface.py`	// run application<br>

As soon as this application begins running, it will ask you to log in to your google account from which the app will access your google calendar (the browser may warn you about our app but just ignore its warning). In order for you to get meaningful output, I suggest you fill in this account’s google calendar with meaningful events (e.g. your classes and such) so that you can have meaningful output as you’re working.

When you’re done for the day and want to exit miniconda’s virtual environment:<br>
`conda deactivate`<br>

If you find that `(base)` prefix on your terminal annoying and want to turn it off:<br>
`conda config --set changeps1 false`
