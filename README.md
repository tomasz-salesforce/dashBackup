Python EA Dashboard Backup Utility

## Usage:

To use the utility, open the dashBackup.py file in a text editor. You will then have to edit the two lines in the code:

    self.sourceOAuth = "OAuth 00D1I000000mhr9!AQcAQAfXXSaG.bdWdtoET.b7jflde2dgdad"
    self.sourceInst = "https://tomasz234.my.salesforce.com"

Here you’ll have to put in your own OAuth token as well as the instance URL to the org from which you are backing up the dashboards. 

## Getting the OAuth Token

The OAuth token can be found in the Developer Console of your browser. For example in Chrome the steps are:

1. Login to your org

2. Navigate to Analytics Studio

3. Right click on the window and select "Inspect"

	![image alt text](image_0.png)

4. In the Developer Console, navigate to the "Network" tab. In Analytics, click on a dashboard, lens, or dataset and find a network request named “query”:

5. Copy the entire OAuth token from the location "Authorization"

![image alt text](image_1.png)

You can then paste this entire string into the self.sourceOAuth variable in the Python script.

## Getting the Instance URL

The instance URL can be found at the top of your browser when logged in to the org:

![image alt text](image_2.png)

Paste this into the self.sourceInst variable.

## Running the Script

To run the script, navigate to the location of the script in your terminal and type:

    python dashBackup.py

If you have everything configured correctly, you should see a folder in the same directory as where the script was run with a date/time name (ex. "2018-01-30_15-11-58"). This directory will have all of your backed up dashboards.

## Prerequisites and Troubleshooting

To get the script to work, you need to have the requests Python module installed. If you do not have it installed, you’ll get an error like this when running the script:

    ImportError: No module named requests

 when running the script, try installing the module by typing

    sudo pip install requests

 into your terminal. If you get another error such as:

    pip: command not found

first run the command:

    sudo easy_install pip

You should then be able to run the earlier command (sudo pip install requests). With no errors in these steps, you should be able to go back and run `python dashBackup.py`. 

## Notes

This script downloads the entire JSON of each dashboard that you have access to in your org using the EA Rest API. This means that it includes system generated fields such as "lastModifiedDate". If you want to paste your backed up dashboard into the JSON editor within Analytics Studio, do so by copying the “state” node of the JSON. Trying to copy the entire backed up JSON into the JSON editor in Analytics Studio will result in errors due to the extra fields included in this backup.

