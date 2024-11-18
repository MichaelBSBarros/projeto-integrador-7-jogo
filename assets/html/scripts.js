var backend;

new QWebChannel(qt.webChannelTransport, function(channel) {
    backend = channel.objects.backend;

    // Inicializar a aplicação
    backend.loadThumbnails();

    // Vincular o botão de calcular
    document.getElementById('calculateBtn').addEventListener('click', function() {
        // Desabilitar o botão para evitar múltiplos cliques
        this.disabled = true;
        backend.processImages();
    });
});

// Função para exibir uma imagem no canvas
function displayImage(canvasId, imageData) {
    console.log(`displayImage called for ${canvasId} with data:`, imageData);
    var canvas = document.getElementById(canvasId);
    var ctx = canvas.getContext('2d');
    var img = new Image();
    img.onload = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }
    img.onerror = function() {
        console.error(`Erro ao carregar a imagem no canvas ${canvasId}.`);
    }
    img.src = imageData;
}

// Função para exibir as correspondências
function displayMatches(imageData) {
    console.log("displayMatches called with data:", imageData);
    var canvas = document.getElementById('matchesCanvas');
    if (!canvas) {
        console.error("Canvas 'matchesCanvas' não encontrado.");
        return;
    }
    var ctx = canvas.getContext('2d');
    var img = new Image();
    img.onload = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        console.log("Imagem de correspondências desenhada no canvas.");
    }
    img.onerror = function() {
        console.error("Erro ao carregar a imagem de correspondências.");
    }
    img.src = imageData;
}

// Função para exibir o resultado
function displayResult(text, color) {
    var resultDiv = document.getElementById('result');
    resultDiv.textContent = text;
    resultDiv.style.color = color;
    resultDiv.style.display = 'block';
}

// Função para reabilitar o botão "CALCULAR"
function enableCalculateButton() {
    var calculateBtn = document.getElementById('calculateBtn');
    if (calculateBtn) {
        calculateBtn.disabled = false;
        console.log("Botão CALCULAR reabilitado.");
    }
}

// Função para limpar a mensagem de resultado
function clearResult() {
    var resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.textContent = "";
        resultDiv.style.display = 'none';
        console.log("Mensagem de resultado limpa.");
    }
}

// Função para adicionar miniaturas
function addThumbnail(src, filepath) {
    var thumbnailsDiv = document.getElementById('thumbnails');
    var div = document.createElement('div');
    div.className = 'thumbnail';
    var img = document.createElement('img');
    img.src = src;
    img.title = filepath;
    img.onclick = function() {
        // Substituir barras invertidas por barras normais
        var normalizedPath = filepath.replace(/\\/g, '/');
        console.log(`Enviando para backend: ${normalizedPath}`);  // Depuração
        backend.selectImageB(normalizedPath);
    }
    div.appendChild(img);
    thumbnailsDiv.appendChild(div);
}

// Função para resetar a interface
function resetInterface() {
    console.log("resetInterface called.");
    // Limpar Digital B
    var canvasB = document.getElementById('imageB');
    if (canvasB) {
        var ctxB = canvasB.getContext('2d');
        ctxB.clearRect(0, 0, canvasB.width, canvasB.height);
        console.log("Digital B limpa.");
    }

    // Limpar o resultado
    var resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.textContent = "";
        resultDiv.style.color = "white"; // ou a cor padrão
        resultDiv.style.display = 'none';
        console.log("Div de resultados limpa.");
    }

    // Limpar as correspondências
    var matchesCanvas = document.getElementById('matchesCanvas');
    if (matchesCanvas) {
        var ctxMatches = matchesCanvas.getContext('2d');
        ctxMatches.clearRect(0, 0, matchesCanvas.width, matchesCanvas.height);
        console.log("Canvas de correspondências limpa.");
    }

    // Ocultar o Quadrado 4: Correspondências
    var quadrado4 = document.getElementById('quadrado4');
    if (quadrado4) {
        quadrado4.style.display = 'none';
        console.log("Quadrado 4: Correspondências oculto.");
    }

    // Reabilitar o botão de calcular
    var calculateBtn = document.getElementById('calculateBtn');
    if (calculateBtn) {
        calculateBtn.disabled = false;
        console.log("Botão CALCULAR reabilitado.");
    }

    // Mostrar os outros quadrados
    showElements();

    // Chamar o backend para resetar a aplicação e selecionar nova imagem A
    if (backend && backend.resetApplication) {
        backend.resetApplication();
        console.log("Chamado backend.resetApplication().");
    } else {
        console.error("Método backend.resetApplication não está disponível.");
    }
}

// Função para esconder elementos, exceto o Quadrado 4
function hideElementsExceptMatches() {
    console.log("hideElementsExceptMatches called.");
    // Esconder Quadrado 1: Digital A
    var quadrado1 = document.getElementById('quadrado1');
    if (quadrado1) {
        quadrado1.style.display = 'none';
        console.log("Quadrado 1: Digital A oculto.");
    }

    // Esconder Quadrado 2: Digital B
    var quadrado2 = document.getElementById('quadrado2');
    if (quadrado2) {
        quadrado2.style.display = 'none';
        console.log("Quadrado 2: Digital B oculto.");
    }

    // Esconder Quadrado 3: Banco de Digitais
    var quadrado3 = document.getElementById('quadrado3');
    if (quadrado3) {
        quadrado3.style.display = 'none';
        console.log("Quadrado 3: Banco de Digitais oculto.");
    }

    // Mostrar Quadrado 4: Correspondências
    var quadrado4 = document.getElementById('quadrado4');
    if (quadrado4) {
        quadrado4.style.display = 'block';
        console.log("Quadrado 4: Correspondências exibido.");
    }

    // Mostrar o resultado
    var resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.style.display = 'block';
        console.log("Div de resultados exibida.");
    }
}

// Função para mostrar todos os elementos novamente
function showElements() {
    console.log("showElements called.");
    // Mostrar Quadrado 1: Digital A
    var quadrado1 = document.getElementById('quadrado1');
    if (quadrado1) {
        quadrado1.style.display = 'flex';
        console.log("Quadrado 1: Digital A exibido.");
    }

    // Mostrar Quadrado 2: Digital B
    var quadrado2 = document.getElementById('quadrado2');
    if (quadrado2) {
        quadrado2.style.display = 'flex';
        console.log("Quadrado 2: Digital B exibido.");
    }

    // Mostrar Quadrado 3: Banco de Digitais
    var quadrado3 = document.getElementById('quadrado3');
    if (quadrado3) {
        quadrado3.style.display = 'block';
        console.log("Quadrado 3: Banco de Digitais exibido.");
    }

    // Ocultar Quadrado 4: Correspondências (se ainda estiver visível)
    var quadrado4 = document.getElementById('quadrado4');
    if (quadrado4) {
        quadrado4.style.display = 'none';
        console.log("Quadrado 4: Correspondências oculto.");
    }

    // Ocultar o resultado
    var resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.style.display = 'none';
        console.log("Div de resultados ocultada.");
    }

    // Reabilitar o botão de calcular
    var calculateBtn = document.getElementById('calculateBtn');
    if (calculateBtn) {
        calculateBtn.disabled = false;
        console.log("Botão CALCULAR reabilitado.");
    }
}

// Função chamada pelo backend para processar as imagens
function onProcessImagesComplete() {
    console.log("onProcessImagesComplete called.");
    // Após o processamento, exibir as correspondências e esconder os outros quadrados
    hideElementsExceptMatches();

    // Iniciar o timer para resetar a aplicação após 5 segundos
    setTimeout(resetInterface, 5000);
}