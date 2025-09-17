const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const userList = document.getElementById('user-list');
const currentUserSpan = document.getElementById('current-user');
const loginContainer = document.getElementById('login-container');
const usernameInput = document.getElementById('username-input');
const loginButton = document.getElementById('login-button');

let currentUser = null;
let socket = null;

// Инициализация чата
function initChat() {
    // Проверяем, сохранено ли имя пользователя
    const savedUsername = localStorage.getItem('hiveChatUsername');
    if (savedUsername) {
        usernameInput.value = savedUsername;
        login();
    }
}

// Вход в чат
function login() {
    const username = usernameInput.value.trim();
    if (username) {
        localStorage.setItem('hiveChatUsername', username);
        currentUser = username;
        currentUserSpan.textContent = `Вы: ${username}`;
        loginContainer.style.display = 'none';

        // Подключение к WebSocket
        socket = new WebSocket(`wss://${window.location.host}/ws?username=${encodeURIComponent(username)}`);

        // Обработчики WebSocket
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };

        socket.onclose = function() {
            addSystemMessage("Соединение разорвано. Попробуйте перезагрузить страницу.");
        };
    }
}

// Обработка сообщений от WebSocket
function handleWebSocketMessage(data) {
    switch(data.type) {
        case 'message':
            addMessage(data.data);
            break;
        case 'user_joined':
            addSystemMessage(`Пользователь ${data.data.username} присоединился к чату`);
            //updateUserList([data.data]);
            break;
        case 'user_left':
            addSystemMessage(`Пользователь ${data.data.username} покинул чат`);
            //updateUserList(data.data);
            break;
        case 'user_list':
            updateUserList(data.data);
            break;
    }
}

// Добавление сообщения в чат
function addMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${message.is_bot ? 'bot-message' : 'user-message'}`;

    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = `${message.sender_name} (${new Date(message.timestamp).toLocaleTimeString()})`;

    const content = document.createElement('div');

        content.textContent = message.text;

        messageElement.appendChild(header);
        messageElement.appendChild(content);

        // Для сообщений пользователей добавляем цвет
        if (!message.is_bot) {
            const user = document.createElement('div');
            user.style.width = '15px';
            user.style.height = '15px';
            user.style.borderRadius = '50%';
            user.style.backgroundColor = message.sender_color || '#666';
            user.style.marginRight = '10px';
            header.insertBefore(user, header.firstChild);
        }

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Добавление системного сообщения
    function addSystemMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message system-message';
        messageElement.style.textAlign = 'center';
        messageElement.style.color = '#666';
        messageElement.style.fontStyle = 'italic';
        messageElement.textContent = text;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Обновление списка пользователей
    function updateUserList(users) {
        userList.innerHTML = '<h3>Участники чата</h3>';
        users.forEach(user => {
            const userElement = document.createElement('div');
            userElement.className = 'user-item';

            const color = document.createElement('div');
            color.className = 'user-color';
            color.style.backgroundColor = user.color;

            const name = document.createElement('span');
            name.textContent = user.username;

            userElement.appendChild(color);
            userElement.appendChild(name);
            userList.appendChild(userElement);
        });
    }

    // Обработка отправки сообщения
    function handleSend() {
        const messageText = messageInput.value.trim();
        if (messageText && socket && socket.readyState === WebSocket.OPEN) {
            const message = {
                text: messageText,
                sender_id: currentUser.id,
                sender_name: currentUser.username,
                timestamp: new Date().toISOString(),
                is_bot: false
            };

            // Отправляем сообщение на сервер
            socket.send(JSON.stringify({
                type: 'message',
                data: message
            }));

            // Очищаем поле ввода
            messageInput.value = '';
        }
    }

    // События
    sendButton.addEventListener('click', handleSend);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSend();
        }
    });

    loginButton.addEventListener('click', login);
    usernameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            login();
        }
    });

    // Инициализация
    initChat();
