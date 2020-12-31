from fastapi import APIRouter
from fastapi import FastAPI, BackgroundTasks

from app.worker.celery_worker import celery_app

router = APIRouter()


def celery_on_message(body):
    print(body)

def background_on_message(task):
    print(task.get(on_message=celery_on_message, propagate=False))


@router.get("/{word}")
async def root(word: str, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "app.worker.celery_worker.test_celery", args=[word])
    print(task)
    background_task.add_task(background_on_message, task)
    return {"message": "Word received"}