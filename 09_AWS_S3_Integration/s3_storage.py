from pathlib import Path
import shutil


# Local folder acting like an S3 bucket
BUCKET_DIR = Path("storage")

# Create storage directory if it doesn't exist
BUCKET_DIR.mkdir(exist_ok=True)


def upload_file(file_path):
    """
    Upload a file to our local S3 simulator.
    """

    source = Path(file_path)

    if not source.exists():
        print("❌ File not found:", file_path)
        return

    destination = BUCKET_DIR / source.name

    shutil.copy2(source, destination)

    print("✅ File uploaded successfully!")
    print("Stored at:", destination)


def list_files():
    """
    List files stored in our local bucket.
    """

    files = list(BUCKET_DIR.iterdir())

    if not files:
        print("📂 Bucket is empty.")
        return

    print("\n📦 Files in bucket:")

    for file in files:
        if file.is_file():
            print("-", file.name)


def download_file(filename):
    """
    Download a file from our local bucket.
    """

    source = BUCKET_DIR / filename

    if not source.exists():
        print("❌ File not found in bucket:", filename)
        return

    destination = Path("downloaded_" + filename)

    shutil.copy2(source, destination)

    print("✅ File downloaded!")
    print("Saved as:", destination)


def delete_file(filename):
    """
    Delete a file from our local bucket.
    """

    file_path = BUCKET_DIR / filename

    if not file_path.exists():
        print("❌ File not found:", filename)
        return

    file_path.unlink()

    print("✅ File deleted:", filename)


def main():

    print("================================")
    print("     LOCAL S3 STORAGE")
    print("================================")

    while True:

        print("\nChoose an option:")
        print("1. Upload file")
        print("2. List files")
        print("3. Download file")
        print("4. Delete file")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":

            file_path = input("Enter file path: ")

            upload_file(file_path)

        elif choice == "2":

            list_files()

        elif choice == "3":

            filename = input("Enter filename: ")

            download_file(filename)

        elif choice == "4":

            filename = input("Enter filename: ")

            delete_file(filename)

        elif choice == "5":

            print("Goodbye 👋")
            break

        else:

            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()