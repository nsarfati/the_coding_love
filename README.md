# The Coding Love Feed Parser

If you love so much [the coding love](https://thecodinglove.com/) gifs as I do, you probably want to see them in Slack everyday.

So, this is a little script that will make your morning a bit better

## Requirements:
- Python >= 2.7.x
- pip
- Run pip install -r requirements.txt

## How to run it?

Just remember to configure:
- The Slack bot token variable: `BOT_TOKEN`
- The Slack channel that you want to use: `THE_CODING_LOVE_CHANNEL`, set to `#the_coding_love` by default
- The file where the sent gifs are going to be stored: `PROCESSED_URLS_FILE_NAME`, set to `./the_coding_love_lines` by default

Then, you just cron it every 10 minutes in you crontab as:

`*/10 * * * * python <path>./the-coding-love/the_coding_love.py`

And it's all

## Contribute?

Feel free to migrate it to python3 if you don't feel run it in 2.7 :)