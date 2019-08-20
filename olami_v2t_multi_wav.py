from asrapi import SpeechAPISample
import time
import json
import os
def main():
    f=open('log.txt','w+')
    compressed=False    #audio file = wav PCM => False, Speex  compress=True
    url="https://tw.olami.ai/cloudservice/api"
    appKey=""     #yourappkey
    appSecret=""  #your appSecert
    audioPath=""    #     wav file location folder
    files = os.listdir(audioPath)
    asrapi=SpeechAPISample()   #set asrapi as class of  SpeechAPI Sample
    asrapi.setLocalization(url)
    asrapi.setAuthorization(appKey,appSecret)
    for wav in files:
        if ".wav" in wav:
            wavPath=audioPath+"\\"+wav
            '''starting sending file for vioce recognition'''
            print("\n-------Testing Speech API-------\n")
            print("\nsending audio file......\n")
            response_string=asrapi.sendAudioFile(asrapi.API_NAME_ASR,"nli,seg",True,wavPath,compressed)
            print("\n\nResult:\n\n",response_string,"\n")

            '''try to get result if uploaded is successful'''
            if ("error" not in response_string.lower()):
                print("\n--------get recognition result--------\n")
                time.sleep(1)
                '''try to get result until the end of recognition is completed'''
                while(True):
                    response_string=asrapi.getRecognitionResult(asrapi.API_NAME_ASR,"nli,seg")
                    print("\n\n result\n\n", response_string,"\n")
                    if ("\"final\":true" not in response_string.lower()):
                        print("recognition process is not yet finish")
                        if ("error" in response_string.lower()):
                            break
                        time.sleep(2)
                    else:
                        break
            print("\n\n")
            d = json.loads(response_string)
            f.write(wav+" "+"v2t:"+d['data']['asr']['result']+" "+"nli:"+d['data']['nli'][0]['desc_obj']['result']+"\n")
    f.close()
#if __name__=='__main__':
main()



