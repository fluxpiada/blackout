import shutil
import os

def main():
    # Ensure dist/ exists
    os.makedirs("dist", exist_ok=True)

    # Copy the static index.html
    shutil.copyfile("index.html", "dist/index.html")

    # Copy styles/
    if os.path.isdir("styles"):
        shutil.copytree("styles", "dist/styles", dirs_exist_ok=True)

    # Copy images/
    if os.path.isdir("images"):
        shutil.copytree("images", "dist/images", dirs_exist_ok=True)

if __name__ == "__main__":
    main()
