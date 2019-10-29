import threading
import time

MAX_ELFS = 9

mutex = threading.Semaphore(3) ## Controla seccio critica
noSomTres = threading.Semaphore(0) ## Esperen a ser tres per demanar ajuda
ajuda = threading.Semaphore(0) ## S'ha d'ajudar

elfs_quest = 0

def elf():
    global elfs_quest
    print("Hi som l'elf-{}".format(threading.current_thread().name))
    time.sleep(1)
    mutex.acquire()
    elfs_quest += 1
    if(elfs_quest == 3):
        print("Elf-{} says: I have a question, I'm the {} SANTAAA !".format(threading.current_thread().name,elfs_quest))
        ajuda.release()
    else:
        print("Elf-{} says: I have a question, I'm the {} waiting ...".format(threading.current_thread().name,elfs_quest))
    noSomTres.acquire()
    mutex.release()
    print("Elf-{} is getting help".format(threading.current_thread().name))
    time.sleep(3)
    print("BYE elf-{}".format(threading.current_thread().name))
    
def santaclaus():
    global elfs_quest
    
    print("----> Santa says: I'm tired")
    for i in range(3):
        print("----> Santa says: I'm going to sleep")
        ajuda.acquire()
        elfs_quest = 0
        print("----> Santa says: I'm awake ho ho ho!")
        print("----> Santa says: What is thre problem?")
        for i in range(3):
            print("----> Santa helps the {} of 3".format(i+1))
            noSomTres.release()
    
def main():
    threads = []

    t = threading.Thread(target=santaclaus, name="Santa Claus")
    threads.append(t)
    for i in range(MAX_ELFS):
        t = threading.Thread(target=elf, name=str(i))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("FINISH !!")

if __name__ == "__main__":
    main()