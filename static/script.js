// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const greetingElement = document.getElementById('greeting');
    const toolButtons = document.querySelectorAll('.tool-button');
    
    // Hide greeting after 2 seconds or on first interaction
    setTimeout(() => {
        if (greetingElement && !isChatStarted()) {
            greetingElement.style.display = 'none';
        }
    }, 2000);
    
    // Add event listeners to tool buttons
    toolButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const question = this.textContent;
            userInput.value = question;
            sendQuestion(question, category);
        });
    });
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key press
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Function to check if chat has started
    function isChatStarted() {
        return chatMessages.children.length > 0;
    }
    
    // Function to send message
    function sendMessage() {
        const question = userInput.value.trim();
        if (question) {
            const category = 'general'; // Default category
            sendQuestion(question, category);
        }
    }
    
    // Function to actually send the question
    function sendQuestion(question, category) {
        // Clear input
        userInput.value = '';
        
        // Add user message to chat
        addMessageToChat(question, 'user');
        
        // Show typing indicator
        const typingIndicator = addTypingIndicator();
        
        // Send request to backend
        fetch(`/api/consult?question=${encodeURIComponent(question)}&category=${category}`)
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                if (typingIndicator.parentNode) {
                    typingIndicator.parentNode.removeChild(typingIndicator);
                }
                
                // Add AI response to chat
                if (data.error) {
                    addMessageToChat(`Error: ${data.error}`, 'ai');
                } else {
                    addMessageToChat(data.answer, 'ai');
                }
            })
            .catch(error => {
                // Remove typing indicator
                if (typingIndicator.parentNode) {
                    typingIndicator.parentNode.removeChild(typingIndicator);
                }
                
                // Add error message to chat
                addMessageToChat(`Network error: ${error.message}`, 'ai');
            });
    }
    
    // Function to add message to chat
    function addMessageToChat(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageElement.innerHTML = `
            <div class="message-header">
                <span>${sender === 'user' ? 'You' : 'Sethry'}</span>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-content">${formatMessage(message)}</div>
        `;
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to add typing indicator
    function addTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.classList.add('typing-indicator');
        typingElement.id = 'typing-indicator';
        
        typingElement.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span>Thinking...</span>
        `;
        
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return typingElement;
    }
    
    // Function to format message content
    function formatMessage(message) {
        // Convert line breaks to <br> tags and handle long lists properly
        return message.replace(/\n/g, '<br>');
    }
    
    // Initial focus on input field
    userInput.focus();
});
