const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");

const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

const newChatButton = document.getElementById("newChat");
const clearChatButton = document.getElementById("clearChat");

const historyElement = document.getElementById("history");
const menuButton = document.getElementById("menuButton");
const sidebar = document.querySelector(".sidebar");


let sessionId = localStorage.getItem("chat_session_id");

if (!sessionId) {

    sessionId =
        crypto.randomUUID();

    localStorage.setItem(
        "chat_session_id",
        sessionId
    );
}


let chatHistory =
    JSON.parse(
        localStorage.getItem("chat_history") || "[]"
    );


function saveHistory() {

    localStorage.setItem(
        "chat_history",
        JSON.stringify(chatHistory)
    );
}


function addMessage(
    role,
    text
) {

    if (welcome) {
        welcome.style.display = "none";
    }


    const message =
        document.createElement("div");

    message.className =
        `message ${role}`;


    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar";

    avatar.textContent =
        role === "user"
            ? "You"
            : "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";

    content.textContent =
        text;


    message.appendChild(avatar);

    message.appendChild(content);

    messages.appendChild(message);


    messages.scrollTop =
        messages.scrollHeight;
}


function showTyping() {

    const typing =
        document.createElement("div");

    typing.className =
        "message assistant";

    typing.id =
        "typing";


    typing.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">
            Thinking...
        </div>
    `;


    messages.appendChild(typing);

    messages.scrollTop =
        messages.scrollHeight;
}


function removeTyping() {

    const typing =
        document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


async function sendMessage(text) {

    text = text.trim();

    if (!text) {
        return;
    }


    addMessage(
        "user",
        text
    );


    chatHistory.push({
        role: "user",
        text: text
    });

    saveHistory();


    messageInput.value = "";

    messageInput.style.height =
        "auto";

    sendButton.disabled = true;


    showTyping();


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    session_id:
                        sessionId,

                    message:
                        text
                })
            });


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(
                error ||
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        removeTyping();


        addMessage(
            "assistant",
            data.response
        );


        chatHistory.push({

            role: "assistant",

            text:
                data.response
        });


        saveHistory();


        updateHistory();


    } catch (error) {

        removeTyping();


        addMessage(
            "assistant",
            "Sorry, something went wrong. Please try again."
        );


        console.error(error);

    } finally {

        sendButton.disabled =
            false;

        messageInput.focus();
    }
}


chatForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        await sendMessage(
            messageInput.value
        );
    }
);


messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            chatForm.requestSubmit();
        }
    }
);


messageInput.addEventListener(
    "input",
    () => {

        messageInput.style.height =
            "auto";

        messageInput.style.height =
            Math.min(
                messageInput.scrollHeight,
                180
            ) + "px";
    }
);


document
    .querySelectorAll(
        ".suggestions button"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                sendMessage(
                    button.dataset.message
                );
            }
        );
    });


newChatButton.addEventListener(
    "click",
    () => {

        sessionId =
            crypto.randomUUID();

        localStorage.setItem(
            "chat_session_id",
            sessionId
        );


        chatHistory = [];

        saveHistory();


        messages.innerHTML = `
            <div id="welcome" class="welcome">

                <div class="welcome-logo">
                    AI
                </div>

                <h1>
                    How can I help you?
                </h1>

                <p>
                    Ask me anything.
                </p>

                <div class="suggestions">

                    <button data-message="Explain MCP in simple words">
                        Explain MCP
                    </button>

                    <button data-message="What is FastAPI?">
                        What is FastAPI?
                    </button>

                    <button data-message="Give me a Python example">
                        Python example
                    </button>

                    <button data-message="What is 2 + 2?">
                        Calculate
                    </button>

                </div>

            </div>
        `;


        location.reload();
    }
);


clearChatButton.addEventListener(
    "click",
    () => {

        chatHistory = [];

        saveHistory();

        messages.innerHTML = "";

        location.reload();
    }
);


menuButton.addEventListener(
    "click",
    () => {

        sidebar.classList.toggle(
            "open"
        );
    }
);


function loadHistory() {

    if (!chatHistory.length) {
        return;
    }


    if (welcome) {
        welcome.style.display = "none";
    }


    chatHistory.forEach(
        message => {

            addMessage(
                message.role,
                message.text
            );

        }
    );
}


function updateHistory() {

    historyElement.innerHTML = "";


    const userMessages =
        chatHistory.filter(
            item =>
                item.role === "user"
        );


    userMessages
        .slice(-20)
        .reverse()
        .forEach(item => {

            const element =
                document.createElement("div");

            element.className =
                "history-item";

            element.textContent =
                item.text;

            historyElement.appendChild(
                element
            );
        });
}


loadHistory();

updateHistory();