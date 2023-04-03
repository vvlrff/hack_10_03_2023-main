# import sys
# import os
# sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем 

from aeromotus.parsing_aeromotus    import main as aero_main    #th0
from banggood.parsing_banggood      import main as bang_main    #th1
from dji.parsing_dji                import main as dji_main     #th2
from drone.parsing_drone            import main as drone_main   #th3
from nelk.parsing_nelk              import main as nelk_main    #th4
import pandas as pd

from threading import Thread
from time import sleep

def get_emptyDataframe( listColoms : list) -> pd.DataFrame: 
    # Создаём пустой DF с полями из списка listColoms
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def concat_list_of_df(list_df : list , listColumns : list) -> pd.DataFrame:
    cache_df =  get_emptyDataframe(listColumns) 
    for item_df in list_df:
        try:
            cache_df =  pd.concat([cache_df, item_df.get_val()])
        except Exception:
            pass
    return cache_df

def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'): 
    # Записываем полученный DF в JSON рядом с исполняемым файлом 
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')

def start_demons(list_threads : list) -> None:
    for thread in list_threads:
       thread.start()
    #    thread.join()

def get_content_in_thread( func):
    return func()

class CustomThread(Thread): # Создаём экземпляр потока Thread
    def __init__(self, var):
        Thread.__init__(self)
        self.daemon = True # Указываем, что этот поток - демон
        self.val = "None"
        self.var = var
        
    def run(self): # метод, который выполняется при запуске потока
        self.val = self.var()
        
    def get_val(self):
        return self.val

def main():
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    list_threads = [
                    CustomThread( aero_main ),
                    CustomThread( bang_main ),
                    CustomThread( dji_main ),
                    CustomThread( drone_main ),
                    CustomThread( nelk_main )
                   ]

    
    start_demons(list_threads)
    
    while True:
        sleep(3)
        b_in_progess = False
        for thread in list_threads:
            print(f" {thread.name} - {thread.is_alive()}")
            if  thread.is_alive() == True: b_in_progess = True
        if b_in_progess == False : 
            break
    
    cache = concat_list_of_df(list_threads, list_threads)
    make_jsonFile(cache, 'data_total')
            
                
                
            
    
    
    
    
    

print(f'{__name__} is here !')

if __name__ == '__main__': 
    main()
    



