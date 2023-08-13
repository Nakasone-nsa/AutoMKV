import os
import subprocess

def listar_arquivos(pasta, extensoes):
    arquivos = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(tuple(extensoes)):
            arquivos.append(arquivo)
    return arquivos

def associar_legendas_e_audio(videos, legendas, audios):
    associacoes = {}
    for video in videos:
        base_nome = video.rsplit('.', 1)[0]
        associacoes[video] = {
            'legendas': [legenda for legenda in legendas if legenda.startswith(base_nome)],
            'audios': [audio for audio in audios if audio.startswith(base_nome)]
        }
    return associacoes

def obter_idioma(legenda, audio, language_code):
    for termos, codigo in language_code.items():
        for termo in termos.split(','):
            if termo.strip() in legenda or termo.strip() in audio:
                return codigo
    return 'und'

def muxar_videos_e_audios(pasta, associacoes, language_code):
    arquivos_deletar = []
    for video, arquivos in associacoes.items():
        entrada_video = os.path.join(pasta, video)
        saida = os.path.join(pasta, video.rsplit('.', 1)[0] + '.mkv')
        comando = ['mkvmerge', '-o', saida, entrada_video]

        for legenda in arquivos['legendas']:
            idioma = obter_idioma(legenda, '', language_code)
            forced = '[Forced]' in legenda
            sdh = '[SDH]' in legenda
            if forced:
                comando.extend(['--forced-track', '0:yes'])
            if sdh:
                comando.extend(['--hearing-impaired-flag', '0:yes'])
            comando.extend(['--language', '0:' + idioma, os.path.join(pasta, legenda)])

        for audio in arquivos['audios']:
            idioma = obter_idioma('', audio, language_code)
            comando.extend(['--language', '0:' + idioma, os.path.join(pasta, audio)])

        subprocess.run(comando, check=True)
        arquivos_deletar.append((entrada_video, [os.path.join(pasta, legenda) for legenda in arquivos['legendas']], [os.path.join(pasta, audio) for audio in arquivos['audios']]))
    return arquivos_deletar

def deletar_arquivos(arquivos):
    for entrada, legendas, audios in arquivos:
        os.remove(entrada)
        for legenda in legendas:
            os.remove(legenda)
        for audio in audios:
            os.remove(audio)

pasta = r'pasta_com_arquivos_mkv'
extensoes_video = ('.mp4', '.avi', '.mkv')
extensoes_legenda = ('.srt', '.ass', '.ssa')
extensoes_audio = ('.eac3', '.ac3', '.aac')

language_code = {
    '.ar-sa': 'ar-SA',
    '.ar-eg': 'ar-EG',
    '.ces, .cs-cz': 'cs-CZ',
    '.dan, .da-dk': 'da-DK',
    '.deu, .de-de': 'de-DE',
    '.ell, .el-gr': 'el-GR',
    '.eng, .en-us, .en-US': 'en-US',
    '.en-gb': 'en-GB',
    '.en-ca, .en-CA': 'en-CA',
    '.fil-ph': 'fil-PH',
    '.fin, .fi-fi': 'fi-FI',
    '.fra, .fr-fr': 'fr-FR',
    '.fr-ca': 'fr-CA',
    '.hun, .hu-hu': 'hu-HU',
    '.hi-in': 'hi-IN',
    '.id-id': 'id-ID',
    '.ita, .it-it': 'it-IT',
    '.jpn, .ja-jp': 'ja-JP',
    '.kor, .ko-kr': 'ko-KR',
    '.kn-in': 'kn-in',
    '.ml-in': 'ml-IN',
    '.ms-my': 'ms-MY',
    '.nld, .nl-nl': 'nl-NL',
    '.nor': 'nb-NO',
    '.pol, .pl-pl': 'pl-PL',
    '.pt-BR, .pt-br': 'pt-BR',
    '.pt-PT, .pt-pt': 'pt-PT',
    '.ron, .ro-ro': 'ro-RO',
    '.slk, .sk-sk': 'sk-SK',
    '.es-419': 'es-419',
    '.es-ES, .es-es': 'es-ES',
    '.es-cl': 'es-CL',
    '.es-mx': 'es-MX',
    '.es-co, .es-CO': 'es-CO',
    '.ru-ru': 'ru-RU',
    '.swe, .sv-se': 'sv-SE',
    '.tur, .tr-tr': 'tr-TR',
    '.ta-in': 'ta-IN',
    '.te-in': 'te-IN',
    '.th-th': 'th-TH',
    '.vi-vn': 'vi-VN',
    '.zho, .zh': 'zh',
    '.zh-Hans, .zh-hans': 'zh-Hans',
    '.zh-Hant, zh-hant': 'zh-Hant',
    '.zh-hk, .zh-HK': 'zh-HK',
}

videos = listar_arquivos(pasta, extensoes_video)
legendas = listar_arquivos(pasta, extensoes_legenda)
audios = listar_arquivos(pasta, extensoes_audio)
associacoes = associar_legendas_e_audio(videos, legendas, audios)
arquivos_deletar = muxar_videos_e_audios(pasta, associacoes, language_code)

resposta = input("Você deseja deletar os arquivos originais (vídeo, legendas e áudios)? Responda com 'sim' ou 'não'. ")

if resposta.lower() == 'sim':
    deletar_arquivos(arquivos_deletar)

print("Processo concluído.")
