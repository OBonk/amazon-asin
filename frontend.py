from tkinter import *
import amz
import asyncio
import threading
import random

def begin(key,zipcode,stop):
    task = asyncio.ensure_future(run(key,zipcode))
    stop.state = NORMAL
async def run(key,zipcode):
    await amz.main(key,zipcode)


def do_tasks(async_loop):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()


def main(async_loop):
    root = Tk()
    fg = "#00B900"
    bg = "#404040"

    loop = asyncio.get_event_loop()
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
    go = Button(text="Search",foreground=fg,background=bg,width =20,command= lambda: begin(searchkey.get(),searchzip.get(),stop))
    go.grid(row=5,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    stop = Button(text="Stop",state = DISABLED,foreground=fg,background=bg,width =20,command=amz.stop)
    stop.grid(row=6,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    root.mainloop()
if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
