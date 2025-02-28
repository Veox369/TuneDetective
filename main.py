import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from dotenv import load_dotenv
import json
from datetime import datetime
from lyrics_search import LyricsSearch
import time

# Load environment variables
load_dotenv()

# Initialize bot and services
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUDD_API_KEY = os.getenv('AUDD_API_KEY')
bot = telebot.TeleBot(BOT_TOKEN)
lyrics_search = LyricsSearch()

# Store user statistics
user_stats = {}

def log_user_action(user, action):
    """Log user actions with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] 👤 User: {user.first_name} (ID: {user.id})")
    print(f"[{timestamp}] 🎯 Action: {action}")
    print("-" * 50)

def init_user_stats(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {
            'searches': 0,
            'successful_matches': 0,
            'history': [],
            'joined_date': datetime.now().strftime('%Y-%m-%d')
        }

def create_menu_keyboard():
    """Create an inline keyboard for the main menu."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📊 Statistics", callback_data="stats"),
        InlineKeyboardButton("📜 History", callback_data="history"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        InlineKeyboardButton("👾 About", callback_data="about")
    ]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Initialize user stats
    init_user_stats(message.from_user.id)
    
    # Log user start
    log_user_action(message.from_user, "started using the bot")
    
    welcome_text = (
        "🎵 *Welcome to Music Recognition Bot!*\n\n"
        "I'm your personal music detective! Here's what I can do:\n\n"
        "🎧 *Identify Songs From:*\n"
        "• Audio files 🎵\n"
        "• Voice messages 🎤\n"
        "• Video files 🎥\n"
        "• Song lyrics 📝\n\n"
        "*Quick Start:*\n"
        "1️⃣ Send any audio/voice/video\n"
        "2️⃣ Or use /lyrics to search by text\n"
        "3️⃣ Get instant song matches!\n\n"
        "Use the menu below to explore more features! 👇"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=create_menu_keyboard()
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    log_user_action(message.from_user, "requested help")
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🔍 Try Lyrics Search", callback_data="lyrics_help"),
        InlineKeyboardButton("📊 View Stats", callback_data="stats"),
        InlineKeyboardButton("📜 View History", callback_data="history"),
        InlineKeyboardButton("ℹ️ About Bot", callback_data="about")
    ]
    keyboard.add(*buttons)

    help_text = (
        "*🤖 Bot Commands & Features*\n\n"
        "*Main Commands:*\n"
        "• /start - Launch the bot\n"
        "• /stats - Your usage statistics\n"
        "• /history - Recent searches\n"
        "• /about - Bot information\n"
        "• /help - Show this help\n\n"
        "*Music Recognition:*\n"
        "• Send any audio file 🎵\n"
        "• Record a voice message 🎤\n"
        "• Share a video clip 🎥\n\n"
        "*Lyrics Search:*\n"
        "• Use /lyrics + text 📝\n"
        "Example: `/lyrics we will rock you`\n\n"
        "_Select an option below:_ 👇"
    )
    bot.reply_to(
        message,
        help_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['about'])
def send_about(message):
    log_user_action(message.from_user, "viewed about info")
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🎵 Start Using", callback_data="new_search"),
        InlineKeyboardButton("❓ Help", callback_data="help"),
        InlineKeyboardButton("⭐️ View Stats", callback_data="stats"),
        InlineKeyboardButton("📜 History", callback_data="history")
    ]
    keyboard.add(*buttons)

    about_text = (
        "*🎵 Music Recognition Bot*\n\n"
        "*Features:*\n"
        "• Instant song recognition 🎧\n"
        "• Support for multiple file types 📁\n"
        "• Lyrics search functionality 📝\n"
        "• Personal usage statistics 📊\n"
        "• Search history tracking 📜\n\n"
        "*Technologies:*\n"
        "• AuDD Music Recognition API 🎵\n"
        "• Genius Lyrics API 📚\n"
        "• Spotify Integration 🎧\n"
        "• Apple Music Integration 🎵\n\n"
        "_Created with ❤️ by Your Bot Creator_\n\n"
        "What would you like to do? 👇"
    )
    bot.reply_to(
        message,
        about_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['stats'])
def send_stats(message):
    log_user_action(message.from_user, "checked their stats")
    user_id = message.from_user.id
    init_user_stats(user_id)
    stats = user_stats[user_id]
    
    success_rate = (stats['successful_matches'] / stats['searches'] * 100) if stats['searches'] > 0 else 0
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📜 View History", callback_data="history"),
        InlineKeyboardButton("🔍 New Search", callback_data="new_search")
    ]
    keyboard.add(*buttons)
    
    stats_text = (
        "*📊 Your Music Detective Stats*\n\n"
        "*Activity Overview:*\n"
        f"• Total Searches: `{stats['searches']}`\n"
        f"• Successful Matches: `{stats['successful_matches']}`\n"
        f"• Success Rate: `{success_rate:.1f}%`\n"
        f"• Member Since: `{stats['joined_date']}`\n\n"
        "_Select an option below:_ 👇"
    )
    bot.reply_to(
        message,
        stats_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['history'])
def send_history(message):
    log_user_action(message.from_user, "viewed their history")
    user_id = message.from_user.id
    init_user_stats(user_id)
    history = user_stats[user_id]['history']
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🔍 New Search", callback_data="new_search"),
        InlineKeyboardButton("📊 View Stats", callback_data="stats")
    ]
    keyboard.add(*buttons)
    
    if not history:
        bot.reply_to(
            message,
            "*No Search History Yet* 🎵\n\n"
            "Start by:\n"
            "• Sending an audio file\n"
            "• Recording a voice message\n"
            "• Using /lyrics to search\n\n"
            "_Try your first search!_ 👇",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return
    
    history_text = (
        "*🕒 Your Recent Music Discoveries*\n\n"
        "_Last 10 searches:_\n\n"
    )
    for item in history[-10:]:  # Show last 10 searches
        history_text += f"• `{item['title']}` - _{item['artist']}_\n"
    
    history_text += "\n_What would you like to do next?_ 👇"
    
    bot.reply_to(
        message,
        history_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

def create_loading_animation(message):
    """Create a loading animation while processing."""
    loading_texts = [
        "🎵 Analyzing your file",
        "🎵 Analyzing your file.",
        "🎵 Analyzing your file..",
        "🎵 Analyzing your file..."
    ]
    msg = bot.reply_to(message, loading_texts[0])
    
    for i in range(2):  # Show animation for 2 cycles
        for text in loading_texts[1:]:
            time.sleep(0.5)
            try:
                bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id)
            except:
                pass
    
    return msg

@bot.message_handler(content_types=['audio', 'voice', 'video'])
def handle_audio(message):
    try:
        # Log file processing
        file_type = 'audio' if message.audio else 'voice' if message.voice else 'video'
        log_user_action(message.from_user, f"submitted a {file_type} file for recognition")
        
        # Show loading animation
        processing_msg = create_loading_animation(message)
        
        # Get file info
        if message.audio:
            file_info = bot.get_file(message.audio.file_id)
        elif message.voice:
            file_info = bot.get_file(message.voice.file_id)
        else:  # video
            file_info = bot.get_file(message.video.file_id)
        
        # Download file
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        
        # Recognize music using AuDD API
        response = requests.post('https://api.audd.io/', data={
            'api_token': AUDD_API_KEY,
            'url': file_url,
            'return': 'apple_music,spotify'
        })
        
        result = response.json()
        
        # Update user stats
        user_id = message.from_user.id
        init_user_stats(user_id)
        user_stats[user_id]['searches'] += 1
        
        if result['status'] == 'success' and result.get('result'):
            # Successful match
            song = result['result']
            user_stats[user_id]['successful_matches'] += 1
            
            # Log successful recognition
            log_user_action(message.from_user, f"found song: {song['title']} by {song['artist']}")
            
            # Add to history
            user_stats[user_id]['history'].append({
                'title': song['title'],
                'artist': song['artist']
            })
            
            # Create inline keyboard for streaming links
            keyboard = InlineKeyboardMarkup(row_width=2)
            buttons = []
            if 'spotify' in song:
                buttons.append(InlineKeyboardButton(
                    "🎧 Listen on Spotify",
                    url=song['spotify']['external_urls']['spotify']
                ))
            if 'apple_music' in song:
                buttons.append(InlineKeyboardButton(
                    "🎵 Listen on Apple Music",
                    url=song['apple_music']['url']
                ))
            buttons.append(InlineKeyboardButton("🔍 New Search", callback_data="new_search"))
            keyboard.add(*buttons)
            
            # Format response with emojis and markdown
            response_text = (
                f"*✨ Found Your Song!*\n\n"
                f"*🎵 Title:* `{song['title']}`\n"
                f"*👤 Artist:* `{song['artist']}`\n"
                f"*💿 Album:* `{song.get('album', 'N/A')}`\n"
                f"*📅 Released:* `{song.get('release_date', 'N/A')}`\n\n"
                f"_Click the buttons below to listen:_ 👇"
            )
            
            bot.edit_message_text(
                response_text,
                chat_id=processing_msg.chat.id,
                message_id=processing_msg.message_id,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            # Log failed recognition
            log_user_action(message.from_user, "no song match found")
            
            bot.edit_message_text(
                "Sorry, I couldn't identify that song. Please try again with a different part of the song.",
                chat_id=processing_msg.chat.id,
                message_id=processing_msg.message_id
            )
    
    except Exception as e:
        log_user_action(message.from_user, f"encountered an error: {str(e)}")
        bot.reply_to(
            message,
            "Sorry, something went wrong while processing your request. Please try again later."
        )
        print(f"Error: {str(e)}")

@bot.message_handler(commands=['lyrics'])
def handle_lyrics_search(message):
    try:
        # Get the search query
        query = message.text.replace('/lyrics', '').strip()
        
        # Log lyrics search attempt
        log_user_action(message.from_user, f"searched lyrics: '{query}'" if query else "attempted lyrics search without query")
        
        if not query:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("📝 Try an Example", callback_data="lyrics_example"))
            bot.reply_to(
                message,
                "*How to Search by Lyrics* 🎵\n\n"
                "Type /lyrics followed by some lyrics you remember.\n\n"
                "Example: `/lyrics we will rock you`\n\n"
                "_Click the button below to try an example!_ 👇",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            return

        # Show searching animation
        loading_msg = bot.reply_to(
            message,
            "🔍 *Searching for matching songs...*",
            parse_mode="Markdown"
        )

        # Search for songs
        results = lyrics_search.search_song(query)
        
        if not results:
            # Log no results found
            log_user_action(message.from_user, "no lyrics matches found")
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("🔄 Try Another Search", callback_data="lyrics_help"))
            bot.edit_message_text(
                "*No Songs Found* 😕\n\n"
                "Try:\n"
                "• Using different lyrics\n"
                "• Checking for typos\n"
                "• Using a longer portion of the lyrics\n\n"
                "_Click below to try another search!_ 👇",
                chat_id=loading_msg.chat.id,
                message_id=loading_msg.message_id,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            return

        # Log successful search
        log_user_action(message.from_user, f"found {len(results)} songs matching lyrics")

        # Create inline keyboard for results
        keyboard = InlineKeyboardMarkup(row_width=1)
        for song in results:
            keyboard.add(InlineKeyboardButton(
                f"🎵 {song['title']} - {song['artist']}",
                url=song['url']
            ))
        keyboard.add(InlineKeyboardButton("🔍 New Lyrics Search", callback_data="lyrics_help"))

        # Format results with markdown
        response = (
            f"*✨ Found {len(results)} Matching Songs!*\n\n"
            f"*Your Lyrics:* `{query}`\n\n"
            "_Click on a song to see full lyrics:_ 👇"
        )

        bot.edit_message_text(
            response,
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        
        # Update user stats
        user_id = message.from_user.id
        init_user_stats(user_id)
        user_stats[user_id]['searches'] += 1
        
        # Add first result to history
        if results:
            user_stats[user_id]['history'].append({
                'title': results[0]['title'],
                'artist': results[0]['artist']
            })

    except Exception as e:
        log_user_action(message.from_user, f"lyrics search error: {str(e)}")
        bot.reply_to(message, "Sorry, something went wrong while searching for lyrics. Please try again later.")
        print(f"Error in lyrics search: {str(e)}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Handle inline keyboard button clicks."""
    try:
        # Log button click
        log_user_action(call.from_user, f"clicked button: {call.data}")
        
        if call.data == "stats":
            send_stats(call.message)
        elif call.data == "history":
            send_history(call.message)
        elif call.data == "help":
            send_help(call.message)
        elif call.data == "about":
            send_about(call.message)
        elif call.data == "lyrics_help":
            bot.send_message(
                call.message.chat.id,
                "*Search by Lyrics* 🎵\n\n"
                "Type /lyrics followed by some lyrics you remember.\n\n"
                "Example: `/lyrics we will rock you`",
                parse_mode="Markdown"
            )
        elif call.data == "lyrics_example":
            bot.send_message(
                call.message.chat.id,
                "/lyrics we will rock you"
            )
        elif call.data == "new_search":
            text = (
                "*Ready for Another Song!* 🎵\n\n"
                "You can:\n"
                "• Send an audio file 🎵\n"
                "• Send a voice message 🎤\n"
                "• Send a video file 🎥\n"
                "• Use /lyrics to search by lyrics 📝\n"
            )
            bot.send_message(
                call.message.chat.id,
                text,
                parse_mode="Markdown",
                reply_markup=create_menu_keyboard()
            )
        
        # Remove the loading animation from inline button
        bot.answer_callback_query(call.id)
    
    except Exception as e:
        print(f"Callback error: {str(e)}")
        bot.answer_callback_query(call.id, "An error occurred. Please try again.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Log unknown command/message
    log_user_action(message.from_user, f"sent unrecognized message: {message.text}")
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📖 View Commands", callback_data="help"),
        InlineKeyboardButton("🔍 Search Lyrics", callback_data="lyrics_help"),
        InlineKeyboardButton("📊 My Stats", callback_data="stats"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    ]
    keyboard.add(*buttons)
    
    text = (
        "*How Can I Help You?* 🤔\n\n"
        "Send me:\n"
        "• Audio file 🎵\n"
        "• Voice message 🎤\n"
        "• Video file 🎥\n"
        "• Use /lyrics + text 📝\n\n"
        "_Choose an option below or send me a file!_ 👇"
    )
    bot.reply_to(
        message,
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

def main():
    # Print startup banner
    print("\n" + "=" * 50)
    print("🎵 Music Recognition Bot Starting...")
    print("=" * 50)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")
    
    # Start bot
    bot.infinity_polling()

if __name__ == "__main__":
    main()
