# data-scrapper
Data Scrapper for Shopee

# Docker Setup
## Build Docker Image
`docker build . --tag ubuntu`

## Running Docker Images
Runs both previously built ubuntu image and postgres image
`./run_docker.sh`

# Manual Setup
## Setup PostgreSQL database

- `apt install postgresql`
- `sudo service postgresql start`
- `sudo -u postgres createuser [username]`
- `sudo -u postgres createdb [database_name]`
- `sudo -u postgres psql`
  - `alter user [username] with encrypted password '[password]';`
  - `grant all privileges on database [database_name] to [username];`

## Setup ChromeDriver for Selenium

- `wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
- `dpkg -i google-chrome-stable_current_amd64.deb`
- (optional) `sudo apt --fix-broken install`
- check chrome version with `google-chrome --version`
- Download compatible ChromeDriver from `https://chromedriver.chromium.org/downloads`

## Run Scraper
- `python3 scraper.py --databse_name [database_name] --username [username]`

## Run Flask server showing scraped results
- `export FLASK_APP=server`
- `flask run`
