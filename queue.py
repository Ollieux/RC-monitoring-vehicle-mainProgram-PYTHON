import queue

c= 7
a = queue.Queue()

a.put(5)
a.put(3)


for i in range(10):

    try:
        b = a.get()
        print(b)

    except queue.Empty as e:
        print(e)
        print(":(")


