def format_timestamp(seconds):
    """Saniyeyi SRT zaman formatına (HH:MM:SS,mmm) çevirir."""
    td = float(seconds)
    hours = int(td // 3600)
    minutes = int((td % 3600) // 60)
    secs = int(td % 60)
    milliseconds = int((td % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def data_to_srt(data, output_file="tmp/tmp.srt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, entry in enumerate(data, 1):
            start, end = entry['timestamp']
            # Eğer end None ise (son segment gibi), küçük bir ekleme yapılabilir
            if end is None: end = start + 2.0 
            
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{entry['text'].strip()}\n\n")

    return output_file


def format_vtt_timestamp(seconds):
    """Saniyeyi VTT zaman formatına (HH:MM:SS.mmm) çevirir."""
    td = float(seconds)
    hours = int(td // 3600)
    minutes = int((td % 3600) // 60)
    secs = int(td % 60)
    milliseconds = int((td % 1) * 1000)
    # VTT formatında milisaniyeler nokta (.) ile ayrılır
    return f"{hours:02}:{minutes:02}:{secs:02}.{milliseconds:03}"

def data_to_vtt(data, output_file="tmp/tmp.srt"):
    # "w" kullanın, "wb" değil
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")  # VTT dosya başlığı zorunludur
        
        for entry in data:
            start, end = entry['timestamp']
            # Bitiş zamanı None ise varsayılan 2 saniye ekle
            if end is None: 
                end = start + 2.0 
            
            f.write(f"{format_vtt_timestamp(start)} --> {format_vtt_timestamp(end)}\n")
            f.write(f"{entry['text'].strip()}\n\n")
    return output_file