from flask import Flask, request, jsonify, render_template
import random
import re
from datetime import datetime

app = Flask(__name__)

class DigitalLiteracyChatbot:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.user_sessions = {}

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
                        "follow_up": "would you like to know about WhatsApp security features next?"
                    },
                    "security": {
                        "questions": ["security", "privacy", "safe"],
                        "answer": """WhatsApp security features:
• End-to-end encryption
• Two-step verification
• Privacy settings for last seen/profile photo
• Block unwanted contacts""",
                        "tutorials": [
                            {"title": "WhatsApp Security Guide", "url": "https://example.com/whatsapp-security"},
                            {"title": "Privacy Settings", "url": "https://example.com/whatsapp-privacy"}
                        ]
                    },
                    "groups": {
                        "questions": ["create group", "group chat", "group settings"],
                        "answer": """To create a WhatsApp group:
1. Tap the 3-dot menu > New group
2. Select contacts to add
3. Set a group name and photo
4. Tap the green checkmark""",
                        "tutorials": [
                            {"title": "Group Management", "url": "https://example.com/whatsapp-groups"}
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
                        "follow_up": "would you like to know how to secure your Paytm wallet?"
                    },
                    "security": {
                        "questions": ["secure", "safety", "protection"],
                        "answer": """Paytm security features:
• UPI PIN protection
• Transaction alerts
• Biometric login
• Device binding""",
                        "tutorials": [
                            {"title": "Paytm Security Guide", "url": "https://example.com/paytm-security"},
                            {"title": "UPI Safety", "url": "https://example.com/paytm-upi-safety"}
                        ]
                    },
                    "payments": {
                        "questions": ["send money", "make payment", "transfer"],
                        "answer": """To send money with Paytm:
1. Open Paytm app
2. Tap 'Pay' or 'Send Money'
3. Enter recipient details
4. Enter amount and confirm""",
                        "tutorials": [
                            {"title": "UPI Payments", "url": "https://example.com/paytm-upi"}
                        ]
                    }
                },
                "tutorials": [
                    {"title": "Paytm Wallet Guide", "url": "https://example.com/paytm-wallet", "steps": 6},
                    {"title": "Bill Payments", "url": "https://example.com/paytm-bills", "steps": 4}
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
                        "follow_up": "would you like to learn about offline maps?"
                    },
                    "offline": {
                        "questions": ["offline", "download map"],
                        "answer": """Using offline maps:
1. Search for an area
2. Tap location name
3. Tap 'Download'
4. Select area""",
                        "tutorials": [
                            {"title": "Offline Maps Guide", "url": "https://example.com/maps-offline"},
                            {"title": "Data Saving Tips", "url": "https://example.com/maps-data-saving"}
                        ]
                    },
                    "sharing": {
                        "questions": ["share location", "send location"],
                        "answer": """To share your location:
1. Tap the blue dot (your location)
2. Tap 'Share your location'
3. Choose duration and contacts
4. Tap 'Share'""",
                        "tutorials": [
                            {"title": "Location Sharing", "url": "https://example.com/maps-sharing"}
                        ]
                    }
                },
                "tutorials": [
                    {"title": "Navigation Basics", "url": "https://example.com/maps-navigation", "steps": 5},
                    {"title": "Advanced Features", "url": "https://example.com/maps-advanced", "steps": 8}
                ]
            },
            "fallback": [
                "I'm not sure I understand. Could you ask about WhatsApp, Paytm or Google Maps?",
                "I specialize in digital tools. Try asking about WhatsApp payments or Maps navigation!",
                "Here's what I can help with:\n- WhatsApp setup\n- Paytm wallet\n- Maps offline usage"
            ]
        }

    def process_message(self, user_id, message):
        message = message.lower().strip()
        response = {
            "text": "",
            "options": [],
            "tutorials": []
        }

        # Check greetings
        if any(word in message for word in self.knowledge_base["greetings"]["patterns"]):
            response["text"] = random.choice(self.knowledge_base["greetings"]["responses"])
            response["options"] = ["WhatsApp", "Paytm", "Google Maps"]
            return response

        # Check if handling follow-up
        if user_id in self.user_sessions and "pending_follow_up" in self.user_sessions[user_id]:
            topic, follow_up_key = self.user_sessions[user_id]["pending_follow_up"]
            if "yes" in message:
                follow_up = self.knowledge_base[topic]["faqs"][follow_up_key]
                response["text"] = follow_up["answer"]
                if "tutorials" in follow_up:
                    response["tutorials"] = follow_up["tutorials"]
                del self.user_sessions[user_id]["pending_follow_up"]
                return response
            else:
                del self.user_sessions[user_id]["pending_follow_up"]

        # Check WhatsApp queries
        if "whatsapp" in message:
            return self._handle_topic_query("whatsapp", message, user_id)

        # Check Paytm queries
        if "paytm" in message:
            return self._handle_topic_query("paytm", message, user_id)

        # Check Google Maps queries
        if any(term in message for term in ["google maps", "maps", "navigation"]):
            return self._handle_topic_query("google_maps", message, user_id)

        # Fallback response
        response["text"] = random.choice(self.knowledge_base["fallback"])
        response["options"] = ["WhatsApp", "Paytm", "Google Maps"]
        return response

    def _handle_topic_query(self, topic, message, user_id):
        response = {
            "text": "",
            "options": [],
            "tutorials": []
        }

        # Check FAQs
        for faq_key, faq in self.knowledge_base[topic]["faqs"].items():
            if any(q in message for q in faq["questions"]):
                response["text"] = faq["answer"]
                if "follow_up" in faq:
                    self.user_sessions[user_id] = {"pending_follow_up": (topic, faq_key)}
                    response["options"] = ["Yes", "No"]
                if "tutorials" in faq:
                    response["tutorials"] = faq["tutorials"]
                return response

        # Show topic options if no specific FAQ matched
        response["text"] = f"Here are {topic.replace('_', ' ')} topics I can help with:"
        response["options"] = list(self.knowledge_base[topic]["faqs"].keys())
        response["tutorials"] = self.knowledge_base[topic]["tutorials"]
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
