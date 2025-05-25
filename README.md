# IDÓSIA - Assistente Virtual para Saúde do Idoso

## 📋 Sobre o Projeto
IDÓSIA é uma aplicação web inovadora desenvolvida para auxiliar no monitoramento e gestão da saúde de pessoas idosas. O sistema oferece análise em tempo real de parâmetros vitais e recomendações personalizadas.

## 🚀 Funcionalidades Principais
- Monitoramento de pressão arterial com análise automática
- Acompanhamento de níveis de colesterol
- Dashboard interativo com histórico de medições
- Recomendações personalizadas baseadas nos dados
- Interface intuitiva e amigável
- Chatbot integrado para dúvidas e suporte, com capacidade opcional de IA avançada.

## 💻 Tecnologias Utilizadas
- Python 3.x
- Flask (Framework Web)
- Plotly (Visualização de Dados)
- Pandas (Análise de Dados)
- HTML/CSS (Interface)
- NLTK (Processamento de Linguagem Natural para Chatbot)
- OpenAI API (Opcional, para Chatbot com IA Avançada)
- python-dotenv (Gerenciamento de variáveis de ambiente)

## Para visualizar ##

1 - git clone https://github.com/yurifmunhozdev/idosia.git
2 - cd idosia
3 - python -m venv venv
4 - .\venv\Scripts\activate
5 - pip install -r requirements.txt
6 - python idosia.py

Link: https://idosia.onrender.com

### Chatbot com Inteligência Artificial Avançada (Opcional)

O chatbot da IDÓSIA foi aprimorado e agora pode, opcionalmente, integrar-se a um serviço de Modelo de Linguagem de Grande Escala (LLM) externo, como o da OpenAI, para fornecer respostas mais detalhadas e contextuais sobre tópicos gerais de saúde e bem-estar.

**Instruções de Configuração da Chave API:**

Para habilitar os recursos avançados de IA do chatbot, é necessária uma chave de API do provedor do LLM (por exemplo, OpenAI).

1.  **Variável de Ambiente:**
    A aplicação procura pela chave de API na variável de ambiente chamada `OPENAI_API_KEY`.
    *   No Linux ou macOS, você pode defini-la no seu terminal:
        ```bash
        export OPENAI_API_KEY="SUA_CHAVE_SECRETA_AQUI"
        ```
    *   No Windows, você pode usar o Painel de Controle (Variáveis de Ambiente do Sistema) ou o PowerShell:
        ```powershell
        $Env:OPENAI_API_KEY="SUA_CHAVE_SECRETA_AQUI"
        ```
    (Lembre-se que a configuração via terminal geralmente é temporária para a sessão atual).

2.  **Uso de arquivo `.env` para Desenvolvimento Local:**
    Para facilitar o desenvolvimento local, você pode criar um arquivo chamado `.env` na raiz do projeto (no mesmo diretório que `idosia.py`). Adicione sua chave API a este arquivo da seguinte forma:
    ```
    OPENAI_API_KEY="SUA_CHAVE_SECRETA_AQUI"
    ```
    **Importante:** Se você criar um arquivo `.env`, é crucial garantir que ele **NÃO** seja enviado para o seu repositório Git. Adicione `.env` ao seu arquivo `.gitignore` para evitar a exposição acidental da sua chave API. Se o arquivo `arquivo.gitignore` no projeto não listar `.env`, adicione uma linha contendo apenas `.env`.

**Comportamento sem Chave API:**
Se a variável de ambiente `OPENAI_API_KEY` não estiver configurada, o chatbot da IDÓSIA continuará funcionando, mas utilizará apenas seu sistema interno de respostas baseadas em regras, que é mais limitado em escopo e complexidade de conversação. A funcionalidade de IA avançada será desabilitada e uma mensagem de aviso será exibida no console do servidor durante a inicialização.

**Aviso de Uso Ético:**
A funcionalidade de chat com IA avançada destina-se a fornecer informações gerais sobre saúde e bem-estar. Ela **não substitui o aconselhamento médico profissional, diagnósticos ou tratamentos.** Sempre consulte um profissional de saúde qualificado para questões médicas pessoais. O assistente não pode realizar diagnósticos nem prescrever tratamentos.

## Em desenvolvimento ##
