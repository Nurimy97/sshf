# sshf — SSH Log Filter

A command-line tool to filter and display SSH logs (`auth.log`) with colored, structured output.

## Description

`sshf` parses your SSH log file and lets you filter entries by service type, keyword, or date. Results are displayed in a formatted table with color-coded rows so you can quickly spot failed logins, accepted connections, cron jobs, and sudo usage.

## Installation

**Requirements:**
- Python 3.6+
- [rich](https://github.com/Textualize/rich)

**Install dependencies:**
```bash
pip install rich
```

**Clone the repo:**
```bash
git clone https://github.com/Nurimy97/sshf.git
cd sshf
```

**Make it executable (optional):**
```bash
chmod +x sshf.py
```

## Usage

```
python sshf.py -f <logfile> [options]
```

| Flag | Long flag | Description |
|------|-----------|-------------|
| `-f` | `--file` | Path to the SSH log file (required) |
| `-l` | `--list` | Filter by service: `login`, `cron`, or `sudo` |
| `-s` | `--search` | Search for a keyword |
| `-d` | `--date` | Filter by date, e.g. `"Mar 6"` or `"Mar 6 12:45"` |

## Examples

Show all log entries:
```bash
python sshf.py -f /var/log/auth.log
```

Show only login attempts:
```bash
python sshf.py -f /var/log/auth.log -l login
```

Filter by date:
```bash
python sshf.py -f /var/log/auth.log -d "Mar 6"
```

Search for a specific IP:
```bash
python sshf.py -f /var/log/auth.log -s "192.168.1.10"
```

Combine filters:
```bash
python sshf.py -f /var/log/auth.log -l login -d "Mar 6" -s "Failed"
```

## Color Reference

| Color | Meaning |
|-------|---------|
| 🟢 Green | Accepted connection / successful login |
| 🔴 Red | Failed password / invalid user |
| 🟣 Magenta | Other sshd activity |
| 🟡 Yellow | Cron session |
| 🔵 Cyan | Sudo usage |
| ⚪ White | Other entries |
