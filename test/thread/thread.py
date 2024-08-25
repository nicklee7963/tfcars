import threading
import time


done = False



def worker(text):

    counter = 0

    while True:

        time.sleep(1)

        counter += 1

        print(f"{text} : {counter}")



threading.Thread(target=worker, daemon = True, args = ("ABC",)).start()





input("press enter to quit")

done = True