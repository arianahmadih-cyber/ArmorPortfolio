#!/usr/bin/env python3
# todo.py - یک برنامهٔ سادهٔ فهرست کارها با ذخیره در JSON

import json
from pathlib import Path
import argparse
import datetime
import sys

DATA_FILE = Path.home() / ".todo_cli.json"

def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

def add_task(text, due=None, priority="normal"):
    tasks = load_tasks()
    task = {
        "id": int(datetime.datetime.now().timestamp()*1000),
        "text": text,
        "created": datetime.datetime.now().isoformat(),
        "due": due,
        "priority": priority,
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("کار اضافه شد:", text)

def list_tasks(all=False):
    tasks = load_tasks()
    if not tasks:
        print("هیچ کاری وجود ندارد.")
        return
    def fmt(t):
        status = "✔" if t["done"] else " "
        du = f" | due: {t['due']}" if t.get("due") else ""
        pr = f" | pr: {t.get('priority','')}"
        return f"[{status}] id:{t['id']} {t['text']}{du}{pr}"
    shown = tasks if all else [t for t in tasks if not t["done"]]
    for t in shown:
        print(fmt(t))

def done_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if str(t["id"]) == str(task_id):
            t["done"] = True
            save_tasks(tasks)
            print("علامت انجام خورد:", t["text"])
            return
    print("کار با این id پیدا نشد.")

def remove_task(task_id):
    tasks = load_tasks()
    new = [t for t in tasks if str(t["id"]) != str(task_id)]
    if len(new) == len(tasks):
        print("کار با این id پیدا نشد.")
    else:
        save_tasks(new)
        print("کار حذف شد.")

def parse_args():
    p = argparse.ArgumentParser(description="Todo CLI ساده")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add", help="اضافه کردن کار")
    a.add_argument("text", nargs="+", help="متن کار")
    a.add_argument("--due", help="موعد (مثلاً 2025-10-20)")
    a.add_argument("--priority", choices=["low","normal","high"], default="normal")

    l = sub.add_parser("list", help="نمایش کارها")
    l.add_argument("--all", action="store_true", help="نمایش همه (شامل انجام‌شده‌ها)")

    d = sub.add_parser("done", help="علامت‌زدن کار به‌عنوان انجام شده")
    d.add_argument("id", help="id کار")

    r = sub.add_parser("rm", help="حذف کار")
    r.add_argument("id", help="id کار")

    return p.parse_args()

def main():
    args = parse_args()
    if args.cmd == "add":
        add_task(" ".join(args.text), due=args.due, priority=args.priority)
    elif args.cmd == "list":
        list_tasks(all=args.all)
    elif args.cmd == "done":
        done_task(args.id)
    elif args.cmd == "rm":
        remove_task(args.id)
    else:
        print("دستوری وارد نشده — از یکی از: add, list, done, rm استفاده کن.")
        print("مثال‌ها:")
        print("  python todo.py add خرید نان --due 2025-10-12 --priority high")
        print("  python todo.py list --all")
        print("  python todo.py done 1632432340000")
    main(l)