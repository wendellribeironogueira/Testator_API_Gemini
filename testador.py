from google import genai
from google.genai import types
import os
import time
import colorama
from dotenv import load_dotenv

# Inicializa colorama para funcionar em todos os terminais (e reseta a cor automaticamente)
colorama.init(autoreset=True)
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
CYAN = colorama.Fore.CYAN

def main():
    print(f"{CYAN}=== Testador de API Google Generative AI ===")

    # Carrega variáveis do arquivo .env (override=True garante que usaremos o que está no arquivo)
    load_dotenv(override=True)

    # 1. Configuração da Chave de API
    # Tenta pegar da variável de ambiente ou pede input se não existir
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(f"{YELLOW}[AVISO] Variável GOOGLE_API_KEY não encontrada.")
        api_key = input("Cole sua API Key aqui: ").strip()

    if not api_key:
        print(f"{RED}[ERRO] Sem chave, não consigo testar.")
        return

    client = genai.Client(api_key=api_key)

    print(f"\n{YELLOW}[INFO] Consultando Google para listar modelos disponíveis para sua chave...")
    
    try:
        # 2. Listar Modelos
        models_info = []
        for m in client.models.list():
            # Filtra apenas modelos que geram texto (ignora modelos de embedding puro por enquanto)
            if "gemini" in m.name and "embedding" not in m.name:
                models_info.append({
                    "name": m.name,
                    "input_token_limit": getattr(m, "input_token_limit", 0) or 0,
                    "output_token_limit": getattr(m, "output_token_limit", 0) or 0,
                })
        
        print(f"{GREEN}[SUCESSO] Encontrados {len(models_info)} modelos compatíveis.\n")

    except Exception as e:
        print(f"{RED}[ERRO FATAL] Não foi possível listar modelos. Verifique se a chave está correta.")
        print(f"Detalhe do erro: {e}")
        return

    # 3. Testar Consumo e Acesso
    print(f"{CYAN}=== Iniciando Teste de Acesso e Latência ===")
    print(f"{'MODELO':<30} | {'ENTRADA (tokens)':<18} | {'SAÍDA (tokens)':<17} | {'STATUS':<15} | {'LATÊNCIA':<10}")
    print("-" * 105)

    stats = {"ATIVO": 0, "COTA EXCEDIDA": 0, "OUTROS": 0}

    for model_data in models_info:
        model_name = model_data["name"]
        input_limit = model_data["input_token_limit"]
        output_limit = model_data["output_token_limit"]
        start_time = time.time()
        status = "..."
        latency = "0s"
        color = "" # A cor será definida abaixo

        try:
            # Tenta gerar um conteúdo mínimo (max_output_tokens=1) para economizar cota
            response = client.models.generate_content(
                model=model_name,
                contents="Oi",
                config=types.GenerateContentConfig(max_output_tokens=1)
            )
            
            # Se chegou aqui sem erro, a chave funciona para este modelo
            end_time = time.time()
            duration = end_time - start_time
            
            status = "ATIVO"
            latency = f"{duration:.2f}s"
            color = GREEN

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            latency = f"{duration:.2f}s"
            
            error_str = str(e)
            if "429" in error_str or "ResourceExhausted" in error_str:
                status = "COTA EXCEDIDA" # Limite atingido
                color = YELLOW
            elif "403" in error_str or "PermissionDenied" in error_str:
                status = "SEM PERMISSÃO" # Chave não autorizada para este modelo específico
                color = RED
            elif "400" in error_str or "InvalidArgument" in error_str:
                status = "REQ. INVÁLIDA" # Modelo não aceita o input simples (ex: requer config de áudio)
                color = RED
            elif "404" in error_str or "NotFound" in error_str:
                status = "NÃO ENCONTRADO" # Modelo descontinuado ou url errada
                color = RED
            else:
                status = "ERRO"
                color = RED

        if status in stats:
            stats[status] += 1
        else:
            stats["OUTROS"] += 1

        print(f"{color}{model_name:<30} | {f'{input_limit:,}':<18} | {f'{output_limit:,}':<17} | {status:<15} | {latency:<10}")
        # Pequena pausa para não causar rate limit artificialmente durante o teste
        time.sleep(0.5) 

    print("\n" + "-" * 105)
    print(f"{YELLOW}[RESUMO]")
    print(f"Total Testado: {len(models_info)}")
    print(f"Ativos: {GREEN}{stats['ATIVO']}{YELLOW} | Cota Excedida: {stats['COTA EXCEDIDA']} | Outros Erros: {stats['OUTROS']}")
    print("-" * 105)
    print("Se o status for 'ATIVO', você pode usar esse modelo no seu projeto.")
    print("Se for 'COTA EXCEDIDA', você atingiu o limite gratuito (RPM/TPM) ou pago.")

if __name__ == "__main__":
    main()