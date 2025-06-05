document.addEventListener('DOMContentLoaded', function() {
    // Chatbot UI Class
    class ChatbotUI {
        constructor() {
            this.elements = {
                button: document.getElementById('chatbotButton'),
                window: document.getElementById('chatbotWindow'),
                close: document.getElementById('chatbotClose'),
                messages: document.getElementById('chatbotMessages'),
                input: document.getElementById('chatbotInput'),
                send: document.getElementById('chatbotSend')
            };
            this.userId = `user_${Math.random().toString(36).substr(2, 9)}`;
            this.init();
        }

        init() {
            this.elements.button.addEventListener('click', () => this.toggleChat());
            this.elements.close.addEventListener('click', () => this.closeChat());
            this.elements.send.addEventListener('click', () => this.handleSend());
            this.elements.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.handleSend();
            });

            // Initial greeting
            this.addMessage("Hello! I'm your Digital Literacy Assistant. What would you like to learn today?", false, true);
        }

        toggleChat() {
            this.elements.window.classList.toggle('active');
            if (this.elements.window.classList.contains('active')) {
                this.scrollToBottom();
            }
        }

        closeChat() {
            this.elements.window.classList.remove('active');
        }

        async handleSend() {
            const message = this.elements.input.value.trim();
            if (!message) return;

            this.addMessage(message, true);
            this.elements.input.value = '';
            
            this.showTypingIndicator();
            
            try {
                const response = await this.getBotResponse(message);
                this.addMessage(response.text, false);
                
                if (response.tutorials && response.tutorials.length > 0) {
                    this.showTutorials(response.tutorials);
                }
                
                if (response.options && response.options.length > 0) {
                    this.showOptions(response.options);
                }
            } catch (error) {
                this.addMessage("Sorry, I'm having trouble connecting. Please try again later.", false);
                console.error('Chatbot error:', error);
            }
            
            this.hideTypingIndicator();
        }

        async getBotResponse(message) {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    message: message
                })
            });
            return await response.json();
        }

        addMessage(text, isUser, isInitial = false) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
            
            if (isInitial) {
                messageDiv.classList.add('initial-message');
            }
            
            messageDiv.textContent = text;
            this.elements.messages.appendChild(messageDiv);
            this.scrollToBottom();
        }

        showOptions(options) {
            const optionsContainer = document.createElement('div');
            optionsContainer.classList.add('options-container');
            
            options.forEach(option => {
                const button = document.createElement('button');
                button.classList.add('option-button');
                button.textContent = option;
                button.addEventListener('click', () => {
                    this.elements.messages.removeChild(optionsContainer);
                    this.addMessage(option, true);
                    this.handleSend(option);
                });
                optionsContainer.appendChild(button);
            });
            
            this.elements.messages.appendChild(optionsContainer);
            this.scrollToBottom();
        }

        showTutorials(tutorials) {
            const tutorialsContainer = document.createElement('div');
            tutorialsContainer.classList.add('tutorials-container');
            
            const title = document.createElement('h4');
            title.textContent = 'Recommended Tutorials:';
            tutorialsContainer.appendChild(title);
            
            tutorials.forEach(tutorial => {
                const tutorialItem = document.createElement('a');
                tutorialItem.classList.add('tutorial-item');
                tutorialItem.href = typeof tutorial === 'string' ? tutorial : tutorial.url;
                tutorialItem.target = '_blank';
                tutorialItem.textContent = typeof tutorial === 'string' 
                    ? tutorial.split('/').pop().replace(/-/g, ' ')
                    : tutorial.title;
                tutorialsContainer.appendChild(tutorialItem);
            });
            
            this.elements.messages.appendChild(tutorialsContainer);
            this.scrollToBottom();
        }

        showTypingIndicator() {
            const typingDiv = document.createElement('div');
            typingDiv.id = 'typingIndicator';
            typingDiv.classList.add('typing-indicator');
            
            // Create animated dots
            typingDiv.innerHTML = `
                <span>Digital Assistant is typing</span>
                <span class="dot">.</span>
                <span class="dot">.</span>
                <span class="dot">.</span>
            `;
            
            this.elements.messages.appendChild(typingDiv);
            this.scrollToBottom();
        }

        hideTypingIndicator() {
            const typingIndicator = document.getElementById('typingIndicator');
            if (typingIndicator) {
                this.elements.messages.removeChild(typingIndicator);
            }
        }

        scrollToBottom() {
            this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
        }
    }

    // Initialize Chatbot
    const chatbot = new ChatbotUI();

    // Page Interactions
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    window.addEventListener('scroll', () => {
        const nav = document.querySelector('.nav');
        nav.style.background = window.scrollY > 50 ? 
            'rgba(15, 15, 35, 0.95)' : 'rgba(255, 255, 255, 0.1)';
    });
});
