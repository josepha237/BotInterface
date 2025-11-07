const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");

const userData = {
  message: null
}

const chatHistory = [];
const initialInputHeight = messageInput.scrollHeight;

//créer un élément message avec une classe dynamique et le retourner
const createMessageElement = (content, ...classes) => {
  const div = document.createElement("div");
  div.classList.add("message", ...classes);
  div.innerHTML = content;
  return div;
}

// Réponses générés par le bot
const generateBotResponse = async(incomingMessageDiv) => {
  const messageElement = incomingMessageDiv.querySelector(".message-text");
  chatHistory.push();
  input = input.toLowerCase();
      if (input.includes("bonjour")) return "Bonjour 👋 Je suis Bot4Univ, ravi de discuter avec toi !";
      if (input.includes("merci")) return "Avec plaisir 😊. N'hésite pas à me consulter si tu veux plus d'infos sur le préinscription";
      if (input.includes("aide")) return "Je peux t’aider à te préinscrire ou répondre à tes questions 📘.";
      if (input.includes("au revoir")) return "Au revoir 👋 À bientôt !";
      return "Je ne suis pas sûr de comprendre 🤔 Peux-tu reformuler ?";
}

// Gérer le message utilisateur sortant
const handleOutgoingMessage = (e) => {
  e.preventDefault();
  userData.message = messageInput.value.trim();
  messageInput.value = ""; // nettoie le textarea après l'envoie du message
  messageInput.dispatchEvent(new Event("input"));

  // Créer et afficher le message utilisateur sortant
  const messageContent = `<div class="message-text"></div>`;

  const outgoingMessageDiv = createMessageElement(messageContent, "user-message");
  outgoingMessageDiv.querySelector(".message-text").textContent = userData.message;
  chatBody.appendChild(outgoingMessageDiv);
  chatBody.scrollTo({top: chatBody.scrollHeight, behavior: "smooth" });

  //simulation de la reponse du bot 
  setTimeout(() => {
    const messageContent = `  <img src="/stactic/img/logo.jpg" alt="Logo B4U" class="logo-img" class="bot-avatar">
        <div class="message-text"> 
          <div class="thinking-indicator">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
        </div>
      </div>`;

    const incomingMessageDiv = createMessageElement(messageContent, "bot-message", "thinking");
    chatBody.appendChild(incomingMessageDiv);
    chatBody.scrollTo({top: chatBody.scrollHeight, behavior: "smooth" });
    generateBotResponse(incomingMessageDiv);
    document.querySelector(".chat-form").style.borderRadius = messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
  }, 600 );
}

// Gérer la pression sur la touche Entrée pour envoyer des messages
messageInput.addEventListener("keydown", (e) =>{
  const userMessage = e.target.value.trim();
  if (e.key === "Enter" && userMessage && !e.shiftkey && window.innerWidth > 768) {
    handleOutgoingMessage(e);
  }
});

// Adjust input field height dynamically
messageInput.addEventListener("input", () => {
  messageInput.style.height = `${initialInputHeight}px`
  messageInput.style.height = `${messageInput.scrollHeight}px`
})

//initialisation des emojis  
 const picker = new EmojiMart.Picker({
  theme: "light",
  skinTonePosition: "none",
  previewPosition: "none",
  onEmojiSelect: (emoji) => {
    const { selectionStart: start, selectionEnd: end } = messageInput;
    messageInput.setRangeText(emoji.native, start, end, "end");
    messageInput.focus();
  },
  onClickOutside: (e) => {
    if (e.target.id === "emoji-picker") {
       document.body.classList.toggle("show-emoji-picker");
    } else {
      document.body.classList.remove("show-emoji-picker");
    }
  }
 });

 document.querySelector(".chat-form").appendChild(picker);

sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e))
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
closeChatbot.addEventListener("click", () =>  document.body.classList.remove("show-chatbot"));