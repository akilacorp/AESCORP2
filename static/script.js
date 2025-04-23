// Efeito de digitação para o texto hacker
function typeWriter(text, element, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Animação dos contadores
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Efeito sonoro de clique
function playClickSound() {
    const audio = new Audio('data:audio/mp3;base64,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</audio>');
    audio.volume = 0.1;
    audio.play();
}

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o efeito de digitação
    const hackerText = document.getElementById('hackerText');
    const messages = [
        'AesCorp no topo',
        'Hakeando sua camera',
        'Segue o canal AesCorp',
        'A E S C O R P',
        'Desenvolvido por Akila',
        'AesCorp no topo',
        'Hakeando sua camera',
        'Segue o canal AesCorp',
        'A E S C O R P',
        'Desenvolvido por Akila'
    ];
    let messageIndex = 0;

    function cycleMessages() {
        typeWriter(messages[messageIndex], hackerText);
        messageIndex = (messageIndex + 1) % messages.length;
    }

    cycleMessages();
    setInterval(cycleMessages, 4000);

    // Animação dos contadores
    const hackCount = document.getElementById('hackCount');
    const onlineUsers = document.getElementById('onlineUsers');
    
    // Números aleatórios para os contadores
    const randomHacks = Math.floor(Math.random() * 1000) + 500;
    const randomUsers = Math.floor(Math.random() * 100) + 50;
    
    animateValue(hackCount, 0, randomHacks, 2000);
    animateValue(onlineUsers, 0, randomUsers, 2000);

    // Configuração do botão de copiar link
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            const link = this.getAttribute('data-link');
            navigator.clipboard.writeText(window.location.origin + link)
                .then(() => {
                    playClickSound();
                    const originalText = this.querySelector('.btn-content').textContent;
                    this.querySelector('.btn-content').textContent = 'LINK COPIADO!';
                    setTimeout(() => {
                        this.querySelector('.btn-content').textContent = originalText;
                    }, 2000);
                });
        });
    }

    // Adiciona som de clique em todos os botões
    document.querySelectorAll('.cyber-button').forEach(button => {
        button.addEventListener('click', playClickSound);
    });
});