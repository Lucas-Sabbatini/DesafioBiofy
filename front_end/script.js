// Executa o script quando o conteúdo da página estiver totalmente carregado.
  const loginForm = document.querySelector('.login-section form');
  const loginSection = document.querySelector('.login-section');
  console.log("Rodouuu");

  // Adiciona um ouvinte de evento para o envio do formulário.
  loginForm.addEventListener('submit', async (event) => {
    // Impede o comportamento padrão do formulário, que é recarregar a página.
    event.preventDefault();

    // Remove mensagens de erro antigas.
    clearError();

    const username = loginForm.querySelector('input[type="text"]').value;
    const password = loginForm.querySelector('input[type="password"]').value;

    // O corpo da requisição deve ser formatado como x-www-form-urlencoded.
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch('/api/v1/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        // Login bem-sucedido.
        // Armazena o token em um cookie. O navegador o enviará automaticamente
        // nas próximas requisições para páginas protegidas.
        sessionStorage.setItem('access_token', data.access_token);

        // Redireciona para a página do menu.
        window.location.href = '/menu/index.html';
      } else {
        // Exibe a mensagem de erro retornada pela API.
        showError('Falha no login.');
      }
    } catch (error) {
      // Trata erros de rede ou conexão.
      console.error('Erro de conexão:', error);
      showError('Não foi possível conectar ao servidor.');
    }
  });

  /**
   * Exibe uma mensagem de erro abaixo do formulário de login.
   * @param {string} message - A mensagem a ser exibida.
   */
  function showError(message) {
    let errorDiv = document.getElementById('login-error');
    if (!errorDiv) {
      errorDiv = document.createElement('p');
      errorDiv.id = 'login-error';
      errorDiv.style.color = 'red';
      errorDiv.style.textAlign = 'center';
      loginSection.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
  }

  /**
   * Limpa a mensagem de erro.
   */
  function clearError() {
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
      errorDiv.remove();
    }
  }