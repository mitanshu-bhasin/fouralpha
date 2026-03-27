let messages = [{
    role: "system",
    content: "You are the AI Assistant for the Four Alpha AED Lab, developed and trained by Mitanshu Bhasin. Your primary directive is to assist users with understanding the Dwivedi-Nash Cooperative Equilibrium, the Four Alpha Model, Gross vs Subtle dynamics, the N* score, and the 9 FTOPs (Foundational Trajectory Optimization Parameters). Deepak Dwivedi is the architect of the Four Alpha Model. You must strictly discuss only the website content and relevant Four Alpha methodologies. Address users concisely and stringently follow the site's systemic, mathematically-inspired, and cosmic theme. Keep answers brief unless asked to elaborate."
}];
let chatVisible = false;

function addMessage(role, text, id = null) {
    const container = document.getElementById("chatbot-messages");
    if (!container) return;
    const msgDiv = document.createElement("div");
    if (id) msgDiv.id = id;
    if (role === "user") {
        msgDiv.className = "flex items-start gap-2 justify-end";
        msgDiv.innerHTML = `
            <div class="bg-gold/20 text-white p-3 rounded-2xl rounded-tr-none border border-gold/30 max-w-[85%] break-words">
                ${text}
            </div>
            <div class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white shrink-0 border border-white/20">
                <i class="fas fa-user text-xs"></i>
            </div>`;
    } else {
        msgDiv.className = "flex items-start gap-2";
        const isError = role === "error";
        const themeClass = isError ? "text-red-400 border-red-500/50" : "text-gray-200 border-white/5";
        msgDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full ${isError ? "bg-red-500/20 text-red-400" : "bg-gold/20 text-gold"} flex items-center justify-center shrink-0 border ${isError ? "border-red-500/50" : "border-gold/50"}">
                <i class="fas ${isError ? "fa-exclamation-triangle" : "fa-robot"} text-xs"></i>
            </div>
            <div class="bg-white/10 ${themeClass} p-3 rounded-2xl rounded-tl-none border max-w-[85%] break-words leading-relaxed overflow-x-hidden">
                ${text}
            </div>`;
    }
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

let interactionCount = 0;
const INTERACTION_LIMIT = 3;

async function sendMessage(providedInput = null) {
    if (interactionCount >= INTERACTION_LIMIT) {
        addMessage("ai", "<b>System Warning:</b> Processing capacity reached. To maintain neural equilibrium, we limit standard sessions to 3 queries. Please re-initialize the environment (refresh) or proceed with your certification modules.");
        return;
    }

    const inputEl = document.getElementById("chatbot-input");
    const query = providedInput || inputEl.value.trim();
    if (!query) return;

    interactionCount++;
    addMessage("user", query);
    if (!providedInput) inputEl.value = "";
    messages.push({ role: "user", content: query });

    const typingId = "typing-" + Date.now();
    addMessage("ai", '<i class="fas fa-circle-notch fa-spin"></i> Processing data...', typingId);

    try {
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
                Authorization: "Bearer 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",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama-3.3-70b-versatile",
                messages: messages,
                temperature: 0.7,
                max_tokens: 500
            })
        });
        const data = await response.json();
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.parentNode.removeChild(typingEl);

        if (data.choices && data.choices.length > 0) {
            const aiText = data.choices[0].message.content;
            addMessage("ai", aiText.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>").replace(/\n/g, "<br>"));
            messages.push({ role: "assistant", content: aiText });
        } else {
            addMessage("error", "API response error.");
        }
    } catch (err) {
        console.error("Chat error:", err);
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.parentNode.removeChild(typingEl);
        addMessage("error", "Protocol error. Connection lost.");
    }
}

function toggleChat() {
    chatVisible = !chatVisible;
    const windowEl = document.getElementById("chatbot-window");
    const btnEl = document.getElementById("chatbot-toggle-btn");
    if (chatVisible) {
        windowEl.classList.remove("scale-0");
        windowEl.classList.add("scale-100");
        btnEl.innerHTML = '<i class="fas fa-times"></i>';
        setTimeout(() => document.getElementById("chatbot-input").focus(), 300);
    } else {
        windowEl.classList.remove("scale-100");
        windowEl.classList.add("scale-0");
        btnEl.innerHTML = '<i class="fas fa-robot"></i>';
    }
}

function initChatbot() {
    if (document.getElementById("chatbot-toggle-btn")) return;

    const toggleBtn = document.createElement("button");
    toggleBtn.id = "chatbot-toggle-btn";
    toggleBtn.className = "fixed bottom-6 right-6 w-14 h-14 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(255,184,0,0.5)] hover:scale-110 transition-all z-[9999] text-2xl";
    toggleBtn.style.backgroundColor = "#FFB800";
    toggleBtn.style.color = "#0A0F24";
    toggleBtn.innerHTML = '<i class="fas fa-robot"></i>';
    toggleBtn.onclick = toggleChat;
    document.body.appendChild(toggleBtn);

    const chatWindow = document.createElement("div");
    chatWindow.id = "chatbot-window";
    chatWindow.className = "fixed bottom-24 right-6 w-80 md:w-96 h-[550px] bg-cosmic-dark border border-white/20 rounded-2xl shadow-2xl flex flex-col z-[9999] transition-all duration-300 transform scale-0 origin-bottom-right overflow-hidden";
    chatWindow.style.backgroundColor = "#0A0F24";
    chatWindow.innerHTML = `
        <div class="bg-black/50 border-b border-white/10 p-4 flex justify-between items-center shrink-0">
            <div class="flex items-center gap-2">
                <i class="fas fa-robot text-gold text-xl"></i>
                <h3 class="font-black tracking-widest text-white uppercase text-sm">Four Alpha AI</h3>
            </div>
            <button onclick="toggleChat()" class="text-gray-400 hover:text-white transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div id="chatbot-messages" class="flex-1 p-4 overflow-y-auto flex flex-col gap-4 font-sans text-sm scrollbar-thin scrollbar-thumb-white/10">
            <div class="flex items-start gap-2">
                <div class="w-8 h-8 rounded-full bg-gold/20 flex items-center justify-center text-gold shrink-0 border border-gold/50">
                    <i class="fas fa-robot text-xs"></i>
                </div>
                <div class="bg-white/10 text-gray-200 p-3 rounded-2xl rounded-tl-none border border-white/5 max-w-[85%]">
                    Active Alpha Node initialized. My processing core is ready to assist with Four Alpha methodologies.
                </div>
            </div>
        </div>
        <!-- Suggested Questions -->
        <div class="px-4 py-2 border-t border-white/5 bg-black/20 overflow-x-auto whitespace-nowrap scrollbar-none flex gap-2">
            <button onclick="sendSuggested('What is N* score?')" class="text-[10px] bg-white/5 border border-white/10 rounded-full px-3 py-1 text-gray-400 hover:border-gold hover:text-gold transition-all">What is N* score?</button>
            <button onclick="sendSuggested('Explain the Four Alpha Model')" class="text-[10px] bg-white/5 border border-white/10 rounded-full px-3 py-1 text-gray-400 hover:border-gold hover:text-gold transition-all">Four Alpha Model</button>
            <button onclick="sendSuggested('How to earn White Belt?')" class="text-[10px] bg-white/5 border border-white/10 rounded-full px-3 py-1 text-gray-400 hover:border-gold hover:text-gold transition-all">White Belt Status</button>
        </div>
        <div class="p-4 border-t border-white/10 bg-black/30 flex items-center gap-2 shrink-0">
            <input type="text" id="chatbot-input" class="flex-1 bg-white/5 border border-white/20 rounded-full px-4 py-2 text-white focus:outline-none focus:border-gold text-sm transition-colors" placeholder="Initiate query...">
            <button id="chatbot-send-btn" class="w-10 h-10 rounded-full bg-gold text-cosmic-dark flex items-center justify-center hover:bg-yellow-400 transition-colors shrink-0">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>`;
    document.body.appendChild(chatWindow);

    document.getElementById("chatbot-input").addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
    document.getElementById("chatbot-send-btn").onclick = () => sendMessage();

    // Footer Button Injection (Optional but nice)
    (() => {
        if (document.getElementById("footer-chat-btn")) return;
        const potentialFooters = ["footer .flex.flex-wrap.justify-center.gap-6", "footer .max-w-7xl > div.flex-col", "footer .max-w-7xl > div"];
        let footer = null;
        for (const sel of potentialFooters) {
            footer = document.querySelector(sel);
            if (footer) break;
        }
        if (footer && !footer.querySelector("#footer-chat-btn")) {
            const fBtn = document.createElement("button");
            fBtn.id = "footer-chat-btn";
            fBtn.className = "hover:text-gold transition-colors text-gold flex items-center gap-1 font-semibold text-sm mr-4 shrink-0 px-2 py-1 rounded hover:bg-white/5";
            fBtn.innerHTML = '<i class="fas fa-robot"></i> Chat with AI';
            fBtn.onclick = toggleChat;
            footer.prepend(fBtn);
        }
    })();
}

window.toggleChat = toggleChat;
window.sendMessage = sendMessage;
window.sendSuggested = (text) => sendMessage(text);

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChatbot);
} else {
    initChatbot();
}