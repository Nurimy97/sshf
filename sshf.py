#!/usr/bin/env python3
import argparse
from rich import print
from rich.panel import Panel
from rich.table import Table

# Output to file function
# Make it work only with keyword and date flags

###################
# Argument Parser # 
###################

parser = argparse.ArgumentParser(description="Filter your SSH Logs with style and comfort")
parser.add_argument("-f", "--file", required=True, dest="file", help="SSH log file to read")
parser.add_argument("-s", "--search", required=False, dest="keyword", help="Search for keyword")
parser.add_argument("-l", "--list", required=False, dest="list", help="List sshd logs ( login/cron/sudo)")
parser.add_argument("-d", "--date", required=False, dest="date", help="Filter by date (e.g: 'Apr 19' or 'Apr 19 12:45')")
args = parser.parse_args()

VALID_LISTS = ["login", "cron", "sudo"]
if args.list and args.list not in VALID_LISTS:
    print(Panel(f"[red]Invalid list type '{args.list}'. Choose from: {', '.join(VALID_LISTS)}[/red]", border_style="red"))
    exit(1)

###########
# Helpers #
###########

def parse_line(line):
    parts = line.strip().split()

    if len(parts) < 5:
        return None

    return {
        "date": f"{parts[0]} {parts[1]}",
        "time": parts[2],
        "host": parts[3],
        "service": parts[4].strip(":"),
        "message": " ".join(parts[5:])
    }

def render_table(rows, columns, title="Results", keyword=None):
    table = Table()

    for col in columns:
        table.add_column(col.capitalize())
    for row in rows:
        style = row.get("style", None)
        table.add_row(*(str(row.get(col, "")) for col in columns), style=style)
    if keyword:
        print(Panel(f"[green]{keyword}[/green]", title="[bold][ Search Term ][/bold]", border_style="green"))
    if rows:
        print(Panel(table, title="[bold][ Results ][/bold]", border_style="blue"))
    else:
        print(Panel("[red]0 matches[/red]", title=f"[bold][ {title} ][/bold]", border_style="red"))

############
# Filters  #
############

def filter_by_login(lines, keyword, date):
    results = []

    for line in lines:
        if "sshd" not in line:
            continue

        if keyword and keyword not in line:
            continue

        if date and date not in line:
            continue

        parsed = parse_line(line)
        if not parsed:
            continue

        msg = parsed["message"]

        if ("Accepted" in msg) or ("Connection from" in msg):
            parsed["style"] = "green" 
        elif ("Failed password" in msg) or ("Invalid user" in msg):
            parsed["style"] = "red"
        else:
            parsed["style"] = "magenta"
        
        results.append(parsed)

    return results


def filter_by_cron(lines, keyword, date):
    results = []

    for line in lines:
        if "cron:session" not in line:
            continue
        if keyword and keyword not in line:
            continue
        if date and date not in line:
            continue

        parsed = parse_line(line)
        if not parsed:
            continue
            
        parsed["style"] = "yellow"
        results.append(parsed)

    return results


def filter_by_sudo(lines, keyword, date):
    results = []

    for line in lines:
        if "sudo" not in line:
            continue
        if keyword and keyword not in line:
            continue
        if date and date not in line:
            continue

        parsed = parse_line(line)
        if not parsed:
            continue 
            
        parsed["style"] = "cyan"
        results.append(parsed)

    return results

def default(lines, keyword, date):
    results = []
    for line in lines:

        if keyword and keyword not in line:
            continue
        if date and date not in line:
            continue
        parsed = parse_line(line)
        if not parsed:
            continue 
            
        msg = parsed["message"]

        if "sshd" in line:
            if ("Accepted" in msg) or ("Connection from" in msg):
                parsed["style"] = "green"
            elif ("Failed password" in msg) or ("Invalid user" in msg):
                parsed["style"] = "red"
            else:
                parsed["style"] = "magenta"
        elif "cron:session" in line:
            parsed["style"] = "yellow"
        elif "sudo" in line:
            parsed["style"] = "cyan"
        else:
            parsed["style"] = "white"

        results.append(parsed)
        
    return results

########
# Main #
########

def open_file():
    with open(args.file, "r") as f:
        lines = [line.replace("  ", " ") for line in f.readlines()]

    if args.list == "login":
        data = filter_by_login(lines, args.keyword, args.date)
        render_table(data, ["date", "time", "host", "service", "message"], title="Login Logs", keyword=args.keyword)
    elif args.list == "cron":
        data = filter_by_cron(lines, args.keyword, args.date)
        render_table(data, ["date", "time", "host", "service", "message"], title="Cron Logs", keyword=args.keyword)
    elif args.list == "sudo":
        data = filter_by_sudo(lines, args.keyword, args.date)
        render_table(data, ["date", "time", "host", "service", "message"], title="Sudo Logs", keyword=args.keyword)
    else:
        data = default(lines, args.keyword, args.date)
        render_table(data, ["date", "time", "host", "service", "message"], title="All Logs", keyword=args.keyword)

open_file()

#########
# Tests #
#########




