import os
import subprocess

def list_files(folder, extensions):
    files = []
    for file in os.listdir(folder):
        if file.endswith(tuple(extensions)):
            files.append(file)
    return files

def associate_subtitles_and_audio(videos, subtitles, audios):
    associations = {}
    for video in videos:
        base_name = video.rsplit('.', 1)[0]
        associations[video] = {
            'subtitles': [subtitle for subtitle in subtitles if subtitle.startswith(base_name)],
            'audios': [audio for audio in audios if audio.startswith(base_name)]
        }
    return associations

def get_language(subtitle, audio, language_code):
    for terms, code in language_code.items():
        for term in terms.split(','):
            if term.strip() in subtitle or term.strip() in audio:
                return code
    return 'und'

def mux_videos_and_audios(folder, associations, language_code):
    files_to_delete = []
    for video, files in associations.items():
        input_video = os.path.join(folder, video)
        output = os.path.join(folder, video.rsplit('.', 1)[0] + '.mkv')
        command = ['mkvmerge', '-o', output, input_video]

        for subtitle in files['subtitles']:
            language = get_language(subtitle, '', language_code)
            forced = '[Forced]' in subtitle
            sdh = '[SDH]' in subtitle
            if forced:
                command.extend(['--forced-track', '0:yes'])
            if sdh:
                command.extend(['--hearing-impaired-flag', '0:yes'])
            command.extend(['--language', '0:' + language, os.path.join(folder, subtitle)])

        for audio in files['audios']:
            language = get_language('', audio, language_code)
            command.extend(['--language', '0:' + language, os.path.join(folder, audio)])

        subprocess.run(command, check=True)
        files_to_delete.append((input_video, [os.path.join(folder, subtitle) for subtitle in files['subtitles']], [os.path.join(folder, audio) for audio in files['audios']]))
    return files_to_delete

def delete_files(files):
    for input_file, subtitles, audios in files:
        os.remove(input_file)
        for subtitle in subtitles:
            os.remove(subtitle)
        for audio in audios:
            os.remove(audio)

folder = r'folder_with_mk_files'
video_extensions = ('.mp4', '.avi', '.mkv')
subtitle_extensions = ('.srt', '.ass', '.ssa')
audio_extensions = ('.eac3', '.ac3', '.aac')

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

videos = list_files(folder, video_extensions)
subtitles = list_files(folder, subtitle_extensions)
audios = list_files(folder, audio_extensions)
associations = associate_subtitles_and_audio(videos, subtitles, audios)
files_to_delete = mux_videos_and_audios(folder, associations, language_code)

response = input("Do you want to delete the original files (videos, subtitles, and audios)? Answer with 'yes' or 'no'. ")

if response.lower() == 'yes':
    delete_files(files_to_delete)

print("Process completed.")
