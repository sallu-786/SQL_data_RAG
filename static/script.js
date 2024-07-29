async function sendMessage(message = null) {
    const messageInput = document.getElementById('message');
    if (!message) {
        message = messageInput.value.trim();
    }
    if (!message) return;

    // Hide title and cards
    document.querySelector('.title').style.display = 'none';
    document.querySelector('.cards').style.display = 'none';

    // Display user message in chat immediately
    displayMessage(message, 'user-message');
    messageInput.value = '';

    // Add spinner
    const spinnerElement = document.createElement('div');
    spinnerElement.className = 'message bot-message spinner-message';
    spinnerElement.innerHTML = '<div class="spinner"></div><span>Loading...</span>';
    document.getElementById('chat').appendChild(spinnerElement);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        const data = await response.json();

        // console.log('Answer message:', data.answer);

        // Remove spinner
        spinnerElement.remove();

        // Display bot message in chat with delay
        await displayMessageWithDelay(data.answer, 'bot-message');
        document.querySelector('.chat-container').style.display = 'block';

        const chatContainer = document.getElementById('chat');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (error) {
        // Remove spinner
        spinnerElement.remove();
        displayMessage('Error: ' + error.message, 'bot-message');
    }
}

async function displayMessageWithDelay(message, className) {
    const chat = document.getElementById('chat');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + className;

    // Create avatar element
    const avatarElement = document.createElement('img');
    avatarElement.src = 'static/tb_icon.png'; // Replace with actual URL
    avatarElement.className = 'avatar';
    
    messageElement.appendChild(avatarElement);

    // Create a separate element for the text
    const textElement = document.createElement('div');
    textElement.className = 'message-text';
    messageElement.appendChild(textElement);

    chat.appendChild(messageElement);

    await displayFormattedCharactersWithDelay(textElement, message);

    chat.scrollTop = chat.scrollHeight;
}

async function displayFormattedCharactersWithDelay(textElement, message) {
    // Handle bold text
    let responseArray = message.split("**");
    let formattedMessage = "";
    for (let i = 0; i < responseArray.length; i++) {
        if (i === 0 || i % 2 !== 1) {
            formattedMessage += responseArray[i];
        } else {
            formattedMessage += "<b>" + responseArray[i] + "</b>";
        }
    }

    let lines = formattedMessage.split('\n');
    let inList = false;
    let ulElement;

    for (let line of lines) {
        if (line.trim().startsWith('-')) {
            if (!inList) {
                ulElement = document.createElement('ul');
                textElement.appendChild(ulElement);
                inList = true;
            }
            const liElement = document.createElement('li');
            ulElement.appendChild(liElement);
            await displayLineWithDelay(liElement, line.trim().substring(1).trim());
        } else {
            if (inList) {
                inList = false;
                ulElement = null;
            }
            await displayLineWithDelay(textElement, line);
            if (line !== '') {
                textElement.insertAdjacentHTML('beforeend', '<br>');
            }
        }
    }
}

async function displayLineWithDelay(element, text) {
    const linkRegex = /\[([^\]]+)\]\(([^\)]+)\)/g;
    let match;
    let lastIndex = 0;

    while ((match = linkRegex.exec(text)) !== null) {
        // Display text before the link
        await displayTextWithDelay(element, text.slice(lastIndex, match.index));


        const linkText = match[1];
        const linkUrl = match[2];
        const linkElement = document.createElement('a');
        linkElement.href = linkUrl;
        linkElement.textContent = linkText;
        element.appendChild(linkElement);

        lastIndex = linkRegex.lastIndex;
    }


    await displayTextWithDelay(element, text.slice(lastIndex));
}

async function displayTextWithDelay(element, text) {
    for (let char of text) {
        element.insertAdjacentText('beforeend', char);
        const chatContainer = document.getElementById('chat');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        await delay(10); // Adjust delay time as needed
    }
}


function displayMessage(message, className) {
    const chat = document.getElementById('chat');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + className;
    messageElement.textContent = message;
    chat.appendChild(messageElement);


    chat.scrollTop = chat.scrollHeight;
}


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function setupCardListeners() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const message = this.textContent.trim();
            sendMessage(message);
        });
    });
}


const messageInput = document.getElementById('message');


messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage(); // Call sendMessage() when Enter key is pressed
    }
});


document.addEventListener('DOMContentLoaded', setupCardListeners);

document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.querySelector('button'); 
    sendButton.addEventListener('click', function() {
        sendMessage(); 
    });
});
