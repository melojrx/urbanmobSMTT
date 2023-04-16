$(document).ready(function () {
    const welcomeMessage = 'Olá! Seja bem-vindo(a) ao Assistente Virtual UrbanChat!';
    const secondWelcomeMessage = 'Apenas os serviços listados abaixo estão disponíveis, aos poucos outros serão incluídos.';
    const optionsMessage = 'Escolha um dos assuntos desejados ou digite sair para encerrar o chat.';
    
    let firstTimeOpened = true;
    
    function showWelcomeMessage() {
        const messageElement = $('<div class="chatbot-message chatbot-message-bot mb-2 welcome-message"></div>').text(welcomeMessage);
        $("#chatbot-container .messages").append(messageElement);
        scrollToBottom();
    }

    function showSecondWelcomeMessage() {
        const messageElement = $('<div class="chatbot-message chatbot-message-bot mb-2 welcome-message"></div>').text(secondWelcomeMessage);
        $("#chatbot-container .messages").append(messageElement);
        scrollToBottom();
    }

    function showOptionsMessage() {
        const messageElement = $('<div class="chatbot-message chatbot-message-bot mb-2 welcome-message"></div>').text(optionsMessage);
        const buttonsContainer = $('<div class="options-container"></div>');
        const button1 = $('<button class="btn btn-primary btn-sm d-block mb-1">1. Como Solicitar sua credencial de Idoso</button>');
        const button2 = $('<button class="btn btn-primary btn-sm d-block">2. Sair</button>');

        buttonsContainer.append(button1);
        buttonsContainer.append(button2);
        messageElement.append(buttonsContainer);
        
        $("#chatbot-container .messages").append(messageElement);
        scrollToBottom();
    }

    function closeChat() {
        $("#chatbot-container").hide();
    }

    function displayBotMessage(message) {
        const messageElement = $('<div class="chatbot-message chatbot-message-bot mb-2 welcome-message"></div>').text(message);
        $("#chatbot-container .messages").append(messageElement);
        scrollToBottom();
    }

    function endChat() {
        displayBotMessage("Muito obrigado.");
        setTimeout(closeChat, 2000);
    }

    function scrollToBottom() {
        const chatbox = $("#chatbot-container");
        chatbox.scrollTop(chatbox[0].scrollHeight);
    }

    // Função para exibir ou ocultar o chatbot ao clicar no ícone
    $("#chatbot-icon").on("click", function () {
        $("#chatbot-container").toggle();

        if (firstTimeOpened) {
            showWelcomeMessage();
            showSecondWelcomeMessage();
            showOptionsMessage();
            firstTimeOpened = false;
        }
    });

    // Função para ocultar o chatbot ao clicar no ícone de minimizar
    $("#minimize-icon").on("click", function () {
        $("#chatbot-container").hide();
    });

    // Função para encerrar o chat ao clicar no botão "Sair" ou digitar "sair"
    $(document).on("click", ".options-container button:last-child", endChat);
    $("#user-input-form").on("submit", function (e) {
        e.preventDefault();
        const userInput = $("#user-input").val().trim().toLowerCase();

        if (userInput === "sair") {
            endChat();
        } else {
            // Aqui você pode adicionar a lógica para outras ações
        }

        // Lembre-se de limpar o campo de entrada após processar a mensagem do usuário
        $("#user-input").val("");
    });

    function invalidOptionMessage() {
        const message = 'Opção inválida. Por favor, digite uma das opções válidas.';
        const messageElement = $('<div class="chatbot-message chatbot-message-bot mb-2 welcome-message"></div>').text(message);
        $("#chatbot-container .messages").append(messageElement);
        scrollToBottom();
    }

    $("#user-input-form").on("submit", function (e) {
        e.preventDefault();
        const userInput = $("#user-input").val().trim().toLowerCase();

        if (userInput === "sair") {
            endChat();
        } else if (userInput === "1" || userInput === "como solicitar sua credencial de idoso") {
            // Aqui você pode adicionar a lógica para processar a opção 1
        } else {
            invalidOptionMessage();
        }

        // Lembre-se de limpar o campo de entrada após processar a mensagem do usuário
        $("#user-input").val("");
    });

});

