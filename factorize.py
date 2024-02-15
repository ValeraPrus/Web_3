import multiprocessing
from time import time


def factorize(*number):
    result = []
    for num in number:
        num_result = []
        for i in range(1, num + 1):
            if num % i == 0:
                num_result.append(i)
        result.append(f'assert {num} == {num_result}')
    return result


def factorize_process(*number):
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.map_async(factorize, number, callback=show)
        pool.close()
        pool.join()


def show(result):
    for num in result:
        print(num[0])


if __name__ == '__main__':
    print('Synchronous start:')
    start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(f'{a}\n{b}\n{c}\n{d}')
    end = time()
    print(f'Execution time : {end - start} sec\n')

    print('Asynchronous start:')
    print(f'The number of processor cores : {multiprocessing.cpu_count()}')
    start = time()
    factorize_process(128, 255, 99999, 10651060)
    end = time()
    print(f'Execution time : {end - start} sec\n')
