from multiprocessing import cpu_count

workers = cpu_count() * 2 + 1
bind = "127.0.0.1:8000"
worker_class = "uvicorn.workers.UvicornWorker"
reload = True

accesslog = "-"
errorlog = "-"
