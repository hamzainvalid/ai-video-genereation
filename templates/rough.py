from dotenv import load_dotenv
import os

load_dotenv()

apis = [os.getenv('NN_EL_API'),os.getenv('EXTRA_EL_API_1'),os.getenv('TG_EL_TTS_API')]
def api_iterator():
    api_works = False
    counter = 0
    api_key = ''
    print(len(apis))
    while api_works == False:
        if counter == len(apis) - 1:
            api_key = apis[counter]


        if api_key == apis[1]:
            api_works = True
            print(f'api {api_key} works')
        else:
            counter += 1

    print(apis)

api_iterator()