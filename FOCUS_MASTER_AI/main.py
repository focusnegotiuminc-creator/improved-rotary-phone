import os
from core.orchestration import run_task


def main():
    print("FOCUS MASTER AI ENGINE STARTED")

    while True:
        task = input("Enter command: ")

        if task.lower() == "exit":
            break

        result = run_task(task)
        print(result)


if __name__ == "__main__":
    main()
