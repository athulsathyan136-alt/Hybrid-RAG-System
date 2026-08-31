import time
from pathlib import Path

from pypdf import PdfReader

from job_queue import get_jobs, remove_job


INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def process_pdf(job):
    """Extract text from a PDF."""

    filename = job["file"]

    pdf_path = INPUT_DIR / filename
    output_path = OUTPUT_DIR / f"{pdf_path.stem}.txt"

    print("\n================================")
    print("Processing PDF")
    print("================================")

    print("Job ID:", job["id"])
    print("PDF:", pdf_path)

    if not pdf_path.exists():
        print("❌ PDF not found:", pdf_path)
        return False

    try:
        reader = PdfReader(pdf_path)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        output_path.write_text(
            extracted_text,
            encoding="utf-8"
        )

        print("Pages:", len(reader.pages))
        print("✅ Text extracted successfully!")
        print("Saved to:", output_path)

        return True

    except Exception as error:
        print("❌ Error:", error)
        return False


def main():

    print("================================")
    print("       PDF QUEUE WORKER")
    print("================================")

    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    jobs = get_jobs()

    if not jobs:
        print("📭 No jobs in queue.")
        return

    for job in jobs:

        success = process_pdf(job)

        if success:
            remove_job(job["id"])
            print("✅ Job removed from queue.")
        else:
            print("⚠️ Job kept in queue.")


if __name__ == "__main__":
    main()