from flask import Flask, request, jsonify, render_template
import random
import re
from datetime import datetime

app = Flask(__name__)

class DigitalLiteracyChatbot:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.user_sessions = {}
        self.current_tutorials = {}

    def _load_knowledge_base(self):
        return {
            "greetings": {
                "patterns": ["hi", "hello", "hey", "greetings"],
                "responses": [
                    "Hello! I'm your Digital Literacy Assistant. What would you like to learn today?",
                    "Hi there! Ready to master WhatsApp, Paytm or Google Maps?",
                    "Welcome! I can help with WhatsApp, Paytm, and Google Maps. What do you need?"
                ]
            },
            "whatsapp": {
                "faqs": {
                    "account": {
                        "questions": ["create account", "sign up", "register"],
                        "answer": """To create a WhatsApp account:
1. Download WhatsApp from your app store
2. Open and agree to terms
3. Verify your phone number via SMS
4. Set up your profile""",
                        "follow_up": "Would you like to know about WhatsApp security features next?"
                    },
                    "security": {
                        "questions": ["security", "privacy", "safe"],
                        "answer": """WhatsApp security features:
• End-to-end encryption
• Two-step verification
• Privacy settings for last seen/profile photo
• Block unwanted contacts""",
                        "tutorials": [
                            "WhatsApp Security Guide: https://example.com/whatsapp-security",
                            "Privacy Settings: https://example.com/whatsapp-privacy"
                        ]
                    }
                },
                "tutorials": [
                    {"title": "WhatsApp Basics", "url": "https://example.com/whatsapp-basics", "steps": 5},
                    {"title": "Business Features", "url": "https://example.com/whatsapp-business", "steps": 7}
                ]
            },

            "paytm": {
                "faqs": {
                    "wallet": {
                        "questions": ["create wallet", "set up wallet", "wallet"],
                        "answer": """To create Paytm wallet:
1. Download Paytm app
2. Sign up with mobile number
3. Complete KYC verification
4. Add money to wallet""",
                        "follow_up": "Would you like to know how to secure your Paytm wallet?"
                    },
                    "security": {
                    "questions": ["secure", "safety", "protection"],
                    "answer": """Paytm security features:
• UPI PIN protection
• Transaction alerts
• Biometric login
• Device binding""",
                        "tutorials": [
                            "Paytm Security Guide: https://example.com/paytm-security",
                            "UPI Safety: https://example.com/paytm-upi-safety"
                        ]
                    }
                },
    "tutorials": [
        {"title": "Paytm Wallet Guide", "url": "https://example.com/paytm-wallet", "steps": 6},
        {"title": "UPI Payments", "url": "https://example.com/paytm-upi", "steps": 4}
    ]
},
"google_maps": {
    "faqs": {
        "navigation": {
            "questions": ["navigate", "directions", "route"],
            "answer": """To get directions:
1. Search for a place
2. Tap 'Directions'
3. Choose transport mode
4. Tap 'Start'""",
            "follow_up": "Would you like to learn about offline maps?"
        },
        "offline": {
            "questions": ["offline", "download map"],
            "answer": """Using offline maps:
1. Search for an area
2. Tap location name
3. Tap 'Download'
4. Select area""",
            "tutorials": [
                "Offline Maps Guide: https://example.com/maps-offline",
                "Data Saving Tips: https://example.com/maps-data-saving"
            ]
        }
    },
    "tutorials": [
        {"title": "Navigation Basics", "url": "https://example.com/maps-navigation", "steps": 5},
        {"title": "Advanced Features", "url": "https://example.com/maps-advanced", "steps": 8}
    ]
}
            # Similar expanded structures for Paytm and Google Maps...
            "fallback": [
                "I'm not sure I understand. Could you ask about WhatsApp, Paytm or Google Maps?",
                "I specialize in digital tools. Try asking about WhatsApp payments or Maps navigation!",
                "Here's what I can help with:\n- WhatsApp setup\n- Paytm wallet\n- Maps offline usage"
            ]
        }

    def process_message(self, user_id, message):
        message = message.lower()
        response = {
            "text": "",
            "options": [],
            "tutorials": []
        }

        # Check for greetings
        if any(word in message for word in self.knowledge_base["greetings"]["patterns"]):
            response["text"] = random.choice(self.knowledge_base["greetings"]["responses"])
            response["options"] = ["WhatsApp", "Paytm", "Google Maps"]
            return response

        # Check for WhatsApp queries
        if "whatsapp" in message:
            for faq in self.knowledge_base["whatsapp"]["faqs"].values():
                if any(q in message for q in faq["questions"]):
                    response["text"] = faq["answer"]
                    if "follow_up" in faq:
                        response["options"] = ["Yes", "No"]
                        self.user_sessions[user_id] = {"follow_up": "whatsapp:security"}
                    if "tutorials" in faq:
                        response["tutorials"] = faq["tutorials"]
                    return response
            
            response["text"] = "Here are WhatsApp topics I can help with:"
            response["options"] = [topic for topic in self.knowledge_base["whatsapp"]["faqs"].keys()]
            response["tutorials"] = [tut["title"] for tut in self.knowledge_base["whatsapp"]["tutorials"]]
            return response

        # Handle follow-up questions
        if user_id in self.user_sessions and "follow_up" in self.user_sessions[user_id]:
            if "yes" in message:
                topic = self.user_sessions[user_id]["follow_up"].split(":")[1]
                response["text"] = self.knowledge_base["whatsapp"]["faqs"][topic]["answer"]
                if "tutorials" in self.knowledge_base["whatsapp"]["faqs"][topic]:
                    response["tutorials"] = self.knowledge_base["whatsapp"]["faqs"][topic]["tutorials"]
                del self.user_sessions[user_id]["follow_up"]
                return response

        # Fallback response
        response["text"] = random.choice(self.knowledge_base["fallback"])
        response["options"] = ["WhatsApp", "Paytm", "Google Maps"]
        return response

chatbot = DigitalLiteracyChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id', 'default')
    message = data.get('message', '')
    
    response = chatbot.process_message(user_id, message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
