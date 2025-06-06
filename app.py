from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Real-world knowledge base with actual steps and official resources
KNOWLEDGE_BASE = {
    "whatsapp": {
        "create_account": {
            "answer": """To create a WhatsApp account:
1. Download WhatsApp from Play Store/App Store
2. Open and accept Terms of Service
3. Verify your phone number via SMS/call
4. Set up your profile name and photo

Official Guide: https://faq.whatsapp.com/131834966250626""",
            "related": ["security", "backup"]
        },
        "security": {
            "answer": """WhatsApp security features:
• End-to-end encryption (all chats)
• Two-step verification (Settings > Account)
• Fingerprint/Face ID lock (iOS/Android)
• Block and report contacts

Enable 2FA: https://faq.whatsapp.com/2128813922059005""",
            "related": ["backup", "privacy"]
        },
        "backup": {
            "answer": """To backup chats:
1. Go to Settings > Chats > Chat backup
2. Choose backup frequency (daily/weekly)
3. Select Google Drive/iCloud backup
4. Tap 'BACK UP'

Note: Backups don't include payment messages
Guide: https://faq.whatsapp.com/1180414119172465"""
        }
    },
    "paytm": {
        "create_wallet": {
            "answer": """To create Paytm wallet:
1. Download Paytm app
2. Sign up with mobile number
3. Complete KYC (PAN card required)
4. Add money via bank/UPI/card

KYC Guide: https://paytm.com/support/knowledge-base/""",
            "related": ["security", "upipin"]
        },
        "upipin": {
            "answer": """To set UPI PIN:
1. Go to 'Payments' > 'UPI & Payment Settings'
2. Select your bank account
3. Choose 'Set UPI PIN'
4. Enter debit card details
5. Create 4-6 digit PIN

Important: Never share your UPI PIN"""
        },
        "electricity_bill": {
            "answer": """Pay electricity bill:
1. Open Paytm > 'Electricity'
2. Select your state/board
3. Enter consumer number
4. Verify details and amount
5. Choose payment method

Supported boards: https://paytm.com/electricity-bill-payment"""
        }
    },
    "google_maps": {
        "navigation": {
            "answer": """Get directions:
1. Search for destination
2. Tap 'Directions' (blue button)
3. Choose travel mode (car/bus/walk)
4. Tap 'Start' to begin navigation

Pro tip: Say 'OK Google, navigate to [place]'"""
        },
        "offline_maps": {
            "answer": """Download offline maps:
1. Search for area (e.g., "New York")
2. Tap place name at bottom
3. Select 'Download'
4. Adjust map area and download

Note: Requires Google account
Guide: https://support.google.com/maps/answer/6291838"""
        },
        "share_location": {
            "answer": """Share real-time location:
1. Tap blue dot (your location)
2. Select 'Share your location'
3. Choose contacts/duration
4. Tap 'Share'

Safety tip: Use temporary sharing for meetups"""
        }
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    response = {"text": "", "links": []}

    # Check for greetings
    if any(greet in user_message for greet in ['hi','hello','hey']):
        response["text"] = "Hello! I can help with:\n- WhatsApp\n- Paytm\n- Google Maps\nWhat do you need?"
        return jsonify(response)

    # WhatsApp queries
    if 'whatsapp' in user_message:
        if 'account' in user_message or 'create' in user_message:
            response.update(KNOWLEDGE_BASE["whatsapp"]["create_account"])
        elif 'security' in user_message or 'safe' in user_message:
            response.update(KNOWLEDGE_BASE["whatsapp"]["security"])
        elif 'backup' in user_message:
            response.update(KNOWLEDGE_BASE["whatsapp"]["backup"])
        else:
            response["text"] = "I can help with WhatsApp:\n- Account setup\n- Security\n- Backups\nWhat do you need?"

    # Paytm queries
    elif 'paytm' in user_message:
        if 'wallet' in user_message or 'create' in user_message:
            response.update(KNOWLEDGE_BASE["paytm"]["create_wallet"])
        elif 'upi' in user_message or 'pin' in user_message:
            response.update(KNOWLEDGE_BASE["paytm"]["upipin"])
        elif 'bill' in user_message or 'electricity' in user_message:
            response.update(KNOWLEDGE_BASE["paytm"]["electricity_bill"])
        else:
            response["text"] = "I can help with Paytm:\n- Wallet creation\n- UPI PIN\n- Bill payments\nWhat do you need?"

    # Google Maps queries
    elif 'maps' in user_message or 'google' in user_message:
        if 'navigate' in user_message or 'directions' in user_message:
            response.update(KNOWLEDGE_BASE["google_maps"]["navigation"])
        elif 'offline' in user_message or 'download' in user_message:
            response.update(KNOWLEDGE_BASE["google_maps"]["offline_maps"])
        elif 'share' in user_message or 'location' in user_message:
            response.update(KNOWLEDGE_BASE["google_maps"]["share_location"])
        else:
            response["text"] = "I can help with Google Maps:\n- Navigation\n- Offline maps\n- Location sharing\nWhat do you need?"

    # Fallback response
    else:
        response["text"] = "I specialize in:\n- WhatsApp\n- Paytm\n- Google Maps\nTry asking about those!"

    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
