import time
import random
import asyncio
import threading
import multiprocessing as mp


def measure(title, func):
    start = time.time()
    result = func()
    end = time.time()

    print(f"\n{title}")
    print(f"Время выполнения: {end - start:.2f} сек.")
    return result


def process_order(order_id):
    time.sleep(random.uniform(1, 2))

    total = 0
    for i in range(300_000):
        total += (i * i) % 97

    print(f"Заказ {order_id} обработан, результат: {total}")
    return total


def part1_sync():
    results = []

    for order_id in range(1, 6):
        results.append(process_order(order_id))

    return results


def part1_threading():
    threads = []
    results = [None] * 5

    def worker(index, order_id):
        results[index] = process_order(order_id)

    for i in range(5):
        thread = threading.Thread(target=worker, args=(i, i + 1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


def heavy_calculation(n):
    total = 0

    for i in range(1, n):
        total += (i * i) % 123
        total += (i ** 2) % 97
        total += (i * 3) % 17

    return total


def part2_sync(numbers):
    return [heavy_calculation(n) for n in numbers]


def part2_multiprocessing(numbers):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        return pool.map(heavy_calculation, numbers)


async def async_service_request(user_id):
    await asyncio.sleep(random.uniform(1, 2))

    total = 0

    for i in range(500_000):
        if i % 2 == 0:
            total += (i * user_id) % 101

    print(f"Пользователь {user_id}: результат {total}")
    return total


async def part3_async():
    tasks = []

    for user_id in range(1, 11):
        tasks.append(async_service_request(user_id))

    return await asyncio.gather(*tasks)


def run_part3():
    start = time.time()
    results = asyncio.run(part3_async())
    end = time.time()

    print("\nЧасть 3 — Async")
    print(f"Время выполнения: {end - start:.2f} сек.")

    return results


def universal_task(task_id):
    time.sleep(1)

    total = 0

    for i in range(700_000):
        total += (i * task_id) % 89
        total += (i ** 2) % 31

    time.sleep(1)

    final_result = total + task_id

    print(f"Задача {task_id} завершена, результат: {final_result}")

    return final_result


def part4_sync():
    results = []

    for task_id in range(1, 6):
        results.append(universal_task(task_id))

    return results


def part4_threading():
    threads = []
    results = [None] * 5

    def worker(index, task_id):
        results[index] = universal_task(task_id)

    for i in range(5):
        thread = threading.Thread(target=worker, args=(i, i + 1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


def part4_multiprocessing():
    task_ids = list(range(1, 6))

    with mp.Pool(processes=mp.cpu_count()) as pool:
        return pool.map(universal_task, task_ids)


if __name__ == "__main__":
    print("\n===== Часть 1 — Threading =====")

    sync_results_1 = measure(
        "Синхронное выполнение",
        part1_sync
    )

    thread_results_1 = measure(
        "Threading выполнение",
        part1_threading
    )

    print("\nРезультаты совпадают:")
    print(sync_results_1 == thread_results_1)

    print("\n===== Часть 2 — Multiprocessing =====")

    numbers = [3_000_000] * 5

    sync_results_2 = measure(
        "Последовательное выполнение",
        lambda: part2_sync(numbers)
    )

    mp_results_2 = measure(
        "Multiprocessing выполнение",
        lambda: part2_multiprocessing(numbers)
    )

    print("\nРезультаты совпадают:")
    print(sync_results_2 == mp_results_2)

    print("\n===== Часть 3 — Async =====")

    async_results = run_part3()

    print("\nПолучено результатов:")
    print(len(async_results))

    print("\n===== Часть 4 — Смешанный сценарий =====")

    sync_results_4 = measure(
        "Sync выполнение",
        part4_sync
    )

    thread_results_4 = measure(
        "Threading выполнение",
        part4_threading
    )

    mp_results_4 = measure(
        "Multiprocessing выполнение",
        part4_multiprocessing
    )

    print("\nSync == Threading:")
    print(sync_results_4 == thread_results_4)

    print("\nSync == Multiprocessing:")
    print(sync_results_4 == mp_results_4)
