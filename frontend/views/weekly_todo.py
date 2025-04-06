import requests
from datetime import timedelta, timezone, datetime
from zoneinfo import ZoneInfo 

# ====== Step 1: Set Up Your API Credentials ======

API_TOKEN = '13~47Y8UAZaYt32LhLHxNh9uDTZMHWRahEM3Ue7U3uL4v999QH97YFHyN44CDDA9cMa'
CANVAS_DOMAIN = 'https://usflearn.instructure.com'
TODO_ENDPOINT = f"{CANVAS_DOMAIN}/api/v1/users/self/todo"

# ====== Step 2: Set Up the Request Headers ======

headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# ====== Step 3: Call the Canvas To-Do API ======

print("Fetching your to-do list from Canvas...")
response = requests.get(TODO_ENDPOINT, headers=headers)

if response.status_code != 200:
    print("Error fetching tasks:", response.status_code, response.text)
    exit()

todos = response.json()

#print(todos[0])

# ====== Step 4: Filter for Weekly Tasks ======
# Eastern time zone
now = datetime.now(ZoneInfo("America/New_York"))
print("Current time:", now)
one_week_from_now = now + timedelta(days=7)

weekly_tasks = []

for item in todos:
    # Try to get the due date from the top-level; if not, check inside 'assignment'
    due_at_str = item.get('due_at')
    if not due_at_str:
        due_at_str = item.get('assignment', {}).get('due_at')

    if due_at_str:
        try:
            due_date = datetime.fromisoformat(due_at_str.replace("Z", "+00:00"))
        except Exception as e:
            print("Error parsing due date:", due_at_str, e)
            continue

        # Check if the task's due date is within the next week
        if now <= due_date <= one_week_from_now:
            # Get the task title. If not available at the top-level, try the 'assignment' object.
            title = item.get('title')
            if not title and 'assignment' in item:
                title = item['assignment'].get('name', 'No Title')
            # Get the course name from the 'assignment' object  which is called 'context_name'.
            course = item.get('context_name', 'Unknown Course')
            
            weekly_tasks.append({
                'title': title,
                'due_date': due_date,
                'context_name': course
            })

# ====== Step 5: Display the Weekly To-Do List ======

if weekly_tasks:
    print("\nYour Weekly To-Do List:")
    weekly_tasks.sort(key=lambda x: x['due_date'])
    for task in weekly_tasks:
        formatted_due = task['due_date'].strftime('%Y-%m-%d %H:%M')
        print(f"Course: {task['context_name']} | Task: {task['title']} | Due: {formatted_due}")
else:
    print("You have no tasks due in the next week!")

