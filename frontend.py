from tkinter import *
import amz
import asyncio
import threading
import random

async def begin(key,zipcode,runner):
    await run(key,zipcode,runner)
    
async def run(key,zipcode,runner):
    await amz.main(key,zipcode,runner)
def stopper(runner):
    #print(running)
    #if running:
        #raise (KeyboardInterrupt)
    runner.append("stop")



def do_tasks(async_loop,key,zipcode,runner):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,key,zipcode,runner)).start()
def _asyncio_thread(async_loop,key,zipcode,runner):
    async_loop.run_until_complete(begin(key,zipcode,runner))

def main(async_loop):
    root = Tk()
    fg = "#00B900"
    bg = "#404040"
    runner = []
    root.title("Amazon Asin Search")
    root.geometry("170x200")
    root.configure(background="#000000")
    zipL = Label(foreground=fg,background="#000000",width =20,text="Enter search zip")
    zipL.grid(row=1,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    searchzip = Entry(foreground=fg,background=bg,width =20)
    searchzip.grid(row=2,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    keyL = Label(foreground=fg,background="#000000",width =20,text="Enter search word")
    keyL.grid(row=3,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    searchkey = Entry(foreground=fg,background=bg,width =20)
    searchkey.grid(row=4,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    go = Button(text="Search",foreground=fg,background=bg,width =20,command= lambda: do_tasks(async_loop,searchkey.get(),searchzip.get(),runner))
    go.grid(row=5,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    stop = Button(text="Stop",state = NORMAL,foreground=fg,background=bg,width =20,command= lambda: stopper(runner))
    stop.grid(row=6,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    root.mainloop()
if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
