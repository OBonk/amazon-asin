from tkinter import *
import amz
import asyncio
import threading
import random

async def begin(key,zipcode,runner,max,min,coupon):
    await run(key,zipcode,runner,max,min,coupon)
    
async def run(key,zipcode,runner,max,min,coupon):
    await amz.main(key,zipcode,runner,max=max,min=min,coupon=coupon)
def stopper(runner):
    #print(running)
    #if running:
        #raise (KeyboardInterrupt)
    runner.append("stop")



def do_tasks(async_loop,key,zipcode,runner,max,min,coupon):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,key,zipcode,runner,max,min,coupon)).start()
def _asyncio_thread(async_loop,key,zipcode,runner,max,min,coupon):
    async_loop.run_until_complete(begin(key,zipcode,runner,max,min,coupon))

def main(async_loop):
    root = Tk()
    fg = "#00B900"
    bg = "#404040"
    costs = ["1","25","50","100"]
    runner = []
    root.title("Amazon Asin Search")
    root.geometry("170x400")
    root.configure(background="#000000")
    zipL = Label(foreground=fg,background="#000000",width =20,text="Enter search zip")
    zipL.grid(row=3,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    searchzip = Entry(foreground=fg,background=bg,width =20)
    searchzip.grid(row=4,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    keyL = Label(foreground=fg,background="#000000",width =20,text="Enter search word")
    keyL.grid(row=1,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    searchkey = Entry(foreground=fg,background=bg,width =20)
    searchkey.grid(row=2,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    minL = Label(foreground=fg,background="#000000",width =20,text="Enter min price")
    min = StringVar()
    min.set("")
    minL.grid(row=5,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    r =6
    for cost in costs:
        Radiobutton(root, 
                   text=cost,
                   padx = 20, 
                   variable=min, 
                   value=cost,
                   foreground=fg,background="#000000").grid(column=2,row=r)
        r +=1
    maxL = Label(foreground=fg,background="#000000",width =20,text="Enter max price")
    maxL.grid(row=11,column =2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    max = StringVar()
    max.set("")
    r = 12
    for cost in costs:
        Radiobutton(root, 
                   text=cost,
                   padx = 20, 
                   variable=max, 
                   value=cost,
                   foreground=fg,background="#000000").grid(column=2,row=r)
        r+=1
    
    i = IntVar()
    coupon = Checkbutton(text="coupon",variable=i,foreground=fg,background=bg)
    coupon.grid(row=17, column = 2)
    go = Button(text="Search",foreground=fg,background=bg,width =20,command= lambda: do_tasks(async_loop,searchkey.get(),searchzip.get(),runner,max.get(),min.get(),bool(i.get())))
    go.grid(row=18,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    stop = Button(text="Stop",state = NORMAL,foreground=fg,background=bg,width =20,command= lambda: stopper(runner))
    stop.grid(row=19,column=2, columnspan = 1, rowspan = 1,padx = 10, pady = 2)
    root.mainloop()
if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
