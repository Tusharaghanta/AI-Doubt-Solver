/**
 * AI Doubt Solver – Client Interactivity & API Communication
 * Stage 5: Chatbot Frontend Development
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const chatContainer = document.getElementById("chat-container");
    const messagesList = document.getElementById("messages-list");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const clearChatBtn = document.getElementById("clear-chat-btn");
    const errorBanner = document.getElementById("error-banner");
    const errorMessage = document.getElementById("error-message");
    const closeErrorBtn = document.getElementById("close-error-btn");

    // Initial Welcome HTML for reset restore
    const initialWelcomeHTML = messagesList.innerHTML;

    // Helper: Format current time as HH:MM AM/PM
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }

    // Helper: Auto-scroll chat to latest message
    function scrollToBottom() {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: "smooth"
        });
    }

    // Helper: Show error notification banner
    function showError(message) {
        errorMessage.textContent = message;
        errorBanner.classList.remove("hidden");
        scrollToBottom();
    }

    // Helper: Hide error notification banner
    function hideError() {
        errorBanner.classList.add("hidden");
    }

    closeErrorBtn.addEventListener("click", hideError);

    // Helper: Safe Markdown Formatter for AI output
    function formatMarkdown(text) {
        if (!text) return "";

        // 1. Escape HTML special characters to prevent XSS
        let safe = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // 2. Format multi-line code blocks: ```lang\ncode\n```
        safe = safe.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
        });

        // 3. Format inline code: `code`
        safe = safe.replace(/`([^`]+)`/g, "<code>$1</code>");

        // 4. Format bold text: **text** or __text__
        safe = safe.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

        // 5. Format italic text: *text* or _text_
        safe = safe.replace(/\*([^*]+)\*/g, "<em>$1</em>");

        // 6. Format headers: ### Heading
        safe = safe.replace(/^### (.*$)/gim, "<h4>$1</h4>");
        safe = safe.replace(/^## (.*$)/gim, "<h3>$1</h3>");
        safe = safe.replace(/^# (.*$)/gim, "<h2>$1</h2>");

        // 7. Format bullet points: * or -
        safe = safe.replace(/^\s*[-*]\s+(.*)$/gim, "<li>$1</li>");
        safe = safe.replace(/(<li>.*<\/li>)/gim, "<ul>$1</ul>");
        // Clean duplicate adjacent <ul> tags
        safe = safe.replace(/<\/ul>\s*<ul>/g, "");

        // 8. Convert remaining newlines to <br> or paragraphs
        safe = safe.replace(/\n\n+/g, "<br><br>");
        safe = safe.replace(/\n/g, "<br>");

        return safe;
    }

    // Append a message bubble to the chat
    function appendMessage(sender, text, isMarkdown = false) {
        const messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message-wrapper", `${sender}-message`);

        const avatar = document.createElement("div");
        avatar.classList.add("avatar", `${sender}-avatar`);
        avatar.textContent = sender === "user" ? "👤" : "🤖";

        const bubble = document.createElement("div");
        bubble.classList.add("message-bubble");

        const header = document.createElement("div");
        header.classList.add("message-header");
        header.innerHTML = `
            <span class="sender-name">${sender === "user" ? "You" : "AI Tutor"}</span>
            <span class="message-time">${getCurrentTime()}</span>
        `;

        const content = document.createElement("div");
        content.classList.add("message-content");

        if (isMarkdown) {
            content.innerHTML = formatMarkdown(text);
        } else {
            const p = document.createElement("p");
            p.textContent = text;
            content.appendChild(p);
        }

        bubble.appendChild(header);
        bubble.appendChild(content);

        if (sender === "user") {
            messageWrapper.appendChild(bubble);
            messageWrapper.appendChild(avatar);
        } else {
            messageWrapper.appendChild(avatar);
            messageWrapper.appendChild(bubble);
        }

        messagesList.appendChild(messageWrapper);
        scrollToBottom();
        return messageWrapper;
    }

    // Append "AI is thinking..." typing indicator
    function showTypingIndicator() {
        const typingWrapper = document.createElement("div");
        typingWrapper.id = "typing-indicator";
        typingWrapper.classList.add("message-wrapper", "ai-message");

        const avatar = document.createElement("div");
        avatar.classList.add("avatar", "ai-avatar");
        avatar.textContent = "🤖";

        const bubble = document.createElement("div");
        bubble.classList.add("typing-bubble");
        bubble.innerHTML = `
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        `;

        typingWrapper.appendChild(avatar);
        typingWrapper.appendChild(bubble);
        messagesList.appendChild(typingWrapper);
        scrollToBottom();
    }

    // Remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) {
            indicator.remove();
        }
    }

    // Auto-grow textarea height as user types
    userInput.addEventListener("input", () => {
        userInput.style.height = "auto";
        userInput.style.height = `${Math.min(userInput.scrollHeight, 140)}px`;
    });

    // Handle Enter key for sending (Shift + Enter inserts newline)
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event("submit"));
        }
    });

    // Main function: Send Question to Flask Backend
    async function handleSendQuestion(questionText) {
        const question = (questionText || userInput.value).trim();
        if (!question) return;

        hideError();

        // 1. Display user question in chat
        appendMessage("user", question, false);

        // 2. Clear & reset input box height
        userInput.value = "";
        userInput.style.height = "auto";

        // 3. Disable send button and show typing animation
        sendBtn.disabled = true;
        userInput.disabled = true;
        showTypingIndicator();

        try {
            // 4. Send POST request to Flask /ask endpoint
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            removeTypingIndicator();

            if (response.ok && data.status === "success") {
                // 5. Render the real Gemini AI response
                appendMessage("ai", data.answer, true);
            } else {
                // 6. Handle server/API errors gracefully
                const errText = data.message || "Failed to get an answer from AI. Please try again.";
                showError(errText);
                appendMessage("ai", `⚠️ **Notice:** ${errText}`, true);
            }
        } catch (error) {
            removeTypingIndicator();
            const networkErrorMsg = "Unable to reach the server. Please ensure the Flask app is running.";
            showError(networkErrorMsg);
            appendMessage("ai", `⚠️ **Network Error:** ${networkErrorMsg}`, true);
            console.error("Chat error:", error);
        } finally {
            sendBtn.disabled = false;
            userInput.disabled = false;
            userInput.focus();
            scrollToBottom();
        }
    }

    // Chat form submit listener
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        handleSendQuestion();
    });

    // Suggestion chip click listener
    messagesList.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip");
        if (chip) {
            const prompt = chip.getAttribute("data-prompt");
            if (prompt) {
                handleSendQuestion(prompt);
            }
        }
    });

    // Clear Chat / Reset Session
    clearChatBtn.addEventListener("click", async () => {
        if (!confirm("Are you sure you want to clear the chat conversation?")) {
            return;
        }

        try {
            const response = await fetch("/reset", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });

            if (response.ok) {
                // Reset UI to initial welcome message
                messagesList.innerHTML = initialWelcomeHTML;
                hideError();
                userInput.value = "";
                userInput.focus();
                scrollToBottom();
            }
        } catch (err) {
            console.error("Failed to reset session:", err);
            showError("Could not reset the chat session.");
        }
    });
});
