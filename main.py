from transmitter import Transmitter

print("""

   _____       _  __   _____                _   _                           _                 _   _             
  / ____|     | |/ _| |  __ \              | | (_)              /\         (_)               | | (_)            
 | |  __  ___ | | |_  | |__) | __ __ _  ___| |_ _  ___ ___     /  \   _ __  _ _ __ ___   __ _| |_ _  ___  _ __  
 | | |_ |/ _ \| |  _| |  ___/ '__/ _` |/ __| __| |/ __/ _ \   / /\ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \ 
 | |__| | (_) | | |   | |   | | | (_| | (__| |_| | (_|  __/  / ____ \| | | | | | | | | | (_| | |_| | (_) | | | |
  \_____|\___/|_|_|   |_|   |_|  \__,_|\___|\__|_|\___\___| /_/    \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|
                                                                                                                
  ___          _               _   ___                      
 | _ ) __ _ __| |_____ _ _  __| | / __| ___ _ ___ _____ _ _ 
 | _ \/ _` / _| / / -_) ' \/ _` | \__ \/ -_) '_\ V / -_) '_|
 |___/\__,_\__|_\_\___|_||_\__,_| |___/\___|_|  \_/\___|_|  
                                                            
""")

link = Transmitter()

link.connect()

while True:
    msg = input("input message: ")
    link.send(msg)
