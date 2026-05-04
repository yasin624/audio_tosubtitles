import os

from moviepy import VideoFileClip




def cut_audio_fromvideo(video_path, out_dir="tmp/", başlangıç=0, süre=30):
    """
    Librosa kullanarak ses dosyasını keser.
    
    Parametreler:
    - giriş_dosyası: Orijinal ses dosyası
    - çıkış_dosyası: Çıktı dosyası
    - başlangıç: Başlangıç zamanı (saniye)
    - süre: Kesim süresi (saniye)
    """
    video = VideoFileClip(video_path)

    file_name = os.path.basename(video_path)

    tmp_file_path=os.path.join(out_dir,file_name[:-4]+".mp3")
    video.audio.write_audiofile(tmp_file_path) # Sesi mp3 olarak kaydeder

    return tmp_file_path

def save_data(file_path, data):
    with open(file_path,"wb") as file:
        file.write(data)
