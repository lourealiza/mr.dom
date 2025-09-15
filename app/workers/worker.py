from rq import Worker, Queue
from redis import Redis
from app.core.settings import settings

listen = ["events"]
redis = Redis.from_url(settings.REDIS_URL)

if __name__ == "__main__":
    worker = Worker(map(Queue, listen), connection=redis)
    worker.work(with_scheduler=True)
