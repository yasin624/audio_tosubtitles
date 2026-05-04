############################   Model Parameters
MODEL_NAME                  = "openai/whisper-large-v3"
MAX_LENGTH                  = 448                            # Uyarıyı kapatan kritik satır
NUM_BEAMS                   = 1
CONDITION_ON_PREV_TOKENS    = False                          # Önceki tokenlara bağımlılığı kapatır [1]
COMPRESSİON_RATİO_THRESHOLD = 1.35
TEMPERATURE                 = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0) # Temperature fallback stratejisi [1], [3]
LOGROB_THRESHOLD            = -1.0
NO_SPEECH_THRESHOLD         = 0.6
RETURN_TİMESTAMPS           = True                           # Zaman damgalarını tahmin etmesini sağlar [2]
LANGUAGE                    = "english"  #"turkish"

CHUNK_LENGTH                = 30
