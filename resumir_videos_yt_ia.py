# "pip install ffmpeg"  OBS: (Digite os comandando no terminal para 
# "pip install openai"                    baixar as bilbiotecas importadas)
# "pip install yt_dlp"               

import ffmpeg
import yt_dlp
import openai
import os


# Defina sua chave de API da OpenAI
openai.api_key = "CHAVE_API"  # Substitua pela sua chave da API para permitir que a OpenAI execute o código com o GPT e o Whisper


# Caminho fixo para salvar os arquivos
save_path = r"CAMINHO_DA_PASTA" #Substituia pelo caminho da pasta onde será salvo o audio, e a transcrição com resumo.
audio_filename = os.path.join(save_path, "audio.mp3")

# URL do vídeo do YouTube
url = "LINK_DO_VIDEO_YT"  # Substitua pela URL do vídeo do YT


# Função para baixar o áudio do YouTube com yt-dlp
def baixar_audio(url, save_path, audio_filename):
    try:
        ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(save_path, audio_filename),
    'ffmpeg_location': r'CAMINHO_EXECUTAVEL_FFMPEG',  # Substitua pelo caminho correto ou configure a váriavel ambiente no PATH, do comando executavel do ffmpeg.
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
    }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Áudio baixado e salvo como {audio_filename}.")
        return os.path.join(save_path, audio_filename)
    except Exception as e:
        print(f"Erro ao baixar áudio: {e}")
        return None

# Função para transcrever áudio usando OpenAI Whisper
def transcrever_audio(filepath):
    try:
        
        with open(filepath, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
            return response['text']
    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return ""
    
# Função para gerar resumo usando OpenAI GPT
def gerar_resumo(transcript):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[   # Instruções que o GPT vai executar com o texto da transcrição
                {"role": "system", "content": """
                    Você é um assistente que resume vídeos detalhados destacando pontos importantes de tal.
                    Faça seu trabalho em seguida que você receber a transcrição de um vídeo.
                    Use formatação Markdown.
                """},
                {"role": "user", "content": f"Descreva o seguinte vídeo: {transcript}"}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        print(f"Erro ao gerar resumo: {e}")
        return ""

# Função para salvar texto em um arquivo e na pasta especificada
def salvar_arquivo(caminho, conteudo):
    try:
        with open(caminho, "w+", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print(f"Arquivo salvo em: {caminho}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Rodando o código e as funções:
audio_file = baixar_audio(url, save_path, "audio.mp3") #Função de baixar audio do video do YT

if audio_file:
    transcript = transcrever_audio(audio_file) #Função de transcrever o áudio baixado com o Whisper
    
    if transcript:
        transcription_path = os.path.join(save_path, "transcricao.txt")
        salvar_arquivo(transcription_path, transcript) # Função de salvar executada no arquivo da transcrição na pasta especificada

        resumo = gerar_resumo(transcript) # Função de gerar o resumo do vídeo com GPT
        
        if resumo:
            resumo_path = os.path.join(save_path, "resumo.md")
            salvar_arquivo(resumo_path, resumo)  # Função de salvar executada no arquivo do resumo na pasta especificada
else:
    print("Falha no download do áudio.")
