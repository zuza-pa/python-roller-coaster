import time
import threading as thr

customers = 0
riders = 0

boarders = 0
unboarders = 0

boardLock = thr.Lock()
unboardLock = thr.Lock()

boardQueue = thr.Semaphore(0)
unboardQueue = thr.Semaphore(0)
allAboard = thr.Semaphore(0)
allAshore = thr.Semaphore(0)

def boardPassenger():
    boardQueue.acquire()
    global boardLock
    boardLock.acquire()
    global boarders
    boarders = boarders+1
    print("Boarded: %d"%(boarders))
    if boarders == 10:
        allAboard.release();
        boarders = 0;
    boardLock.release()
    
    unboardQueue.acquire()
    unboardLock.acquire()
    global unboarders
    unboarders += 1
    print("Unboarded: %d"%(unboarders))
    if unboarders == 10:
        allAshore.release()
        unboarders = 0
    unboardLock.release()

def rollerCoasterEntry():
    # Creates multiple threads inside to simulate people coming to the roller coaster
    while(True):
        time.sleep(1)
        incomingPerson = thr.Thread(target=boardPassenger)
        incomingPerson.start()

        global customers
        customers = customers+1
        print("Customers: %d"%(customers))

def rollerCoasterRide():
    while(True):
        for i in range(10):
            boardQueue.release() 
        allAboard.acquire()
        print("We are going!")
        time.sleep(10)
        for i in range(10):
            unboardQueue.release()
            global riders
            riders = riders+1
        allAshore.acquire()
        print("Satisfied customers with ride: %d"%(riders))

rollerCoasterEntryThread = thr.Thread(target=rollerCoasterEntry)
rollerCoasterRideThread = thr.Thread(target=rollerCoasterRide)

rollerCoasterEntryThread.start()
rollerCoasterRideThread.start()