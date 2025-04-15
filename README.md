# Django Trading Bot

A powerful cryptocurrency trading bot built with Django, featuring real-time trading, customizable strategies, and a modern web interface.

![Django Trading Bot](https://images.unsplash.com/photo-1639762681485-074b7f938ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80)

## Features

- **Real-time Trading**: Execute trades automatically based on customizable strategies
- **Multiple Trading Strategies**: Choose from RSI, MACD, Bollinger Bands, or create your own
- **Custom Trading Pairs**: Add any cryptocurrency pair to the trading list
- **Secure API Key Management**: Encrypted storage of exchange API credentials
- **Real-time Logging**: Monitor trading activity with auto-scrolling logs
- **Responsive UI**: Modern, mobile-friendly interface with cryptocurrency-themed design
- **Timezone Support**: Configure the bot to operate in your local timezone
- **WebSocket Integration**: Real-time updates without page refreshes

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-trading-bot.git
   cd django-trading-bot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000`

## Configuration

### API Credentials

1. Navigate to the API Credentials section
2. Enter your exchange API key and secret
3. Click "Save Keys" to securely store your credentials

### Trading Parameters

1. Select a trading pair (e.g., BTC/USDT)
2. Choose a timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d)
3. Select your timezone
4. Choose a trading strategy
5. Set your trade amount in USDT
6. Click "Start Trading" to begin

### Custom Trading Pairs

1. Select "Custom Pair..." from the dropdown
2. Enter your custom pair in the format BASE/QUOTE (e.g., LINK/USDT)
3. Click "Add to Dropdown" to save it for future use

## Trading Strategies

### RSI Strategy
- Relative Strength Index (RSI) based trading
- Buy when RSI is oversold (below 30)
- Sell when RSI is overbought (above 70)

### MACD Strategy
- Moving Average Convergence Divergence based trading
- Buy on bullish crossover
- Sell on bearish crossover

### Bollinger Bands Strategy
- Price volatility based trading
- Buy when price touches lower band
- Sell when price touches upper band

## Log Management

- **View Logs**: Real-time trading logs are displayed in the Trading Log section
- **Clear Logs**: Click "Clear Log" to remove all logs
- **Auto-scroll**: Toggle auto-scrolling with the "Toggle Auto-scroll" button

## Security

- API keys are encrypted before storage
- Passwords are never displayed in plain text
- WebSocket connections are secured
- CSRF protection is enabled for all forms

### Protecting Sensitive Files

To prevent accidentally committing sensitive files to Git:

1. Add these entries to your `.gitignore` file:
   ```
   # Sensitive files
   api_keys.enc
   secret.key
   .env
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   env/
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   *.egg-info/
   .installed.cfg
   *.egg
   
   # Virtual Environment
   venv/
   ENV/
   
   # IDE
   .idea/
   .vscode/
   *.swp
   *.swo
   
   # OS
   .DS_Store
   Thumbs.db
   ```

2. If you've already committed these files, remove them from Git tracking:
   ```bash
   git rm --cached api_keys.enc
   git rm --cached secret.key
   ```

3. For deployment, securely transfer these files:
   - Use secure copy (scp) or SFTP
   - Use environment variables in production
   - Use a secure secrets management service

4. Create template files for reference:
   ```bash
   # Create api_keys.enc.template
   touch api_keys.enc.template
   # Create secret.key.template
   touch secret.key.template
   ```

5. Document the format in templates without real values

NEVER commit real API keys or secrets to version control!

## Development

### Project Structure

```
django-trading-bot/
├── crypto_bot_project/      # Main Django project
│   ├── crypto_bot/          # Main app
│   │   ├── bot.py           # Trading bot logic
│   │   ├── consumers.py     # WebSocket consumers
│   │   ├── models.py        # Database models
│   │   ├── routing.py       # WebSocket routing
│   │   └── views.py         # View functions
│   ├── staticfiles/         # Static files
│   │   ├── icons/           # Cryptocurrency icons
│   │   ├── custom_pair.js   # Custom pair handling
│   │   ├── log_fix.js       # Log management
│   │   └── style.css        # Main stylesheet
│   └── templates/           # HTML templates
│       └── bot_control.html # Main UI template
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

### Adding New Features

1. Create a new branch for your feature
2. Implement the feature
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Cryptocurrency icons from [Cryptocurrency Icons](https://github.com/spothq/cryptocurrency-icons)
- Background image from [Unsplash](https://unsplash.com)
- Font Awesome for icons
- Django and Channels for the backend framework 

## Environment Variables

To use the bot with your own API keys, set the following environment variables:

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
``` 

## Pre-commit Hook

To prevent accidental commits of sensitive files, you can set up a pre-commit hook. Add the following script to your `.git/hooks` directory:

```bash
#!/bin/sh
if git diff --cached | grep -q "api_keys.enc\|secret.key"; then
    echo "ERROR: Attempting to commit sensitive files"
    exit 1
fi 