# AutoresponderForAllegroSeller
This application sends short auto response every 15 minutes for allegro user which texted you.
Dont bother yourself about spam. If you had a conversation with user in last 24 hours autoresponder won't send him autoresponse.

> [!IMPORTANT]
> This application work only with allegro sandbox. If you want to use it with real allegro, then you have to change all links in `main.py` by deleting `.allegrosandbox.pl` from links.

## Technologies used in project
* Python 3.12
* Bash
* Cron

## Installation
1. Download repository
2. Complete run_autoresponder.sh by adding path to this file after `cd` command
3. Open terminal and go to project directory
4. If you are using macOS give full disc access for `cron` 
5. Type `chmod 755 install.sh run_autoresponder.sh`
6. Then run `./install.sh`
   
Now your autoresponder should work and if it doesn't, [report issue](https://github.com/TomaszCaba/AutoresponderForAllegroSeller/issues)


> [!TIP]
> You can change `AUTORESPONSE` variable in `main.py` to personalize auto response text.
