// Aguarda o documento HTML ser completamente carregado
document.addEventListener('DOMContentLoaded', function() {

  // Seleciona o input de arquivo e o span que mostrará o nome
  const inputFile = document.getElementById('arquivoContrato');
  const fileNameSpan = document.getElementById('nomeArquivo');

  // Adiciona um "ouvinte" para exibir o nome do arquivo selecionado
  inputFile.addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
      fileNameSpan.textContent = this.files[0].name;
    } else {
      fileNameSpan.textContent = 'Nenhum arquivo selecionado';
    }
  });
});

/**
 * Função para enviar o arquivo para a API e processar a resposta.
 * @param {Event} event O evento do formulário.
 */
async function enviarArquivo(event) {
  // 1. Prevenir o comportamento padrão do formulário (que recarregaria a página)
  event.preventDefault();

  const inputFile = document.getElementById('arquivoContrato');
  const resultadoSection = document.getElementById('resultadoProcessamento');

  // Verifica se um arquivo foi realmente selecionado
  if (inputFile.files.length === 0) {
    alert('Por favor, selecione um arquivo antes de enviar.');
    return;
  }

  // 2. Montar o corpo da requisição (multipart/form-data)
  const arquivo = inputFile.files[0];
  const formData = new FormData();
  formData.append('file', arquivo); // A chave 'file' deve corresponder ao que a API espera

  // 3. Obter o token de autenticação do sessionStorage
  const token = sessionStorage.getItem('access_token');
  if (!token) {
    alert('Erro de autenticação: Token de acesso não encontrado.');
    // Idealmente, você redirecionaria para a página de login aqui
    return;
  }

  // Exibe uma mensagem de carregamento
  resultadoSection.style.display = 'block';
  resultadoSection.innerHTML = '<p>Processando o contrato, por favor aguarde...</p>';

  try {
    // 4. Disparar a requisição POST para a API com o cabeçalho de autorização
    const response = await fetch('/api/v1/contracts/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    // Verifica se a requisição foi bem-sucedida
    if (!response.ok) {
      // Tenta obter mais detalhes do erro, se a API os fornecer
      const errorData = await response.json().catch(() => null);
      const errorMessage = errorData ? JSON.stringify(errorData.detail) : `HTTP error! status: ${response.status}`;
      throw new Error(`Falha no upload do arquivo. ${errorMessage}`);
    }

    // 5. Fazer o parse do JSON da resposta e exibir na tela
    const data = await response.json();
    displayContractData(data);

  } catch (error) {
    console.error('Erro ao processar o arquivo:', error);
    resultadoSection.innerHTML = `<p style="color: #ff4d4d;">Ocorreu um erro: ${error.message}</p>`;
  }
}

/**
 * Função para renderizar os dados do contrato processado na seção de resultados.
 * @param {object} data O objeto JSON retornado pela API.
 */
function displayContractData(data) {
  const resultadoSection = document.getElementById('resultadoProcessamento');

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