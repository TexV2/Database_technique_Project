def method_picker(method, cur):
    conversion = {
        "infrastructure_id": "the ID",
        "type": "infrastructure type",
        "location": "the location",
        "install_date": "the install date",
        "last_inspection": "its last inspection",
        "state": "its current state"
    }
    data = input(f"Enter {conversion[method]}: ").lower().strip()
    if method == "infrastructure_id":
        try:
            data = int(data)
        except ValueError:
            return -1, data
    else:
        data = f"'{data}'"

    found_rows = check_rows(method, data, cur)
    if found_rows:
        return 1, data
    return 0, data


def check_rows(method, data, cur):
    cur.execute(f"SELECT 1 FROM Infrastructure WHERE {method} = {data} LIMIT 1")
    found_rows = cur.fetchone() is not None
    if found_rows:
        return True
    return False