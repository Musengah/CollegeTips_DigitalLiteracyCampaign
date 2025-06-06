from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Enhanced knowledge base with complete coverage
KNOWLEDGE_BASE = {
    "whatsapp": {
        "account": {
            "keywords": ["account", "sign up", "register", "create"],
            "response": """To create a WhatsApp account:
1. Download WhatsApp from your app store
2. Open and verify your phone number
3. Set up your profile name and photo

Official guide: https://faq.whatsapp.com/131834966250626"""
        },
        "security": {
            "keywords": ["security", "safe", "private", "encryption"],
            "response": """WhatsApp security features:
• End-to-end encrypted messages
• Two-step verification (Settings > Account)
• Fingerprint/Face ID lock
• Block and report contacts

Security tips: https://faq.whatsapp.com/2119723580235892"""
        },
        "backup": {
            "keywords": ["backup", "restore", "chats"],
            "response": """To backup WhatsApp chats:
1. Go to Settings > Chats > Chat backup
2. Choose backup frequency
3. Select Google Drive/iCloud
4. Tap 'BACK UP'

Note: Media backups use phone storage
Guide: https://faq.whatsapp.com/1180414119172465"""
        }
    },
    "paytm": {
        "wallet": {
            "keywords": ["wallet", "money", "create"],
            "response": """To create Paytm wallet:
1. Download Paytm app
2. Complete KYC verification
3. Add money via bank/UPI/card
4. Set UPI PIN for payments

KYC requirements: https://paytm.com/support/knowledge-base/"""
        },
        "upi": {
            "keywords": ["upi", "pin", "payment"],
            "response": """To set UPI PIN:
1. Go to Payments > UPI & Payment Settings
2. Select your bank account
3. Enter debit card details
4. Create 4-6 digit PIN

Important: Never share your UPI PIN"""
        },
        "bills": {
            "keywords": ["bill", "electricity", "recharge"],
            "response": """Pay bills on Paytm:
1. Select bill type (electricity/mobile)
2. Enter customer/phone number
3. Verify details and amount
4. Choose payment method

Supported services: https://paytm.com/bills-payment"""
        }
    },
    "maps": {
        "navigation": {
            "keywords": ["navigate", "directions", "route"],
            "response": """Get directions:
1. Search for destination
2. Tap 'Directions' (blue button)
3. Choose travel mode
4. Tap 'Start' for navigation

Pro tip: Use voice command 'Navigate to [place]'"""
        },
        "offline": {
            "keywords": ["offline", "download", "map"],
            "response": """Download offline maps:
1. Search for area (e.g., "Mumbai")
2. Tap place name at bottom
3. Select 'Download'
4. Adjust map area

Guide: https://support.google.com/maps/answer/6291838"""
        },
        "sharing": {
            "keywords": ["share", "location", "live"],
            "response": """Share real-time location:
1. Tap blue dot (your location)
2. Select 'Share your location'
3. Choose contacts/duration
4. Tap 'Share'

Safety: Use temporary sharing for meetups"""
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

    # Greetings
    if not user_message or any(greet in user_message for greet in ['hi','hello','hey']):
        response["text"] = "Hello! I can help with:\n- WhatsApp\n- Paytm\n- Google Maps\nWhat do you need?"
        return jsonify(response)

    # Check all services
    for service in ["whatsapp", "paytm", "maps"]:
        if service in user_message:
            for topic, data in KNOWLEDGE_BASE[service].items():
                if any(keyword in user_message for keyword in data["keywords"]):
                    response["text"] = data["response"]
                    return jsonify(response)
            
            # If service matched but no specific topic
            topics = "\n- ".join([t for t in KNOWLEDGE_BASE[service].keys()])
            response["text"] = f"For {service.capitalize()}, I can help with:\n- {topics}\nWhat specifically do you need?"
            return jsonify(response)

    # Fallback
    response["text"] = "I can help with:\n- WhatsApp (account, security)\n- Paytm (wallet, UPI)\n- Google Maps (navigation)\nWhat do you need?"
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
