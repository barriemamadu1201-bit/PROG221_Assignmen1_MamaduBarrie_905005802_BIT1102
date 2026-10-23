# COMMUNITY VACCINE TRACKER 

A privacy-first, object-oriented Python program that helps a community health post in Sierra Leone register vaccinations, record doses, and spot children and adults who have missed their next dose, **without storing any personal information**.

 

## Table of Contents

1. [Overview](#1-overview)

2. [Problem Statement](#2-problem-statement)

3. [Digital Public Good (DPG) Alignment](#3-digital-public-good-dpg-alignment)

4. [Features](#4-features)

5. [Requirements](#5-requirements)

6. [Installation and Running](#6-installation-and-running)

7. [Usage Guide](#7-usage-guide)

8. [Sample Output and Screenshots](#8-sample-output-and-screenshots)

9. [System Design](#9-system-design)

10. [OOP Concepts Demonstrated](#10-oop-concepts-demonstrated)

11. [Class and Function Reference](#11-class-and-function-reference)

12. [Vaccine Schedules](#12-vaccine-schedules)

13. [Status Logic](#13-status-logic)

14. [Validation and Error Handling](#14-validation-and-error-handling)

15. [Project Structure](#15-project-structure)

16. [Limitations and Future Improvements](#16-limitations-and-future-improvements)

17. [Contributing](#17-contributing)

18. [Licence](#18-licence)

19. [Author](#19-author)

 
---


## 1. Overview

The Community Vaccination Tracker is a command-line application that models the register of a small community health post. Each vaccination is stored as an **anonymous record** containing only:

- a generated record ID (e.g. `VR-0001`)

- an age **group** (not an exact age or date of birth)

- the vaccine being given

- the number of doses received so far

- the date of the last dose

 

From this, the program automatically calculates when the next dose is due and whether a record is **COMPLETE**, **IN PROGRESS**, **NOT STARTED** or **OVERDUE**. A summary report gives the health worker a quick picture of coverage and follow-up needs.

 

The program runs in two modes:

 

| Mode | Command | Purpose |

|------|---------|---------|

| **Demo** (default) | `python vaccination_tracker.py` | Runs a scripted walk-through showing every feature |

| **Interactive menu** | `python vaccination_tracker.py --menu` | Lets a user register records and give doses by typing |

 

---

 

## 2. Problem Statement

 

In many communities, vaccination follow-up depends on paper registers. This causes several problems:

 

- Children and adults miss follow-up doses because nobody notices a due date has passed.

- Multi-dose vaccines (Polio, Pentavalent, Measles, COVID-19) have different gaps between doses that are hard to track by hand.

- Digital records raise privacy concerns when they contain names, phone numbers and addresses.

 

This project shows how a simple, offline, privacy-respecting tool can track dose schedules and highlight **overdue** cases so health workers can prioritise follow-up.

 

---

 

## 3. Digital Public Good (DPG) Alignment

 

This project is designed around the principles of a Digital Public Good, with a focus on **SDG 3: Good Health and Well-being**.

 

| DPG principle | How this project meets it |

|---------------|---------------------------|

| **Privacy and do no harm** | No names, addresses, phone numbers or exact dates of birth are collected. Records use a generated ID and an age *group* only. The health post is identified by facility name, not by a person. |

| **Open source** | The full source code is open and readable, so health programmes can inspect, adapt and reuse it. |

| **Low barrier to use** | Pure Python, **no external libraries**, runs offline on any basic computer. No internet or database server needed. |

| **Platform independence** | Works on Windows, macOS and Linux with any Python 3.8+ installation. |

| **Clear documentation** | Docstrings in the code and this README explain how the system works. |

| **Adaptable** | Vaccine schedules and age groups are defined in two constants at the top of the file and can be changed without touching the logic. |

 

> **Privacy check:** the demo ends by confirming that no names, phone numbers or addresses were stored.

 

---

 

## 4. Features

 

- Register an anonymous vaccination record for an age group and vaccine

- Auto-generate unique, sequential record IDs (`VR-0001`, `VR-0002`, …)

- Record doses with a date, and block invalid entries (see [section 14](#14-validation-and-error-handling))

- Calculate the **next due date** from the vaccine's dose interval

- Classify each record as `COMPLETE`, `IN PROGRESS`, `NOT STARTED` or `OVERDUE`

- Update a record's age group (e.g. when a child moves into the next age band)

- Display all records in a formatted table

- Produce a summary: total records, completed courses, overdue records and their IDs

- Built-in catalogue of five vaccines with their schedules

 

---

 

## 5. Requirements

 

- **Python 3.8 or newer**

- No third-party packages (uses only the standard library: `sys`, `datetime`, `typing`)

Check your version:

```bash

python --version

```

---

 

## 6. Installation and Running

 

### Get the code

 

```bash

git clone https://github.com/barriemamadu1201-bit/<repository-name>.git

cd <repository-name>

```

 

### Run the demo

 

```bash

python vaccination_tracker.py

```

### Run the interactive menu

 

```bash

python vaccination_tracker.py --menu

```

> On some systems use `python3` instead of `python`.

> If your file has a different name, replace `vaccination_tracker.py` with that name.

 

---

 

## 7. Usage Guide

 

### 7.1 Demo mode

 

Running without arguments executes `demo()`, which walks through seven steps:

 

| Step | What it shows |

|------|---------------|

| 1 | Lists all available vaccines and their schedules |

| 2 | Creates a tracker and registers four anonymous records |

| 3 | Records doses, including two deliberate errors (course already complete, unknown ID) |

| 4 | Prints all records with progress, due date and status |

| 5 | Updates a record's age group, including one invalid update |

| 6 | Demonstrates static and class methods |

| 7 | Prints the summary report and privacy confirmation |

 

The demo uses a fixed date (**18 October 2026**) so the output is the same every time.

 

### 7.2 Interactive menu mode

 

```

1 Register  2 Give dose  3 Show all  4 Summary  5 Quit

Choose:

```

 

| Option | Action | What you enter |

|--------|--------|----------------|

| **1 Register** | Creates a new anonymous record | Age group number (1–5), then vaccine name (e.g. `Polio`) |

| **2 Give dose** | Records a dose for an existing record | Record ID (e.g. `VR-0001`, case-insensitive) and date in `YYYY-MM-DD` format |

| **3 Show all** | Displays every record as a table | Nothing |

| **4 Summary** | Shows totals, completed and overdue counts | Nothing |

| **5 Quit** | Exits the program | Nothing |

 

#### Example session

 

```

Choose: 1

  1. 0-11 months

  2. 1-4 years

  3. 5-14 years

  4. 15-49 years

  5. 50+ years

Age group number: 1

  Vaccines: BCG, Polio, Measles, Pentavalent, COVID-19

Vaccine name: Pentavalent

  Added record VR-0001.

 

Choose: 2

Record ID: vr-0001

Date (YYYY-MM-DD): 2026-10-01

  Dose 1/3 recorded for VR-0001 on 2026-10-01.

```

 

> **Note:** vaccine names are case-sensitive in the menu. Type them exactly as shown (e.g. `COVID-19`, `Pentavalent`).

> **Note:** records are held in memory only. They are cleared when the program closes.

 

---

 

## 8. Sample Output and Screenshots

 

Output of the demo (`python vaccination_tracker.py`):

 

```

============================================================

 COMMUNITY VACCINATION TRACKER

============================================================

 

[1]Vaccines available

  Vaccine: BCG          Doses: 1  (single dose)

  Vaccine: Polio        Doses: 4  (28 days apart)

  Vaccine: Measles      Doses: 2  (180 days apart)

  Vaccine: Pentavalent  Doses: 3  (28 days apart)

  Vaccine: COVID-19     Doses: 2  (28 days apart)

 

[2] Creating the tracker and registering anonymous records

  Added record VR-0001.

  Added record VR-0002.

  Added record VR-0003.

  Added record VR-0004.

 

[3] Recording doses

  Dose 1/3 recorded for VR-0001 on 2026-08-01.

  Dose 2/3 recorded for VR-0001 on 2026-08-29.

  Dose 3/3 recorded for VR-0001 on 2026-09-26.

  Dose 1/2 recorded for VR-0002 on 2026-03-01.

  Dose 1/2 recorded for VR-0003 on 2026-09-10.

  Dose 2/2 recorded for VR-0003 on 2026-10-08.

  VR-0001: course already complete - no dose added.

  No record with ID VR-9999.

 

[4] All records as of 2026-10-18

  ID      | Age group    | Vaccine      | Progress  | Due        | Status

  ----------------------------------------------------------------------------

  VR-0001 | 0-11 months  | Pentavalent  | 3/3 doses | -          | COMPLETE

  VR-0002 | 1-4 years    | Measles      | 1/2 doses | 2026-08-28 | OVERDUE

  VR-0003 | 15-49 years  | COVID-19     | 2/2 doses | -          | COMPLETE

  VR-0004 | 0-11 months  | Polio        | 0/4 doses | -          | NOT STARTED

 

[5] Updating a record

  Invalid age group: 100 years

  VR-0004 | 1-4 years    | Polio        | 0/4 doses | -          | NOT STARTED

 

[6] Static and class methods

  is_valid_age_group('5-14 years') : True

  parse_date('2026-10-18')         : 2026-10-18

  Total records created            : 4

 

[7] Summary report

  Health post : Freetown Community Health Post

  Records     : 4

  Complete    : 2

  Overdue     : 1  ['VR-0002']

 

Privacy check: no names, phone numbers or addresses were stored.

```

 

### Screenshots

 

Screenshots of the program running (demo and menu mode) are in the [`Screenshot`](Screenshot/) folder.

 

### Reading the output

 

- **VR-0001** finished all 3 Pentavalent doses, so it is `COMPLETE` and has no due date.

- **VR-0002** had its first Measles dose on 1 March 2026. The second was due 180 days later (28 August 2026). With a report date of 18 October 2026, it is `OVERDUE`.

- **VR-0004** is registered but has no doses yet, so it is `NOT STARTED`.

- The attempt to add a dose to the completed VR-0001 and to the non-existent `VR-9999` were both rejected with a clear message.

 

---

 

## 9. System Design

 

### 9.1 Class overview

 

```

┌──────────────────────┐        ┌────────────────────────────────┐

│       Vaccine        │        │       VaccinationRecord        │

├──────────────────────┤        ├────────────────────────────────┤

│ name                 │◄───────│ record_id                      │

│ doses_required       │ HAS-A  │ age_group                      │

│ interval_days        │        │ vaccine  (a Vaccine object)    │

├──────────────────────┤        │ doses_given                    │

│ from_schedule()  [C] │        │ last_dose_date                 │

│ catalogue()      [C] │        │ _counter  (class attribute)    │

│ display_info()       │        ├────────────────────────────────┤

└──────────────────────┘        │ make_id() / total_records() [C]│

          ▲                     │ is_valid_age_group()  [S]      │

          │ uses                │ parse_date()          [S]      │

          │                     │ record_dose()                  │

┌─────────┴────────────┐        │ is_complete()                  │

│  VaccinationTracker  │ HAS-MANY│ next_due_date()               │

├──────────────────────┤───────►│ status()                       │

│ post_name            │        │ update_record()                │

│ records  {id: record}│        │ display_info()                 │

├──────────────────────┤        └────────────────────────────────┘

│ register()           │

│ find()               │         [C] = class method

│ give_dose()          │         [S] = static method

│ overdue()            │

│ summary()            │

└──────────────────────┘

```

 

### 9.2 Relationships

 

- **`VaccinationRecord` HAS-A `Vaccine`**: each record holds a reference to the vaccine it tracks (composition/association).

- **`VaccinationTracker` HAS-MANY `VaccinationRecord`**: the tracker stores records in a dictionary keyed by record ID.

- **`VaccinationTracker` USES `Vaccine`**: it looks up vaccines from `Vaccine.catalogue()` when registering.

 

### 9.3 Data flow

 

```

Health worker

     │

     ▼

 Menu / Demo ──► VaccinationTracker.register(age_group, vaccine_name)

                        │

                        ├─► Vaccine.catalogue()  → finds the Vaccine

                        ├─► VaccinationRecord()  → validates age group, makes ID

                        └─► add_record()         → stores in dictionary

 

 Menu / Demo ──► VaccinationTracker.give_dose(record_id, date)

                        │

                        ├─► find(record_id)

                        └─► record_dose(date)    → checks complete / date order

                                                 → updates doses and last date

 

 Menu / Demo ──► display_records() / summary()

                        └─► status(today), next_due_date()

```

 

---

 

## 10. OOP Concepts Demonstrated

 

| Concept | Where it appears in the code |

|---------|------------------------------|

| **Classes and objects** | `Vaccine`, `VaccinationRecord`, `VaccinationTracker` |

| **Constructors (`__init__`)** | All three classes initialise their own attributes |

| **Instance attributes** | `name`, `doses_required`, `record_id`, `doses_given`, `records`, etc. |

| **Class attribute** | `VaccinationRecord._counter`, shared by every record to generate unique IDs |

| **Instance methods** | `record_dose()`, `is_complete()`, `next_due_date()`, `status()`, `display_info()`, `give_dose()`, `summary()` |

| **Class methods (`@classmethod`)** | `Vaccine.from_schedule()`, `Vaccine.catalogue()`, `VaccinationRecord.make_id()`, `VaccinationRecord.total_records()` |

| **Static methods (`@staticmethod`)** | `VaccinationRecord.is_valid_age_group()`, `VaccinationRecord.parse_date()` |

| **Object interaction / composition** | A record *has a* vaccine; a tracker *has many* records |

| **Encapsulation** | Each class manages its own data and rules (e.g. a record decides if it is complete) |

| **Immutable data (tuples)** | `AGE_GROUPS` and `VACCINE_SCHEDULES` are fixed and cannot change at runtime |

| **Dictionary data structure** | `records` maps `record_id` → `VaccinationRecord` for fast lookup |

| **Loops and conditionals** | Menu loop, record display loop, status logic |

| **Exception handling** | `try/except (ValueError, IndexError)` in the menu; `raise ValueError` for bad input |

| **Type hints** | `Optional[date]`, `Dict[str, VaccinationRecord]`, `-> bool`, `-> None` |

| **Docstrings** | Every class and most methods are documented |

 

---

 

## 11. Class and Function Reference

 

### Constants

 

| Name | Type | Description |

|------|------|-------------|

| `AGE_GROUPS` | tuple | The five valid age bands: `0-11 months`, `1-4 years`, `5-14 years`, `15-49 years`, `50+ years` |

| `VACCINE_SCHEDULES` | tuple of tuples | `(name, doses required, days between doses)` for each vaccine |

 

### `class Vaccine`

 

Describes one vaccine and its dosing schedule.

 

| Member | Type | Description |

|--------|------|-------------|

| `__init__(name, doses_required, interval_days)` | constructor | Creates a vaccine |

| `from_schedule(schedule)` | class method | Builds a `Vaccine` from a `(name, doses, interval)` tuple |

| `catalogue()` | class method | Returns a dict of all known vaccines keyed by name |

| `display_info()` | instance method | Prints the vaccine name, dose count and gap between doses |

 

### `class VaccinationRecord`

 

One anonymous vaccination record. Stores only an ID and an age group, with no personal details.

 

| Member | Type | Description |

|--------|------|-------------|

| `_counter` | class attribute | Total records created; used to build IDs |

| `__init__(age_group, vaccine)` | constructor | Validates the age group (raises `ValueError` if invalid), assigns an ID, sets `doses_given = 0` and `last_dose_date = None` |

| `make_id()` | class method | Returns the next ID in the form `VR-0001` |

| `total_records()` | class method | Returns how many records have been created |

| `is_valid_age_group(age_group)` | static method | `True` if the group is in `AGE_GROUPS` |

| `parse_date(text)` | static method | Converts `'YYYY-MM-DD'` to a `date` (raises `ValueError` if malformed) |

| `record_dose(dose_date)` | instance method | Adds one dose. Returns `False` if the course is complete or the date is earlier than the last dose |

| `is_complete()` | instance method | `True` when `doses_given >= doses_required` |

| `next_due_date()` | instance method | `last_dose_date + interval_days`, or `None` if complete or not started |

| `status(today)` | instance method | Returns `COMPLETE`, `NOT STARTED`, `OVERDUE` or `IN PROGRESS` |

| `update_record(new_age_group)` | instance method | Changes the age group if valid; returns `True`/`False` |

| `display_info(today=None)` | instance method | Prints one formatted table row (defaults to today's date) |

 

### `class VaccinationTracker`

 

A health post's register. Holds records in a dictionary `{record_id: record}`.

 

| Member | Description |

|--------|-------------|

| `__init__(post_name)` | Creates an empty register for a named health post |

| `register(age_group, vaccine_name)` | Creates and stores a record. Raises `ValueError` for an unknown vaccine or invalid age group |

| `find(record_id)` | Returns the record or `None` |

| `give_dose(record_id, dose_date)` | Records a dose and prints confirmation; returns `True`/`False` |

| `overdue(today)` | Returns a list of IDs whose next dose is overdue |

| `summary(today)` | Prints post name, total records, completed count, and overdue count with IDs |

 

### Module-level functions

 

| Function | Description |

|----------|-------------|

| `add_record(store, record)` | Adds a record to a dictionary using its ID as the key; refuses duplicates |

| `display_records(store, today=None)` | Loops through the dictionary and prints a formatted table |

| `demo()` | Scripted walk-through of all features with a fixed date |

| `menu()` | Interactive text menu for registering records and giving doses |

 

---

 

## 12. Vaccine Schedules

| Vaccine | Doses required | Days between doses |

|---------|:--------------:|:------------------:|

| BCG | 1 | – (single dose) |

| Polio | 4 | 28 |

| Measles | 2 | 180 |

| Pentavalent | 3 | 28 |

| COVID-19 | 2 | 28 |

 

> These values are **sample schedules for learning purposes**. They are not official medical guidance. Real programmes must follow the schedule set by the Ministry of Health and Sanitation.

 

To add or change a vaccine, edit `VACCINE_SCHEDULES` at the top of the file:

 

```python

VACCINE_SCHEDULES = (

    ("BCG", 1, 0),

    ("Polio", 4, 28),

    # add a new one: (name, doses required, days between doses)

    ("Yellow Fever", 1, 0),

)

```

 

---

 

## 13. Status Logic

The `status(today)` method decides a record's state in this order:

```

Is the course complete?             ──► COMPLETE

Have zero doses been given?         ──► NOT STARTED

Is the next due date before today?  ──► OVERDUE

Otherwise                           ──► IN PROGRESS

```

 

**Worked example (Measles, 2 doses, 180 days apart):**

 

- First dose: 1 March 2026

- Next due: 1 March 2026 + 180 days = **28 August 2026**

- Checked on 18 October 2026 → due date has passed → **OVERDUE**

 

A record is **IN PROGRESS** when at least one dose has been given but the next dose is not yet late. A record is **not** overdue on the due date itself, only after it.

 

---

 

## 14. Validation and Error Handling

 

| Situation | What the program does |

|-----------|-----------------------|

| Invalid age group when creating a record | Raises `ValueError("Invalid age group: …")` |

| Unknown vaccine name when registering | Raises `ValueError("Unknown vaccine: …")` |

| Dose given to an already completed course | Prints a message; no dose added; returns `False` |

| Dose date earlier than the last dose | Prints a message; no dose added; returns `False` |

| Dose for a record ID that does not exist | Prints `No record with ID …`; returns `False` |

| Invalid age group in `update_record()` | Prints a message; record unchanged; returns `False` |

| Duplicate record ID in `add_record()` | Refuses to add; returns `False` |

| Bad date text, bad number or bad age group choice in the menu | Caught by `try/except`; prints `Invalid input - please try again.` and returns to the menu |

| Menu choice outside 1–5 | Prints `Please choose 1-5.` |

 

---

 

## 15. Project Structure

 

```

repository-name/

├── vaccination_tracker.py   # Full program (classes, demo and menu)

├── Screenshot/              # Screenshots of the program running

├── README.md                # Project documentation (this file)

└── LICENSE                  # MIT Licence

```

 

---

 

## 16. Limitations and Future Improvements

 

### Current limitations

 

- **No saving:** records exist only while the program runs.

- **Command line only:** no graphical interface.

- **Simplified schedules:** every dose after the first uses the same fixed gap, with no minimum age rules.

- **Menu vaccine names are case-sensitive.**

- **Menu uses today's date:** overdue status in menu mode depends on the computer's clock.

- **Dates in the future** are not rejected when recording a dose.

- **Age-group updates are manual:** the program does not move a person to the next band automatically.

 

### Possible improvements

- Save and load records using a JSON or CSV file (or SQLite)

- Export overdue lists for outreach teams

- Add a simple GUI (Tkinter) or a web interface (Flask)

- Reject future dose dates and make vaccine lookup case-insensitive

- Add SMS or community-worker reminders for overdue records (with consent and privacy safeguards)

- Support multiple health posts and district-level reports

- Add unit tests with `unittest` or `pytest`

- Offer local-language interfaces (e.g. Krio)

 

---

 

## 17. Contributing

Contributions are welcome. To suggest an improvement:

1. Fork the repository

2. Create a branch: `git checkout -b feature/your-feature`

3. Commit your changes with a clear message

4. Push and open a Pull Request

 

**Privacy rule for all contributions:** do not add fields that store names, phone numbers, addresses, exact birth dates or any other personally identifiable information.

 

## 18. Licence

This project is licensed under the **MIT Licence**. See the [LICENSE](LICENSE) file for the full text.

```

MIT License

Copyright (c) 2026 Mamadu Barrie

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

 

The above copyright notice and this permission notice shall be included in all

 

