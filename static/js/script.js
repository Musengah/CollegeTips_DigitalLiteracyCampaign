// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.nav');
    nav.style.background = window.scrollY > 50 ? 
        'rgba(15, 15, 35, 0.95)' : 'rgba(255, 255, 255, 0.1)';
});

// Chatbot functionality
const chatbotButton = document.getElementById('chatbotButton');
const chatbotWindow = document.getElementById('chatbotWindow');
const chatbotClose = document.getElementById('chatbotClose');
const chatbotMessages = document.getElementById('chatbotMessages');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');

// Toggle chatbot window
chatbotButton.addEventListener('click', () => {
    chatbotWindow.classList.toggle('active');
    if (chatbotWindow.classList.contains('active')) {
        // Add welcome message when first opened
        if (chatbotMessages.children.length <= 1) { // Only if empty (1 is sample message)
            addMessage("Hello! I'm your Digital Literacy Assistant. Ask me about WhatsApp, Paytm or Google Maps!", false);
        }
    }
});

// Close chatbot window
chatbotClose.addEventListener('click', () => {
    chatbotWindow.classList.remove('active');
});

// Add message to chat
function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Send message to Flask backend
async function sendToBackend(message) {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return { response: "Sorry, I'm having trouble connecting to the server." };
    }
}

// Handle send button click
chatbotSend.addEventListener('click', async () => {
    const message = chatbotInput.value.trim();
    if (message) {
        addMessage(message, true);
        chatbotInput.value = '';
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.id = 'typingIndicator';
        typingIndicator.textContent = 'Digital Assistant is typing...';
        typingIndicator.style.color = '#666';
        typingIndicator.style.fontStyle = 'italic';
        typingIndicator.style.margin = '0.5rem 1rem';
        chatbotMessages.appendChild(typingIndicator);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        
        // Get response from backend
        const botResponse = await sendToBackend(message);
        
        // Remove typing indicator
        document.getElementById('typingIndicator').remove();
        
        // Add bot response
        addMessage(botResponse.response, false);
        
        // Add tutorials if available
        if (botResponse.tutorials) {
            const tutorialsDiv = document.createElement('div');
            tutorialsDiv.classList.add('message', 'bot-message');
            tutorialsDiv.innerHTML = '<strong>Tutorials:</strong><br>' + 
                botResponse.tutorials.map(t => `• <a href="${t}" target="_blank">${t.split('/').pop().replace('-', ' ')}</a>`).join('<br>');
            chatbotMessages.appendChild(tutorialsDiv);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
    }
});

// Handle Enter key
chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        chatbotSend.click();
    }
});
