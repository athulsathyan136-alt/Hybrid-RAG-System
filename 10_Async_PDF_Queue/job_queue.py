import json
from pathlib import Path


QUEUE_FILE = Path("queue.json")


def create_queue():
    """Create an empty queue if it does not exist."""

    if not QUEUE_FILE.exists():
        QUEUE_FILE.write_text("[]")


def add_job(job):
    """Add a new job to the queue."""

    create_queue()

    jobs = json.loads(QUEUE_FILE.read_text())

    jobs.append(job)

    QUEUE_FILE.write_text(
        json.dumps(jobs, indent=4)
    )

    print("✅ Job added to queue")


def get_jobs():
    """Return all jobs in the queue."""

    create_queue()

    return json.loads(
        QUEUE_FILE.read_text()
    )


def remove_job(job_id):
    """Remove a job from the queue."""

    jobs = get_jobs()

    jobs = [
        job for job in jobs
        if job["id"] != job_id
    ]

    QUEUE_FILE.write_text(
        json.dumps(jobs, indent=4)
    )


if __name__ == "__main__":

    create_queue()

    print("Queue created successfully!")

    print("Current jobs:")
    print(get_jobs())