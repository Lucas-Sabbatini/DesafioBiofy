// Adiciona um ouvinte de evento para o envio do formulário de busca.
document.querySelector('.consulta-search').addEventListener('submit', buscarContrato);

/**
 * Busca um contrato na API com base no nome fornecido.
 * @param {Event} event - O evento de submissão do formulário.
 */
async function buscarContrato(event) {
  // Impede o comportamento padrão do formulário (recarregar a página).
  event.preventDefault();

  // Limpa erros e resultados anteriores.
  const resultadoEl = document.getElementById('resultadoContrato');
  resultadoEl.style.display = 'none';
  resultadoEl.innerHTML = '';

  const contract_name = document.getElementById('pesquisaContrato').value;
  const token = sessionStorage.getItem('access_token');

  // Verifica se o token de acesso existe.
  if (!token) {
    exibirErro('Você não está autenticado. Faça o login novamente.');
    // Opcionalmente, redirecionar para a página de login.
    // window.location.href = '/';
    return;
  }

  try {
    const response = await fetch(`/api/v1/contracts/${contract_name}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();

    if (response.ok) {
      // Exibe os dados do contrato na página.
      exibirContrato(data);
    } else {
      // Exibe a mensagem de erro retornada pela API.
      const errorMessage = data.detail || 'Erro ao buscar o contrato.';
      exibirErro(errorMessage);
    }
  } catch (error) {
    // Trata erros de rede ou conexão.
    console.error('Erro de conexão:', error);
    exibirErro('Não foi possível conectar ao servidor.', error);
  }
}

/**
 * Exibe os dados de um contrato na seção de resultados.
 * @param {object} contrato - O objeto do contrato retornado pela API.
 */
function exibirContrato(data) {
  const resultadoSection = document.getElementById('resultadoContrato');

  // Limpa a seção e a torna visível
  resultadoSection.innerHTML = '';
  resultadoSection.style.display = 'block';

  // Helper para criar listas
  const createList = (items) => {
    if (!items || items.length === 0) return '<li>Nenhuma informação encontrada.</li>';
    return items.map(item => `<li><span class="value">${item}</span></li>`).join('');
  };

  // Helper para criar seções com título e lista
  const createSection = (title, items) => `
    <div class="subsection">
      <h2>${title}</h2>
      <ul>${createList(items)}</ul>
    </div>
  `;

  // Helper para criar seções de dados adicionais (chave-valor)
  const createAdditionalDataSection = (title, dataObject) => {
    const items = Object.entries(dataObject).map(([key, value]) =>
      `<li><span class="label">${key.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase())}:</span> <span class="value">${value}</span></li>`
    ).join('');
    return `
      <div class="subsection">
        <h2>${title}</h2>
        <ul>${items}</ul>
      </div>
    `;
  };

  // Monta o HTML com todas as informações do contrato
  let content = `<h1>Detalhes do Contrato Processado</h1>`;
  content += `<p><span class="label">Arquivo:</span> <span class="value">${data.file_name}</span></p>`;
  content += `<p><span class="label">Processado em:</span> <span class="value">${new Date(data.uploaded_at).toLocaleString('pt-BR')}</span></p>`;

  content += createSection('Partes Envolvidas', data.contract_data.parties);
  content += createSection('Valores Monetários', data.contract_data.monetary_values);
  content += createSection('Obrigações Principais', data.contract_data.main_obligations);
  content += createAdditionalDataSection('Dados Adicionais', data.contract_data.additional_data);

  content += `
    <div class="subsection">
      <h2>Cláusula de Rescisão</h2>
      <p><span class="value">${data.contract_data.termination_clause}</span></p>
    </div>
  `;

  // Insere o conteúdo HTML na seção de resultados
  resultadoSection.innerHTML = content;
}

/**
 * Exibe uma mensagem de erro na seção de resultados.
 * @param {string} message - A mensagem de erro a ser exibida.
 */
function exibirErro(message) {
  const el = document.getElementById('resultadoContrato');
  el.style.display = 'block';
  el.classList.add('error'); // Adiciona uma classe para estilização de erro
  el.innerHTML = `<p class="error-message">${message}</p>`;
}