## Testador de API Gemini

Este é um script Python simples!
Feito para testar sua chave de API do Google Gemini. Ele verifica a validade da chave, lista todos os modelos para você, testa o acesso a cada um e mede a latência da resposta.

## Funcionalidades

-   **Configuração Segura da API Key**: Prioriza o uso de variáveis de ambiente (`GOOGLE_API_KEY`) e, como alternativa, solicita a chave de forma segura durante a execução, sem salvá-la em disco.
-   **Listagem de Modelos**: Detecta e lista todos os modelos compatíveis com o método `generateContent`.
-   **Informações Detalhadas**: Exibe os limites de tokens de entrada (`input_token_limit`) e saída (`output_token_limit`) para cada modelo.
-   **Teste de Conectividade e Latência**: Envia uma pequena requisição para cada modelo para verificar se está ativo e mede o tempo de resposta.
-   **Tratamento de Erros Específicos**: Identifica e informa erros comuns, como cota de uso excedida (`429 ResourceExhausted`) ou falta de permissão para um modelo específico (`403 PermissionDenied`).
-   **Saída Colorida e Clara**: Utiliza `colorama` para uma exibição amigável e compatível com diferentes sistemas operacionais (Windows, macOS, Linux).

## Pré-requisitos

-   Python 3.6+
-   Uma chave de API do Google Gemini. Você pode obter uma no Google AI Studio.

## Instalação

1.  Clone este repositório ou baixe os arquivos `testador.py` e `requirements.txt`.

2.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Como Usar

Existem duas maneiras de executar o script:

### Método 1: Usando Variável de Ambiente (Recomendado)

Esta é a forma mais segura e prática, especialmente para automação.

1.  Defina a sua chave de API como uma variável de ambiente.

    -   **No Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_API_KEY="SUA_API_KEY_AQUI"
        ```
    -   **No Linux/macOS:**
        ```bash
        export GOOGLE_API_KEY="SUA_API_KEY_AQUI"
        ```

2.  Execute o script:
    ```bash
    python testador.py
    ```

### Método 2: Inserindo a Chave na Execução

Se você não quiser configurar uma variável de ambiente, pode simplesmente rodar o script. Ele pedirá que você cole a chave.

1.  Execute o script:
    ```bash
    python testador.py
    ```

2.  Quando solicitado, cole sua chave de API e pressione Enter.

## Entendendo a Saída

O script exibirá uma tabela com os resultados:

```
MODELO                         | ENTRADA (tokens)   | SAÍDA (tokens)    | STATUS          | LATÊNCIA
---------------------------------------------------------------------------------------------------------
models/gemini-1.5-pro-latest   | 1,048,576          | 8,192             | ATIVO           | 0.85s
models/gemini-1.0-pro          | 30,720             | 2,048             | ATIVO           | 0.52s
models/gemini-1.0-pro-vision   | 12,288             | 4,096             | COTA EXCEDIDA   | 0.31s
```

-   **MODELO**: O nome do modelo testado.
-   **ENTRADA (tokens)**: O número máximo de tokens que o modelo aceita como entrada.
-   **SAÍDA (tokens)**: O número máximo de tokens que o modelo pode gerar como saída.
-   **STATUS**:
    -   `ATIVO`: Sua chave tem permissão e cota para usar este modelo.
    -   `COTA EXCEDIDA`: Sua chave é válida, mas você atingiu o limite de requisições por minuto (RPM) para este modelo.
    -   `SEM PERMISSÃO`: Sua chave não está autorizada a usar este modelo específico.
    -   `REQ. INVÁLIDA`: O modelo existe, mas não aceita o teste simples de texto (comum em modelos de áudio/TTS que exigem configurações específicas).
    -   `NÃO ENCONTRADO`: O modelo pode ter sido descontinuado ou não está acessível na região.
    -   `ERRO`: Ocorreu um erro inesperado durante o teste.
-   **LATÊNCIA**: O tempo em segundos que o modelo levou para responder à requisição de teste.