from speaker_diarization_utils import convert_rttm_to_csv, convertmp3towav, diarize_audio
from pydub import AudioSegment

from transcription_utils import transcribe


def diarization_function(audio)->any:
    """
    Inputs:
    audio: str
        Path to the audio file

    Outputs:
    None
    """
    print("Path of the file:", audio)
    # get file name
    file_name = audio.split("/")[-1].split(".")[0]
    wav_file_path = "audio_wav/"+file_name+".wav"
    diarize_audio_path = "diarized_audio/"+file_name+".rttm"
    # convert mp3 to wav
    convertmp3towav(audio, wav_file_path)
    # diarize the audio file
    diarized_audio = diarize_audio(wav_file_path)
    with open(diarize_audio_path, "w") as f:
        diarized_audio.write_rttm(f)

    df = convert_rttm_to_csv(diarize_audio_path)
    
    sound = AudioSegment.from_wav(wav_file_path)

    with open('Final_tsv/'+file_name+'.tsv', 'a') as f:
        for i in range(len(df)):
            timings = [df.iloc[i]['start_time'], df.iloc[i]['end_time']]
            extract = sound[timings[0]:timings[1]]
            extract.export("portion.mp3", format="mp3")
            transcription = transcribe("portion.mp3")

            hrs_start = "{:02d}".format(int(timings[0]/(1000*60*60)))
            mins_beg = "{:02d}".format(int((timings[0]/(1000*60))%60))
            secs_beg = "{:02d}".format(int((timings[0]/1000)%60))

            start_time = hrs_start+":"+mins_beg+":"+secs_beg

            hrs_end = "{:02d}".format(int(timings[1]/(1000*60*60)))
            mins_end = "{:02d}".format(int((timings[1]/(1000*60))%60))
            secs_end = "{:02d}".format(int((timings[1]/1000)%60))

            end_time = hrs_end+":"+mins_end+":"+secs_end

            f.write(df.iloc[i]['speaker_name']+"\t"+start_time+"\t"+end_time+"\t"+transcription+"\n")


