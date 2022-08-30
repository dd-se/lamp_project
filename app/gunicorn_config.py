from multiprocessing import cpu_count

workers = cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
reload = True

accesslog = "-"
errorlog = "-"
