with open('tests/test_date_filter_profile_page.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 10: duplicate timedelta
# Line numbers are 0-indexed, so line 10 is index 10.
if len(lines) > 10 and lines[10].strip() == "from datetime import date, timedelta, timedelta":
    lines[10] = "from datetime import date, timedelta\n"

# Fix the import of database.db: we want to import the module as well as init_db and get_db.
# Find the line that imports from database.db
for i, line in enumerate(lines):
    if line.strip().startswith("from database.db import init_db, get_db"):
        # We'll change this line to: import database.db\nfrom database.db import init_db, get_db
        # But note: we might have already imported the module? We'll replace the line with two lines.
        lines[i] = "import database.db\n"
        lines.insert(i+1, "from database.db import init_db, get_db\n")
        break

# Fix the app fixture to also set database.db.DATABASE = ':memory:'
# Find the app fixture
for i, line in enumerate(lines):
    if line.strip() == "@pytest.fixture" and i+1 < len(lines) and lines[i+1].strip().startswith("def app():"):
        # We found the fixture. We'll insert after the config.update block and before the with flask_app.app_context() line.
        # We'll look for the line with "with flask_app.app_context():" starting from i+2.
        j = i+2  # start after the def line
        while j < len(lines) and not lines[j].strip().startswith("with flask_app.app_context():"):
            j += 1
        # Now j is at the line with "with flask_app.app_context():"
        # We want to insert before this line, with the same indentation as the function body (4 spaces).
        indent = "    "  # 4 spaces
        insert_lines = [
            "# Override the database module's DATABASE variable to use in-memory database",
            "import database.db",
            "database.db.DATABASE = ':memory:'"
        ]
        # Insert the lines in reverse order so that the first line ends up at the correct position.
        for k, insert_line in enumerate(reversed(insert_lines)):
            lines.insert(j, indent + insert_line + "\n")
        # We have inserted 3 lines, so we need to adjust j? We'll break and let the loop continue.
        break

# Write the file back
with open('tests/test_date_filter_profile_page.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
