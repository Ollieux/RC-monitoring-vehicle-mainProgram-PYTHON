import queue

c= 7
q = queue.Queue()

q.put(5)
q.put(3)


for i in range(10):

    try:
        qq = q.get()
        print(qq)

    except queue.Empty as e:
        print(e)
        print(":(")


