class DentalVoiceAgent {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isRecording = false;
        this.isSpeaking = false;
        
        this.initializeSpeechRecognition();
        this.bindEvents();
    }

    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.updateVoiceButton(true);
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.processUserInput(transcript);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.showNotification('Speech recognition error. Please try again.', 'error');
                this.updateVoiceButton(false);
            };
            
            this.recognition.onend = () => {
                this.isRecording = false;
                this.updateVoiceButton(false);
            };
        } else {
            this.showNotification('Speech recognition not supported in this browser.', 'error');
        }
    }

    bindEvents() {
        // Voice button
        const voiceButton = document.getElementById('voiceButton');
        voiceButton.addEventListener('click', () => this.toggleVoiceRecording());

        // Text input
        const textInput = document.getElementById('textInput');
        const sendButton = document.getElementById('sendButton');
        
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.processUserInput(textInput.value);
                textInput.value = '';
            }
        });
        
        sendButton.addEventListener('click', () => {
            this.processUserInput(textInput.value);
            textInput.value = '';
        });

        // Quick action buttons
        const actionButtons = document.querySelectorAll('.action-btn');
        actionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const query = button.getAttribute('data-query');
                this.processUserInput(query);
            });
        });

        // Clear chat
        const clearButton = document.getElementById('clearChat');
        clearButton.addEventListener('click', () => this.clearConversation());
    }

    toggleVoiceRecording() {
        if (!this.recognition) {
            this.showNotification('Speech recognition not available.', 'error');
            return;
        }

        if (this.isRecording) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }

    updateVoiceButton(recording) {
        const voiceButton = document.getElementById('voiceButton');
        const voiceStatus = document.getElementById('voiceStatus');
        const pulseRing = voiceStatus.querySelector('.pulse-ring');
        
        if (recording) {
            voiceButton.classList.add('recording');
            voiceButton.innerHTML = '<i class="fas fa-stop"></i><span>Stop Recording</span>';
            pulseRing.classList.add('active');
        } else {
            voiceButton.classList.remove('recording');
            voiceButton.innerHTML = '<i class="fas fa-microphone"></i><span>Click to Speak</span>';
            pulseRing.classList.remove('active');
        }
    }

    async processUserInput(input) {
        if (!input.trim()) return;

        // Add user message to conversation
        this.addMessage(input, 'user');

        // Show loading indicator
        const loadingMessage = this.addLoadingMessage();

        try {
            const response = await fetch('/api/process-voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: input })
            });

            const data = await response.json();

            if (response.ok) {
                // Remove loading message
                loadingMessage.remove();
                
                // Add AI response
                this.addMessage(data.response, 'assistant');
                
                // Speak the response
                this.speakText(data.response);
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error processing input:', error);
            loadingMessage.remove();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            this.showNotification('Error processing request. Please try again.', 'error');
        }
    }

    addMessage(content, sender) {
        const conversation = document.getElementById('conversation');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const icon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<i class="${icon}"></i><p>${content}</p>`;
        
        messageDiv.appendChild(messageContent);
        conversation.appendChild(messageDiv);
        
        // Scroll to bottom
        conversation.scrollTop = conversation.scrollHeight;
        
        return messageDiv;
    }

    addLoadingMessage() {
        const conversation = document.getElementById('conversation');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = '<i class="fas fa-robot"></i><div class="loading"></div>';
        
        messageDiv.appendChild(messageContent);
        conversation.appendChild(messageDiv);
        
        conversation.scrollTop = conversation.scrollHeight;
        return messageDiv;
    }

    speakText(text) {
        console.log('Attempting to speak text:', text);
        
        if (this.isSpeaking) {
            console.log('Cancelling previous speech');
            this.synthesis.cancel();
        }

        // Check if speech synthesis is available
        if (!this.synthesis) {
            console.error('Speech synthesis not available');
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        
        utterance.onstart = () => {
            console.log('Speech started');
            this.isSpeaking = true;
        };
        
        utterance.onend = () => {
            console.log('Speech ended');
            this.isSpeaking = false;
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.isSpeaking = false;
        };
        
        console.log('Starting speech synthesis...');
        this.synthesis.speak(utterance);
    }

    clearConversation() {
        const conversation = document.getElementById('conversation');
        conversation.innerHTML = `
            <div class="message assistant">
                <div class="message-content">
                    <i class="fas fa-robot"></i>
                    <p>Hello! I'm your AI dental assistant. I can help you with:</p>
                    <ul>
                        <li>📅 Scheduling appointments</li>
                        <li>🏥 Insurance questions</li>
                        <li>🦷 Service information</li>
                        <li>⏰ Office hours</li>
                    </ul>
                    <p>Just click the microphone button and ask me anything!</p>
                </div>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ff6b6b' : '#667eea'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize the voice agent when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dentalVoiceAgent = new DentalVoiceAgent();
    
    // Add some helpful tips
    console.log('Dental Voice Agent initialized!');
    console.log('Features:');
    console.log('- Voice recognition for hands-free interaction');
    console.log('- Text input for typing questions');
    console.log('- Quick action buttons for common queries');
    console.log('- Text-to-speech for AI responses');
    console.log('- Appointment scheduling assistance');
    console.log('- Insurance information lookup');
});
