def get_workers():
    # import multiprocessing
    # return multiprocessing.cpu_count() * 2 + 1
    return 2


bind = "0.0.0.0:8000"
workers = get_workers()
