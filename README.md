# CryptoAlert Bot

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-0088cc)

A powerful Telegram bot that monitors cryptocurrency markets and sends you real-time alerts when coins match your custom criteria. Set up personalized filters for market cap, volume, price changes, and more to never miss potential opportunities.

## 🚀 Features

- **Custom Filter Creation**: Define your own criteria for coins you want to track
- **Real-time Notifications**: Receive instant Telegram messages when coins match your filters
- **Multiple Filter Support**: Create different filter sets for various strategies
- **Comprehensive Metrics**: Filter by market cap, 24h volume, price change, and more
- **Detailed Coin Information**: Get complete data on matching cryptocurrencies
- **User-friendly Commands**: Easy-to-use interface with intuitive commands
- **Secure Authentication**: Only authorized users can access your bot
- **Low-latency Alerts**: Minimal delay between coin detection and notification

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- API keys for cryptocurrency data sources
- Redis (for caching and rate limiting)

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cryptoalert-bot.git
cd cryptoalert-bot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and Telegram Bot token
```

## 🚀 Quick Start

1. Start the bot:
   ```bash
   python bot.py
   ```

2. Open Telegram and message your bot with `/start`

3. Create your first filter with `/newfilter`

4. View your active filters with `/filters`

## 📊 Available Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Display available commands and usage information
- `/newfilter` - Create a new coin filter with custom criteria
- `/filters` - List all your active filters
- `/editfilter <filter_id>` - Modify an existing filter
- `/deletefilter <filter_id>` - Remove a filter
- `/pause <filter_id>` - Temporarily pause notifications for a filter
- `/resume <filter_id>` - Resume notifications for a paused filter
- `/stats` - View statistics about your filters and notifications

## 🔍 Filter Criteria

You can filter coins based on these parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| Market Cap | Total market capitalization | > $10M and < $100M |
| 24h Volume | Trading volume in the last 24 hours | > $500K |
| Price Change | Percentage change in price | > 5% in 1h |
| Exchanges | Specific exchanges where the coin is listed | Binance, KuCoin |
| Age | How long the coin has been listed | < 7 days |
| Social Media | Social media activity thresholds | > 1000 new followers |
| Custom Metrics | Combine multiple criteria | Volume > 3x average |

## 🔔 Notification Example

When a coin matches your criteria, you'll receive a message like this:

```
🚨 ALERT: New coin matching your filter "Small Cap Gems"

🪙 Coin: ExampleCoin (EXC)
💰 Market Cap: $45,230,000
📈 Price: $0.0432 (+12.5% in 24h)
🔄 24h Volume: $3,245,000
📊 Volume/Market Cap: 0.072
📱 Social Media: +1,500 followers (24h)
🏦 Exchanges: Binance, KuCoin, Gate.io

🔗 More info: https://coingecko.com/en/coins/examplecoin
```

## 🛠️ Advanced Configuration

Edit the `config.json` file to customize:

- Scanning frequency
- Data sources priority
- Notification format
- Maximum alerts per hour
- Default filter templates

## 📦 Project Structure

```
cryptoalert-bot/
├── bot.py                # Main bot entry point
├── config.json           # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── src/
│   ├── filters/          # Filter implementation
│   ├── data/             # Data fetching and processing
│   ├── notifications/    # Telegram notification system
│   ├── commands/         # Bot command handlers
│   ├── storage/          # Database and persistence
│   └── utils/            # Helper utilities
└── tests/                # Unit and integration tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request