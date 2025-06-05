document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

const chatbotButton = document.getElementById('chatbotButton');
const chatbotWindow = document.getElementById('chatbotWindow');
const chatbotClose = document.getElementById('chatbotClose');
const chatbotMessages = document.getElementById('chatbotMessages');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');

chatbotButton.addEventListener('click', () => {
    chatbotWindow.classList.toggle('active');
});

chatbotClose.addEventListener('click', () => {
    chatbotWindow.classList.remove('active');
});

function getBotResponse(userMessage) {
    const responses = [
        "I can provide information about our digital literacy courses.",
        "Our courses cover WhatsApp, Paytm, and Google Maps.",
        "You can start any course by clicking the 'Start Course' button.",
        "The WhatsApp course teaches messaging, media sharing, and more.",
        "The Paytm course covers digital payments and financial management.",
        "The Google Maps course helps with navigation and location services.",
        "You can scroll up to see our course offerings.",
        "Let me know if you have any specific questions!"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
}

function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

chatbotSend.addEventListener('click', () => {
    const message = chatbotInput.value.trim();
    if (message) {
        addMessage(message, true);
        chatbotInput.value = '';

        setTimeout(() => {
            addMessage(getBotResponse(message), false);
        }, 1000);
    }
});

chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        chatbotSend.click();
    }
});