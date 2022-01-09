import time

from fastapi import FastAPI, Request


def before_route(request):
    print("---isshe--- before_route---")


def after_route(response):
    print("---isshe--- after_route---")


async def handler(request: Request, call_next):
    start_time = time.time()
    before_route(request)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    after_route(response)
    return response
