/**
 * BotInterface - Frontend JavaScript
 * Handles chat interface, API calls, and UI interactions
 */

// State management
const state = {
    messages: [],
    isLoading: false,
    sessionId: null
};

// DOM Elements
const elements = {
    emptyState: null,
    chatContainer: null,
    messagesWrapper: null,
    messageInput: null,
    sendBtn: null,
    newChatBtn: null,
    settingsBtn: null,
    loadingIndicator: null,
    errorAlert: null,
    errorMessage: null,
    errorDetails: null,
    retryBtn: null
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    attachEventListeners();
    loadChatHistory();
    
    // Focus on input
    elements.messageInput.focus();
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    elements.emptyState = document.getElementById('emptyState');
    elements.chatContainer = document.getElementById('chatContainer');
    elements.messagesWrapper = document.getElementById('messagesWrapper');
    elements.messageInput = document.getElementById('messageInput');
    elements.sendBtn = document.getElementById('sendBtn');
    elements.newChatBtn = document.getElementById('newChatBtn');
    elements.settingsBtn = document.getElementById('settingsBtn');
    elements.loadingIndicator = document.getElementById('loadingIndicator');
    elements.errorAlert = document.getElementById('errorAlert');
    elements.errorMessage = document.getElementById('errorMessage');
    elements.errorDetails = document.getElementById('errorDetails');
    elements.retryBtn = document.getElementById('retryBtn');
}

/**
 * Attach event listeners
 */
function attachEventListeners() {
    // Send message on button click
    elements.sendBtn.addEventListener('click', handleSendMessage);
    
    // Send message on Enter (Shift+Enter for new line)
    elements.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // Auto-resize textarea
    elements.messageInput.addEventListener('input', () => {
        autoResizeTextarea();
    });
    
    // New chat button
    elements.newChatBtn.addEventListener('click', startNewChat);
    
    // Settings button
    elements.settingsBtn.addEventListener('click', () => {
        alert('Paramètres - Fonctionnalité à venir !');
    });
    
    // Retry button
    elements.retryBtn.addEventListener('click', () => {
        hideError();
        const lastUserMessage = state.messages.filter(m => m.role === 'user').pop();
        if (lastUserMessage) {
            sendMessageToBot(lastUserMessage.content);
        }
    });
}

/**
 * Auto-resize textarea based on content
 */
function autoResizeTextarea() {
    const textarea = elements.messageInput;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
}

/**
 * Handle send message action
 */
async function handleSendMessage() {
    const message = elements.messageInput.value.trim();
    
    // Validate message
    if (!message || state.isLoading) {
        return;
    }
    
    // Clear input
    elements.messageInput.value = '';
    elements.messageInput.style.height = 'auto';
    
    // Hide empty state and show chat
    if (elements.emptyState && !elements.emptyState.classList.contains('hidden')) {
        elements.emptyState.classList.add('hidden');
        elements.chatContainer.classList.add('active');
    }
    
    // Add user message to UI
    addMessage('user', message);
    
    // Send to bot
    await sendMessageToBot(message);
}

/**
 * Send message to bot API
 */
async function sendMessageToBot(message) {
    // Set loading state
    state.isLoading = true;
    setInputState(false);
    showLoading();
    hideError();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: state.sessionId
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Update session ID if provided
        if (data.session_id) {
            state.sessionId = data.session_id;
        }
        
        // Add bot response to UI
        if (data.reply) {
            addMessage('assistant', data.reply);
        } else {
            throw new Error('Aucune réponse du bot');
        }
        
    } catch (error) {
        console.error('Erreur lors de l\'envoi du message:', error);
        showError(error.message, error.stack || 'Aucun détail supplémentaire');
    } finally {
        // Reset loading state
        state.isLoading = false;
        setInputState(true);
        hideLoading();
    }
}

/**
 * Add message to chat UI
 */
function addMessage(role, content) {
    const message = {
        role: role,
        content: content,
        timestamp: new Date()
    };
    
    state.messages.push(message);
    
    const messageElement = createMessageElement(message);
    
    // Ensure messages wrapper exists and is ready
    if (elements.messagesWrapper) {
        elements.messagesWrapper.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
    }
}

/**
 * Create message DOM element
 */
function createMessageElement(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${message.role}`;
    
    if (message.role === 'assistant') {
        // Bot message with avatar
        const avatar = document.createElement('div');
        avatar.className = 'bot-avatar';
        avatar.innerHTML = '<span>B</span>';
        messageDiv.appendChild(avatar);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = message.content;
    contentDiv.appendChild(textDiv);
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = formatTimestamp(message.timestamp, message.role);
    contentDiv.appendChild(timestamp);
    
    messageDiv.appendChild(contentDiv);
    
    return messageDiv;
}

/**
 * Format timestamp for display
 */
function formatTimestamp(date, role) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const time = `${hours}:${minutes}`;
    const prefix = role === 'user' ? 'Vous' : 'Bot';
    return `${prefix} · ${time}`;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        setTimeout(() => {
            mainContent.scrollTop = mainContent.scrollHeight;
        }, 100);
    }
}

/**
 * Show loading indicator
 */
function showLoading() {
    if (elements.loadingIndicator) {
        elements.loadingIndicator.style.display = 'flex';
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    if (elements.loadingIndicator) {
        elements.loadingIndicator.style.display = 'none';
    }
}

/**
 * Show error alert
 */
function showError(message, details) {
    if (elements.errorAlert) {
        elements.errorMessage.textContent = message;
        elements.errorDetails.textContent = details;
        elements.errorAlert.style.display = 'block';
    }
}

/**
 * Hide error alert
 */
function hideError() {
    if (elements.errorAlert) {
        elements.errorAlert.style.display = 'none';
    }
}

/**
 * Set input state (enabled/disabled)
 */
function setInputState(enabled) {
    elements.messageInput.disabled = !enabled;
    elements.sendBtn.disabled = !enabled;
    
    if (enabled) {
        elements.messageInput.focus();
    }
}

/**
 * Start a new chat session
 */
function startNewChat() {
    if (state.messages.length === 0) {
        return;
    }
    
    if (confirm('Voulez-vous vraiment démarrer une nouvelle conversation ? Les messages actuels seront effacés.')) {
        // Clear state completely
        state.messages = [];
        state.sessionId = null;
        state.isLoading = false;
        
        // Clear UI - force remove all message elements
        if (elements.messagesWrapper) {
            // Remove all child nodes
            while (elements.messagesWrapper.firstChild) {
                elements.messagesWrapper.removeChild(elements.messagesWrapper.firstChild);
            }
        }
        
        // Reset chat container visibility
        if (elements.chatContainer) {
            elements.chatContainer.classList.remove('active');
        }
        
        // Show empty state
        if (elements.emptyState) {
            elements.emptyState.classList.remove('hidden');
        }
        
        // Hide any errors or loading states
        hideError();
        hideLoading();
        
        // Reset input
        if (elements.messageInput) {
            elements.messageInput.value = '';
            elements.messageInput.style.height = 'auto';
            elements.messageInput.disabled = false;
        }
        
        // Reset send button
        if (elements.sendBtn) {
            elements.sendBtn.disabled = false;
        }
        
        // Clear session storage if exists
        try {
            sessionStorage.removeItem('bot4univ_session');
        } catch (e) {
            console.log('Session storage not available');
        }
        
        // Focus input for new conversation
        setTimeout(() => {
            if (elements.messageInput) {
                elements.messageInput.focus();
            }
        }, 100);
        
        console.log('[NEW CHAT] Session complètement réinitialisée');
    }
}

/**
 * Load chat history from API
 */
async function loadChatHistory() {
    try {
        const response = await fetch('/api/history');
        
        if (!response.ok) {
            console.warn('Impossible de charger l\'historique');
            return;
        }
        
        const data = await response.json();
        
        if (data.messages && data.messages.length > 0) {
            // Hide empty state
            elements.emptyState.classList.add('hidden');
            elements.chatContainer.classList.add('active');
            
            // Load messages
            data.messages.forEach(msg => {
                addMessage(msg.role, msg.content);
            });
            
            if (data.session_id) {
                state.sessionId = data.session_id;
            }
        }
    } catch (error) {
        console.warn('Erreur lors du chargement de l\'historique:', error);
        // Don't show error to user, just log it
    }
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleSendMessage,
        addMessage,
        formatTimestamp,
        startNewChat
    };
}
