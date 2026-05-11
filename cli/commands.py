import argparse
import json

from services.task_service import TaskService
from services.note_service import NoteService
from services.tracker_service import TrackerService
from services.report_service import ReportService


def main():
    parser = argparse.ArgumentParser(description="Smart Work Companion CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Tasks
    tasks_parser = subparsers.add_parser("tasks", help="Manage tasks")
    tasks_sub = tasks_parser.add_subparsers(dest="subcommand")
    tasks_sub.add_parser("list", help="List all tasks")

    add_p = tasks_sub.add_parser("add", help="Add a task")
    add_p.add_argument("title")
    add_p.add_argument("priority", choices=["low", "medium", "high"])

    comp_p = tasks_sub.add_parser("complete", help="Mark task done")
    comp_p.add_argument("task_id")

    del_p = tasks_sub.add_parser("delete", help="Delete task")
    del_p.add_argument("task_id")

    # Notes
    notes_parser = subparsers.add_parser("notes", help="Manage notes")
    notes_sub = notes_parser.add_subparsers(dest="subcommand")
    notes_sub.add_parser("list", help="List notes")

    note_add = notes_sub.add_parser("add", help="Add note")
    note_add.add_argument("text", nargs="+")

    note_del = notes_sub.add_parser("delete", help="Delete note")
    note_del.add_argument("note_id")

    # Tracker
    track_parser = subparsers.add_parser("tracker", help="Time tracking")
    track_sub = track_parser.add_subparsers(dest="subcommand")
    start_p = track_sub.add_parser("start", help="Start session")
    start_p.add_argument("project")
    start_p.add_argument("task_id")

    track_sub.add_parser("stop", help="Stop active session")
    track_sub.add_parser("status", help="Show active session")

    # Report
    rep_parser = subparsers.add_parser("report", help="Generate report")
    rep_parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    task_service = TaskService()
    note_service = NoteService()
    tracker_service = TrackerService()
    report_service = ReportService(task_service, tracker_service, note_service)

    if args.command == "tasks":
        if args.subcommand == "list":
            for t in task_service.get_tasks():
                print(f"{t.id} | {t.title} | {t.priority} | {'done' if t.done else 'open'}")
        elif args.subcommand == "add":
            task = task_service.add_task(args.title, args.priority)
            print("Created:", task.id)
        elif args.subcommand == "complete":
            task_service.complete_task(args.task_id)
            print("Completed")
        elif args.subcommand == "delete":
            task_service.delete_task(args.task_id)
            print("Deleted")

    elif args.command == "notes":
        if args.subcommand == "list":
            for n in note_service.get_notes():
                print(f"{n.id} | {n.text[:50]}... | {n.created_at}")
        elif args.subcommand == "add":
            text = " ".join(args.text)
            note = note_service.add_note(text)
            print("Created:", note.id)
        elif args.subcommand == "delete":
            note_service.delete_note(args.note_id)
            print("Deleted")

    elif args.command == "tracker":
        if args.subcommand == "start":
            sess = tracker_service.start_session(args.project, args.task_id)
            print("Started:", sess.id)
        elif args.subcommand == "stop":
            active = tracker_service.get_active_session()
            if active:
                stopped = tracker_service.stop_session(active.id)
                print("Stopped:", stopped.id)
            else:
                print("No active session")
        elif args.subcommand == "status":
            active = tracker_service.get_active_session()
            print(active or "No active session")

    elif args.command == "report":
        if args.json:
            print(json.dumps(report_service.generate_report(), indent=2))
        else:
            print("Total tracked seconds:", report_service.get_total_tracked_time())
            print("Open tasks:", report_service.get_open_tasks_count())
            active = report_service.get_active_session_report()
            print("Active:", active)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
