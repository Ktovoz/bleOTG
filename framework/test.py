import asyncio

async def my_coroutine():
    print("开始我的协程")
    await asyncio.sleep(1)  # 模拟IO操作
    print("完成我的协程")
    return "结果1"

async def another_coroutine():
    print("开始另一个协程")
    await asyncio.sleep(2.5)  # 模拟IO操作
    print("完成另一个协程")
    return "结果2"

async def third_coroutine():
    print("开始第三个协程")
    await asyncio.sleep(4)  # 模拟IO操作
    print("完成第三个协程")
    return "结果3"

async def producer(queue):
    for i in range(5):
        print(f"生产者正在生产 {i}")
        await queue.put(i)
        await asyncio.sleep(1)
    await queue.put(None)  # 发送结束信号

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消费者正在消费 {item}")
        queue.task_done()

async def main():
    # 使用 asyncio.gather 并发运行多个任务
    print("\n使用 asyncio.gather:")
    results = await asyncio.gather(
        my_coroutine(),
        another_coroutine(),
        third_coroutine()
    )
    print("所有任务完成，结果:", results)

    # 使用 asyncio.wait 等待多个任务
    print("\n使用 asyncio.wait:")
    tasks = [
        asyncio.create_task(my_coroutine()),
        asyncio.create_task(another_coroutine()),
        asyncio.create_task(third_coroutine())
    ]

    done, pending = await asyncio.wait(tasks)
    for task in done:
        print("任务完成，结果:", task.result())

    # 使用 asyncio.Queue 进行任务队列管理
    print("\n使用 asyncio.Queue:")
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.join()  # 等待所有任务完成
    consumer_task.cancel()  # 取消消费者任务

    await consumer_task

# 运行事件循环
asyncio.run(main())
