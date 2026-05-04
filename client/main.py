import requests
from tools import config,Menu
from tools.func import *
class CLIENT:
    def __init__(self):
        self.url=config.url
        self.variable=config.variables
        self.subtitle_url=self.url+"subtitles"



    def url_menu(self,inp):
        if inp.startswith("http://"):
            self.url=inp
            self.menu("start_menu")
        else:
            print("Note !!!  incorrect data ")
        
    
    def variable_menu(self,inp):
        try:
            variable= inp.split(":")
            self.variable[variable[0]]=variable[1]
            self.menu("start_menu")
        except:
            print("Note !!!  incorrect data ")

            
    def menu(self,menu):
        
        if menu=="start_menu":
            variable_str=""
            for i in self.variable:
                variable_str+= f"\t {i} : {self.variable[i]}"+"\n"


            status_code = requests.post(self.url).status_code

            service= "ACTIVE " if status_code ==200 else "PASFIVE"
            
            print(Menu.start_menu.format(url=self.url,variables=variable_str,service=service))

        elif menu=="help_menu":
            print(Menu.help_menu)

            
    def start(self):
        self.menu("start_menu")

        while True:
            inp=input("==>> ")
    
            if inp.startswith("/?") or inp.startswith("/h") or inp.startswith("/help"):
                self.menu("help_menu")
                
            elif inp.startswith("/url"):
                self.url_menu(inp.split()[1])
            elif inp.startswith("/variable"):
                self.variable_menu(inp.split()[1])
                
            elif inp.startswith("/file"):
                self.subtitle(inp.split()[1])
                                
            elif inp.startswith("/q"):
                break
    
            else:
                print("Note !!!  incorrect data ")
                


    def send_file(self,file_path):
        files = {
            "file": open(file_path, "rb")
        }
        

        response = requests.post(self.subtitle_url, files=files,data=self.variable)

        if response.status_code==200:
            return response.content
    def subtitle(self,file_path):

        if file_path[-3:]  not  in ["mp3","wav"]:
            tmp_file_path=cut_audio_fromvideo(file_path)
            
            content=self.send_file(tmp_file_path)
            
            save_data(tmp_file_path[:-4]+"."+self.variable["subtitle_type"],content)
            
        else:
            pass

client= CLIENT()


client.start()
        