def prompt_for_tasks():
    tasks = []
    print("📆 Let's build your task calendar!")
    while True:
        # Task name
        while True:
            name = input("\n🔹 Task name: ").strip()
            if name:
                break
            print("❗ Task name is required.")

        # Deadline
        while True:
            deadline_raw = input(
                "📅 Deadline (YYYY-MM-DD or MM-DD, press Enter for today): "
            )
            try:
                deadline = parse_smart_deadline(deadline_raw)
                break
            except ValueError as e:
                print(e)

        # Description (optional)
        description = input("📝 Description (optional): ").strip()

        # Tags (optional)
        tags_input = input("🏷️ Tags (comma-separated, optional): ").strip()
        tags = (
            [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            if tags_input
            else []
        )

        # Append task
        tasks.append(
            {
                "name": name,
                "deadline": deadline,
                "description": description if description else None,
                "tags": tags if tags else None,
            }
        )

        # Continue?
        add_another = input("\n➕ Add another task? (y/n): ").strip().lower()
        if add_another != "y":
            break
    return tasks
