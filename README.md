# TuneDetective
Meet TuneDetective - your 24/7 musical investigator! Whether you have an audio clip, voice recording, video, or just remember some lyrics, we'll crack the case and find your song. With access to millions of tracks and lightning-fast recognition, no tune can hide from this detective! 🎵🔍

## Features

- 🎵 Identify songs from audio files
- 🎤 Recognize music from voice messages
- 🎥 Extract and identify music from video files
- 📝 Search songs by lyrics
- 📊 Track user statistics
- 📜 View search history
- 🔗 Get links to streaming platforms (Spotify, Apple Music)

## Commands

- `/start` - Start the bot and get welcome message
- `/help` - Show all available commands
- `/stats` - View your usage statistics
- `/history` - View your recent searches
- `/lyrics [text]` - Search songs by lyrics
- `/about` - Information about the bot

## Setup

1. Install Python 3.x
2. Clone this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Get required API keys:
   - Telegram Bot Token from [BotFather](https://t.me/BotFather)
   - AuDD API Key from [AuDD.io](https://audd.io/)
   - Genius Access Token from [Genius API](https://genius.com/api-clients)

5. Create a `.env` file in the project root with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_token_here
   AUDD_API_KEY=your_audd_api_key_here
   GENIUS_ACCESS_TOKEN=your_genius_token_here
   ```

6. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot in Telegram by searching for your bot's username
2. Send `/start` to get started
3. Send any audio file, voice message, or video to identify the song
4. Use `/lyrics` followed by some lyrics to search for songs
5. Use other commands to view statistics and history

## Error Handling

The bot includes comprehensive error handling:
- Invalid file formats
- Failed API requests
- Rate limiting
- Network issues

## Technical Details

- Built with pyTelegramBotAPI
- Uses AuDD API for music recognition
- Uses Genius API for lyrics search
- Supports multiple audio formats
- Includes user statistics tracking
- Maintains search history
- Provides streaming service links

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

MIT License - feel free to use this code for your own projects!
