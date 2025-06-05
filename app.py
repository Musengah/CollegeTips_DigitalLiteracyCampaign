from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Knowledge base for the chatbot
knowledge_base = {
    "greetings": {
        "responses": [
            "Hello! I'm your Digital Literacy Assistant. How can I help you today?",
            "Hi there! Ready to learn about WhatsApp, Paytm or Google Maps?",
            "Welcome! Ask me anything about using digital tools like WhatsApp, Paytm or Google Maps."
        ]
    },
    "whatsapp": {
        "faqs": {
            "how to create account": "To create a WhatsApp account:\n1. Download WhatsApp from your app store\n2. Open the app and agree to terms\n3. Verify your phone number via SMS\n4. Set up your profile name and photo",
            "send messages": "To send messages:\n1. Open a chat\n2. Tap the message box\n3. Type your message\n4. Tap the send button (paper plane icon)",
            "make calls": "To make calls:\n1. Open the chat with the person\n2. Tap the phone icon for voice call or video icon for video call\n3. Wait for them to answer",
            "groups": "To create a group:\n1. Tap the 3-dot menu > New group\n2. Select contacts to add\n3. Set a group name and photo\n4. Tap the green checkmark"
        },
        "tutorials": [
            "WhatsApp Basics: https://example.com/whatsapp-basics",
            "Advanced WhatsApp Features: https://example.com/whatsapp-advanced"
        ]
    },
    "paytm": {
        "faqs": {
            "create wallet": "To create Paytm wallet:\n1. Download Paytm app\n2. Sign up with your mobile number\n3. Complete KYC verification\n4. Add money to your wallet",
            "send money": "To send money:\n1. Open Paytm app\n2. Tap 'Pay' or 'Send Money'\n3. Enter recipient mobile number or scan QR\n4. Enter amount and confirm",
            "pay bills": "To pay bills:\n1. Tap 'Electricity', 'Mobile', etc.\n2. Enter your customer ID/phone number\n3. Verify details and enter amount\n4. Confirm payment",
            "bank transfer": "For bank transfer:\n1. Tap 'Bank Transfer'\n2. Select beneficiary or add new\n3. Enter amount and notes\n4. Confirm with UPI PIN"
        },
        "tutorials": [
            "Paytm Wallet Guide: https://example.com/paytm-wallet",
            "UPI Payments: https://example.com/paytm-upi"
        ]
    },
    "google_maps": {
        "faqs": {
            "navigate": "To navigate:\n1. Search for a place or tap on map\n2. Tap 'Directions'\n3. Choose transportation mode\n4. Tap 'Start' to begin navigation",
            "save places": "To save places:\n1. Find a location you like\n2. Tap the name/address at bottom\n3. Tap 'Save' and choose a list\n4. Add to Favorites or custom list",
            "share location": "To share location:\n1. Tap the blue dot (your location)\n2. Tap 'Share your location'\n3. Choose duration and contacts\n4. Tap 'Share'",
            "offline maps": "For offline maps:\n1. Search for an area\n2. Tap the name/address at bottom\n3. Tap 'Download'\n4. Select area and download"
        },
        "tutorials": [
            "Maps Navigation: https://example.com/maps-navigation",
            "Advanced Map Features: https://example.com/maps-advanced"
        ]
    },
    "fallback": [
        "I'm not sure I understand. Could you rephrase that?",
        "I specialize in WhatsApp, Paytm and Google Maps. Could you ask about those?",
        "Here's what I can help with:\n- WhatsApp account setup\n- Paytm payments\n- Google Maps navigation\nWhat would you like to know?"
    ]
}

@app.route('/')
def home():
    return "Digital Literacy Chatbot Backend"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Check for greetings
        if any(word in user_message for word in ['hi', 'hello', 'hey']):
            return jsonify({
                'response': random.choice(knowledge_base['greetings']['responses'])
            })
        
        # Check for WhatsApp queries
        elif 'whatsapp' in user_message:
            for question in knowledge_base['whatsapp']['faqs']:
                if question in user_message:
                    return jsonify({
                        'response': knowledge_base['whatsapp']['faqs'][question],
                        'tutorials': knowledge_base['whatsapp']['tutorials']
                    })
            
            return jsonify({
                'response': "Here are common WhatsApp questions I can answer:\n" + 
                           "\n".join([f"- {q.replace('_', ' ')}" for q in knowledge_base['whatsapp']['faqs'].keys()]),
                'tutorials': knowledge_base['whatsapp']['tutorials']
            })
        
        # Check for Paytm queries
        elif 'paytm' in user_message:
            for question in knowledge_base['paytm']['faqs']:
                if question in user_message:
                    return jsonify({
                        'response': knowledge_base['paytm']['faqs'][question],
                        'tutorials': knowledge_base['paytm']['tutorials']
                    })
            
            return jsonify({
                'response': "Here are common Paytm questions I can answer:\n" + 
                           "\n".join([f"- {q.replace('_', ' ')}" for q in knowledge_base['paytm']['faqs'].keys()]),
                'tutorials': knowledge_base['paytm']['tutorials']
            })
        
        # Check for Google Maps queries
        elif any(term in user_message for term in ['google maps', 'maps', 'navigation']):
            for question in knowledge_base['google_maps']['faqs']:
                if question in user_message:
                    return jsonify({
                        'response': knowledge_base['google_maps']['faqs'][question],
                        'tutorials': knowledge_base['google_maps']['tutorials']
                    })
            
            return jsonify({
                'response': "Here are common Google Maps questions I can answer:\n" + 
                           "\n".join([f"- {q.replace('_', ' ')}" for q in knowledge_base['google_maps']['faqs'].keys()]),
                'tutorials': knowledge_base['google_maps']['tutorials']
            })
        
        # Fallback response
        else:
            return jsonify({
                'response': random.choice(knowledge_base['fallback'])
            })
            
    except Exception as e:
        return jsonify({
            'response': f"Sorry, I encountered an error: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)
