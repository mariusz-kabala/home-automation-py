from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *


store = {'client_key': '2c6b66bcc523e69ee89d2c7200ddedf8'}

def start():
    client = WebOSClient("192.168.50.3")
    
    client.connect()
    
    for status in client.register(store):
        print(status)
    

    media = MediaControl(client)
    bt_source = AudioOutputSource('bt_soundbar') #bt_soundbar tv_speaker
    speaker_source = AudioOutputSource('tv_speaker') #bt_soundbar tv_speaker
    # media.volume_up()
    audio_outputs = media.list_audio_output_sources()
    cur_media_output_source = media.get_audio_output()
    # media.set_audio_output(speaker_source)
    # media.set_audio_output(bt_source)
    # print(audio_outputs)
    # print(cur_media_output_source)

    # system = SystemControl(client)
    # system.notify("dzidziek jest glupi")

    # print(system.info())

    source_control = SourceControl(client)
    sources = source_control.list_sources()
    print(sources)

    app = ApplicationControl(client)
    # apps = app.list_apps()
    # print(apps)
    app_id = app.get_current() 
    print(app_id)
    inp = InputControl(client)
    inp.connect_input()
    inp.ok()
    inp.move(10, 10)    # Moves mouse
    inp.click()  
    inp.enter()
    inp.click()

    # media.set_audio_output(bt_source) 
    # for status in client.register(store):
    #     if status == WebOSClient.PROMPTED:
    #         print("Please accept the connect on the TV!")
    #     elif status == WebOSClient.REGISTERED:
    #         print("Registration successful!")
    #         print(store)




