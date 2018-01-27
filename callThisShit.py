import subprocess
from threading import Thread
import os



def callReferee(teamName1 = 'knuckles', teamName2 = 'notKnuckles'):
    subprocess.call(['python.exe', 'referee.py', teamName1, teamName2])
def callAgent():
    subprocess.call(['python.exe', 'agent.py'])
def removeFiles(teamName1 = 'knuckles', teamName2 = 'notKnuckles'):
    listOfFiles = [teamName1 + ".go", teamName2 + ".go", "move_file",
                   "history_file", "end_game"]
    for e in listOfFiles:
        try:
            os.remove(os.path.join('./', e))
        except:
            print("No file named " + e)

removeFiles()
thread = Thread(target = callReferee)
thread2 = Thread(target = callAgent)
thread.start()
thread2.start()
thread.join()
