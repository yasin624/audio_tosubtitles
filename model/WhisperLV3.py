import re,time
import io

import torch
from tqdm import tqdm
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import librosa 

from tools import env

class WhisperLargeV3():
    def __init__(self):
        # Kaynaklarda kullanılan temel ayarlar [4]
        self.model_name  = env.MODEL_NAME
        self.device      = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.pattern = r"<\|(\d+\.\d+)\|>(.*?)<\|(\d+\.\d+)\|>"
        
        """self.generate_kwargs = {
            "max_length": 448,  # Uyarıyı kapatan kritik satır
            "num_beams": 1,
            "condition_on_prev_tokens": False, # Önceki tokenlara bağımlılığı kapatır [1]
            "compression_ratio_threshold": 1.35,
            "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0), # Temperature fallback stratejisi [1], [3]
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.5,
            "return_timestamps": True, # Zaman damgalarını tahmin etmesini sağlar [2]
            "language":"english"
        }"""

        self.max_length                  = env.MAX_LENGTH                  # Uyarıyı kapatan kritik satır
        self.num_beams                   = env.NUM_BEAMS
        self.condition_on_prev_tokens    = env.CONDITION_ON_PREV_TOKENS    # Önceki tokenlara bağımlılığı kapatır [1]
        self.compression_ratio_threshold = env.COMPRESSİON_RATİO_THRESHOLD
        self.temperature                 = env.TEMPERATURE                 # Temperature fallback stratejisi [1], [3]
        self.logprob_threshold           = env.LOGROB_THRESHOLD
        self.no_speech_threshold         = env.NO_SPEECH_THRESHOLD
        self.return_timestamps           = env.RETURN_TİMESTAMPS           # Zaman damgalarını tahmin etmesini sağlar [2]
        self.language                    = env.LANGUAGE
        self.chunk_length                = env.CHUNK_LENGTH  
        
        self.model,self.processor=self.Load_model()

    def text_Totimestamps(self,text,start_time=0) :
        matches = re.findall(self.pattern, text)
        # İstenen format: [[[zaman damgası], [text]]]
        formatted_output = [{"timestamp":(float(m[0])+start_time, float(m[2])+start_time),
                             "text":(m[1].strip())} for m in matches]

        return formatted_output

    def remove_duplicates(self,data):
        end_element=""
        for s,element in tqdm(enumerate(data)):
            if end_element and element["text"].replace(" ","").lower() == end_element["text"].replace(" ","").lower():
                try:
                    data.remove(element)
                    data.remove(end_element)
                except:
                pass
                element["timestamp"]=(end_element["timestamp"][0],element["timestamp"][1])
                data.insert(s-1,element)
            else:
                end_element=element
        
        return data
    
    def Load_model(self):
        # 1. Model ve Processor'ı Doğrudan Yükleme [1]
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_name, dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(self.device)
        
        processor = AutoProcessor.from_pretrained(self.model_name)

        return model,processor


    def Load_file(self,audio_path, sr=16000):
        # Not: Ses dosyasını yüklemek için kaynaklarda belirtilmeyen 'librosa' gibi 
        # harici bir kütüphane kullanmanız gerekebilir (Bu bilgi kaynak dışıdır).
        speech, sr = librosa.load(audio_path, sr=sr) # Whisper 16kHz ile çalışır

        return speech, sr

    def Load_data(self,audio_bytes_data, sr=16000):
        # Not: Ses dosyasını yüklemek için kaynaklarda belirtilmeyen 'librosa' gibi 
        # harici bir kütüphane kullanmanız gerekebilir (Bu bilgi kaynak dışıdır).
        speech, sr = librosa.load(io.BytesIO(audio_bytes_data),sr=sr) # Whisper 16kHz ile çalışır

        return speech, sr

    def clear_memory(self,extra_params):
        torch.cuda.empty_cache()

        del extra_params
            
    def preadiction(self,speech,sr=16000):


        
        samples_per_chunk = self.chunk_length * sr
        total_chunks = (len(speech) // samples_per_chunk) + 1
        
        #print(f"Toplam {total_chunks} parça işlenecek...")

        

        # 3. Manuel İlerleme Çubuğu ile Döngü
        with tqdm(total=total_chunks) as pbar:
            result=[]
            for s,i in enumerate(range(0, len(speech), samples_per_chunk)):
                # Ses parçasını al
                chunk = speech[i : i + samples_per_chunk]
                
                # Processor: Ses verisini modelin anlayacağı Mel-spektrograma çevirir [1, 5]
                input_features = self.processor(chunk, sampling_rate=sr, return_tensors="pt").input_features
                input_features = input_features.to(self.device).to(self.torch_dtype)
                
                # Model.generate: Metin üretim aşaması [1]
                with torch.no_grad():
                    #predicted_ids = self.model.generate(input_features,**self.generate_kwargs) # Dil seçimi [6]
                    
                    predicted_ids = self.model.generate(input_features,
                                                        max_length                  = self.max_length,
                                                        condition_on_prev_tokens    = self.condition_on_prev_tokens,
                                                        compression_ratio_threshold = self.compression_ratio_threshold,
                                                        temperature                 = self.temperature,
                                                        logprob_threshold           = self.logprob_threshold,
                                                        no_speech_threshold         = self.no_speech_threshold,
                                                        return_timestamps           = self.return_timestamps,
                                                        language                    = self.language
                                                       ) 
                    
                # Decode: Sayısal çıktıları metne dönüştürür
                transcription = self.processor.batch_decode(*predicted_ids, skip_special_tokens=True,decode_with_timestamps=True)
                formatted_output=self.text_Totimestamps(transcription[0],start_time=s*30)
        
                self.clear_memory([input_features,transcription,predicted_ids])
                
                result+=formatted_output
                # Her parça bittiğinde ilerleme çubuğunu güncelle
                pbar.update(1)
        
            

            
        return self.remove_duplicates(result)
