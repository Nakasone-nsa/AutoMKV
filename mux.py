import os
import subprocess

def list_files(folder, extensions):
    files = []
    for file in os.listdir(folder):
        if file.endswith(tuple(extensions)):
            files.append(file)
    return files

def associate_subtitles(videos, subtitles):
    associations = {}
    for video in videos:
        base_name = video.rsplit('.', 1)[0]
        associations[video] = [subtitle for subtitle in subtitles if subtitle.startswith(base_name)]
    return associations

def get_language(subtitle, language_code):
    for terms, code in language_code.items():
        for term in terms.split(','):
            if term.strip() in subtitle:
                return code
    return 'und'

def mux_videos(folder, associations, language_code):
    files_to_delete = []
    for video, subtitles in associations.items():
        input_file = os.path.join(folder, video)
        output_file = os.path.join(folder, video.rsplit('.', 1)[0] + '.mkv')
        command = ['mkvmerge', '-o', output_file, input_file]

        for subtitle in subtitles:
            language = get_language(subtitle, language_code)
            forced = '[Forced]' in subtitle
            sdh = '[SDH]' in subtitle
            if forced:
                command.extend(['--forced-track', '0:yes'])
            if sdh:
                command.extend(['--hearing-impaired-flag', '0:yes'])
            command.extend(['--language', '0:' + language, os.path.join(folder, subtitle)])

        subprocess.run(command, check=True)
        files_to_delete.append((input_file, [os.path.join(folder, subtitle) for subtitle in subtitles]))
    return files_to_delete

def delete_files(files):
    for input_file, subtitles in files:
        os.remove(input_file)
        for subtitle in subtitles:
            os.remove(subtitle)

folder = r'folder_with_mk_files'
video_extensions = ('.mp4', '.avi', '.mkv')
subtitle_extensions = ('.srt', '.ass', '.ssa')

language_code = {
    'ar-sa': 'ar-SA',
    'ces': 'cs-CZ',
    'dan': 'da-DK',
    'deu, de-de': 'de-DE',
    'ell': 'el-GR',
    'eng, en-us': 'en-US',
    'en-GB': 'en-GB',
    'fil-ph': 'fil-PH',
    'fin': 'fi-FI',
    'fra, fr-fr': 'fr-FR',
    'fr-ca': 'fr-CA',
    'hun': 'hu-HU',
    'id-id': 'id-ID',
    'ita, it-it': 'it-IT',
    'jap, ja-jp': 'ja-JP',
    'kor, ko-kr': 'ko-KR',
    'kn-in': 'kn-in',
    'ml-in': 'ml-IN',
    'ms-my': 'ms-MY',
    'nld': 'nl-NL',
    'nor': 'nb-NO',
    'pol, pl-pl': 'pl-PL',
    'pt-BR, pt-br': 'pt-BR',
    'pt-pt': 'pt-PT',
    'ron': 'ro-RO',
    'slk': 'sk-SK',
    'es-419': 'es-419',
    'es-es': 'es-ES',
    'swe': 'sv-SE',
    'tur': 'tr-TR',
    'ta-in': 'ta-IN',
    'te-in': 'te-IN',
    'th-th': 'th-TH',
    'vi-vn': 'vi-VN',
    'zho': 'zh',
    'zh-Hans': 'zh-Hans',
    'zh-Hant, zh-hant': 'zh-Hant',
    'zh-HK': 'zh-HK',
}

videos = list_files(folder, video_extensions)
subtitles = list_files(folder, subtitle_extensions)
associations = associate_subtitles(videos, subtitles)
files_to_delete = mux_videos(folder, associations, language_code)

response = input("Do you want to delete the original files (videos and subtitles)? Reply with 'yes' or 'no'. ")

if response.lower() == 'yes':
    delete_files(files_to_delete)

print("Process completed.")
