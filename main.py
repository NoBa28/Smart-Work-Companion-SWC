from services.task_service import TaskService


def main():
    service = TaskService()

    task = service.add_task("Test Task", "high")
    print("Created: ", task)

    tasks = service.get_tasks()
    print("All Tasks: ", tasks)


if __name__ == "__main__":
    main()
