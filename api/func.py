from tools import data_to_srt,data_to_vtt

def  variable_controls(model,request_variables):

    variables=request_variables.keys()
    
    if "max_length" in variables:
        model.max_length=int(request_variables["max_length"])
        
    if "num_beams" in variables:
        model.num_beams=int(request_variables["num_beams"])

    if "condition_on_prev_tokens" in variables:
        model.condition_on_prev_tokens=bool(request_variables["condition_on_prev_tokens"])
        
    if "compression_ratio_threshold" in variables:
        model.compression_ratio_threshold=float(request_variables["compression_ratio_threshold"])

    if "temperature" in variables:
        model.temperature=tuple(request_variables["temperature"])
        
    if "logprob_threshold" in variables:
        model.logprob_threshold=float(request_variables["logprob_threshold"])

    if "no_speech_threshold" in variables:
        model.no_speech_threshold=float(request_variables["no_speech_threshold"])
        
    if "return_timestamps" in variables:
        model.return_timestamps=bool(request_variables["return_timestamps"])

    if "language" in variables:
        model.language=request_variables["language"]
        
    if "chunk_length" in variables:
        model.chunk_length=int(request_variables["chunk_length"])


def format_converter (data,request_variables):
    variables=request_variables.keys()
    
    if "subtitle_type" in variables:
        if "str"  ==  request_variables["subtitle_type"]:
            return data_to_srt(data)

        elif "vtt" == request_variables["subtitle_type"]:
            return data_to_vtt(data)


        else:
            return data_to_srt(data)
    else:
        return data_to_srt(data)

        
def save_data(file_path, data,write_type="wb"):
    with open(file_path,write_type) as file:
        file.write(data)
