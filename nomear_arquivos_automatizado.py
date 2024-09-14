import os

# Definir o prefixo e a extensão
PREFIXO = "arquivo"
EXTENSAO = ".jpg"

def renomear_imagens(caminho_pasta):
    contador = 1
    
    # Iterar sobre todos os arquivos na pasta
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_antigo = os.path.join(caminho_pasta, nome_arquivo)
        
        # Verificar se o arquivo tem a extensão desejada
        if nome_arquivo.endswith(EXTENSAO):
            # Criar o novo nome para o arquivo
            caminho_novo = os.path.join(caminho_pasta, f"{PREFIXO}-{contador}{EXTENSAO}")
            
            # Renomear o arquivo
            try:
                os.rename(caminho_antigo, caminho_novo)
                print(f"Renomeado: {caminho_antigo} -> {caminho_novo}")
                contador += 1
            except Exception as e:
                print(f"Erro ao renomear o arquivo {caminho_antigo}: {e}")

if __name__ == "__main__":
    caminho_pasta = r"C:\Users\usuario\OneDrive\Área de Trabalho\Pasta"  # Altere para o caminho correto; "r" faz ignorar as barras da string
    renomear_imagens(caminho_pasta)

