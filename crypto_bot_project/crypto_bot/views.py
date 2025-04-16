# crypto_bot/views.py
from django.shortcuts import render
from .bot import TradingBot, save_api_keys, load_api_keys
from threading import Thread
from django.http import JsonResponse
import time
import datetime
import pytz
import re

# Global bot instance and thread
bot = None
bot_thread = None
logs = []
# Default timezone
default_timezone = 'UTC'

def log_callback(message, level="INFO", timezone=None):
    # Use provided timezone or default to UTC
    tz = pytz.timezone(timezone) if timezone else pytz.timezone(default_timezone)
    # Get current time in the specified timezone
    now = datetime.datetime.now(tz)
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Clean the message by removing any newlines and extra spaces
    clean_message = message.strip().replace('\n', ' ')
    log_entry = f"[{timestamp}] [{level}] {clean_message}"
    
    # Check for duplicate entries
    if not logs or logs[-1] != log_entry:
        logs.append(log_entry)
        if len(logs) > 100:  # Limit log size
            logs.pop(0)

def bot_control(request):
    global bot, bot_thread, default_timezone
    
    # Get the selected timezone from the request or use default
    selected_timezone = request.POST.get("timezone", default_timezone)
    if selected_timezone:
        default_timezone = selected_timezone
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "start":
            if bot is None or bot_thread is None or not bot_thread.is_alive():
                # First try to get credentials from form
                api_key = request.POST.get("api_key")
                api_secret = request.POST.get("api_secret")
                
                # If not in form, try to load saved credentials
                if not api_key or not api_secret:
                    api_key, api_secret = load_api_keys()
                
                if not api_key or not api_secret:
                    log_callback("Error: API Key and Secret are required", "ERROR", default_timezone)
                else:
                    symbol = request.POST.get("symbol", "BTC/USDT")
                    timeframe = request.POST.get("timeframe", "1h")
                    strategy = request.POST.get("strategy", "rsi")
                    amount = float(request.POST.get("amount", 10))
                    
                    # Set default windows based on strategy
                    if strategy == "rsi":
                        short_window = 14
                        long_window = 14
                    elif strategy == "macd":
                        short_window = 12
                        long_window = 26
                    elif strategy == "bollinger":
                        short_window = 20
                        long_window = 20
                    else:
                        short_window = 10
                        long_window = 50
                    
                    bot = TradingBot(lambda msg, level="INFO": log_callback(msg, level, default_timezone), api_key, api_secret)
                    bot_thread = Thread(target=bot.run, args=(symbol, timeframe, short_window, long_window, amount))
                    bot_thread.start()
        elif action == "stop":
            if bot is not None:
                bot.stop()
                bot_thread.join()
                bot = None
                bot_thread = None
        elif action == "save_keys":
            api_key = request.POST.get("api_key")
            api_secret = request.POST.get("api_secret")
            if api_key and api_secret:
                save_api_keys(api_key, api_secret)
                log_callback("API keys saved successfully", "SUCCESS", default_timezone)
            else:
                log_callback("Error: Both API Key and Secret are required to save", "ERROR", default_timezone)
        elif action == "clear_keys":
            try:
                save_api_keys("", "")  # Save empty strings to clear the keys
                log_callback("API keys cleared successfully", "SUCCESS", default_timezone)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        "status": "success",
                        "message": "API keys cleared successfully"
                    })
            except Exception as e:
                log_callback(f"Error clearing API keys: {str(e)}", "ERROR", default_timezone)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        "status": "error",
                        "message": f"Error clearing API keys: {str(e)}"
                    })
    
    api_key, api_secret = load_api_keys()
    
    # Convert logs to the user's timezone for initial page load
    converted_logs = []
    for log in logs:
        # Extract timestamp from log
        timestamp_match = re.match(r'\[(.*?)\]', log)
        if timestamp_match:
            timestamp_str = timestamp_match.group(1)
            try:
                # Parse the timestamp
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                # Assume the timestamp is in the default timezone
                source_tz = pytz.timezone(default_timezone)
                target_tz = pytz.timezone(selected_timezone)
                # Make the timestamp timezone-aware
                timestamp = source_tz.localize(timestamp)
                # Convert to target timezone
                converted_timestamp = timestamp.astimezone(target_tz)
                # Format the new timestamp
                new_timestamp_str = converted_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                # Replace the timestamp in the log
                converted_log = log.replace(f'[{timestamp_str}]', f'[{new_timestamp_str}]')
                converted_logs.append(converted_log)
            except Exception as e:
                # If conversion fails, use the original log
                converted_logs.append(log)
        else:
            converted_logs.append(log)
    
    return render(request, "bot_control.html", {
        "api_key": api_key or "",
        "api_secret": api_secret or "",
        "logs": converted_logs,
        "bot_running": bot is not None and bot_thread is not None and bot_thread.is_alive()
    })

def get_logs(request):
    # Get the selected timezone from the request or use default
    selected_timezone = request.GET.get("timezone", default_timezone)
    return JsonResponse({"logs": logs})
