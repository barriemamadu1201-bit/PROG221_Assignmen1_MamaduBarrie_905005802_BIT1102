import sys
from datetime import date, timedelta
from typing import Dict, Optional

# Tuples: fixed values that must never change at runtime.
AGE_GROUPS = ("0-11 months", "1-4 years", "5-14 years", "15-49 years", "50+ years")

# (vaccine name, doses required, days between doses)
VACCINE_SCHEDULES = (
    ("BCG", 1, 0),
    ("Polio", 4, 28),
    ("Measles", 2, 180),
    ("Pentavalent", 3, 28),
    ("COVID-19", 2, 28),
)

# CLASS 1: Vaccinesssssssss
class Vaccine:
    """Describes one vaccine and its dosing schedule."""

    def __init__(self, name, doses_required, interval_days):
        self.name = name
        self.doses_required = doses_required
        self.interval_days = interval_days

    #class method:
    @classmethod
    def from_schedule(cls, schedule):
        """Build a Vaccine from a (name, doses, interval) tuple."""
        name, doses, interval = schedule
        return cls(name, doses, interval)

    @classmethod
    def catalogue(cls):
        """Return a dictionary of every known vaccine, keyed by name."""
        return {s[0]: cls.from_schedule(s) for s in VACCINE_SCHEDULES}

    #instance method
    def display_info(self):
        gap = f"{self.interval_days} days apart" if self.doses_required > 1 else "single dose"
        print(f"  Vaccine: {self.name:<12} Doses: {self.doses_required}  ({gap})")


# CLASS 2: VaccinationRecord
class VaccinationRecord:
    """
    One anonymous vaccination record.
    DPG privacy: stores only a generated ID and an age GROUP - no name,
    address, phone number or exact date of birth.
    """

    _counter = 0          # class attribute: shared by all records

    def __init__(self, age_group, vaccine):
        if not VaccinationRecord.is_valid_age_group(age_group):
            raise ValueError(f"Invalid age group: {age_group}")
        VaccinationRecord._counter += 1
        self.record_id = VaccinationRecord.make_id()
        self.age_group = age_group
        self.vaccine = vaccine            # interaction: record HAS-A Vaccine
        self.doses_given: int = 0
        self.last_dose_date: Optional[date] = None

    #class methods
    @classmethod
    def make_id(cls):
        """Generate the next unique anonymous ID, e.g. VR-0001."""
        return f"VR-{cls._counter:04d}"

    @classmethod
    def total_records(cls):
        """Shows how many records have been created so far."""
        return cls._counter

    #static methods (need no object or class data)
    @staticmethod
    def is_valid_age_group(age_group):
        return age_group in AGE_GROUPS

    @staticmethod
    def parse_date(text):
        """Convert 'YYYY-MM-DD' to a date object (raises ValueError if bad)."""
        year, month, day = (int(p) for p in text.split("-"))
        return date(year, month, day)

    #instance methods
    def record_dose(self, dose_date: date) -> bool:
        """Register one more dose given on dose_date."""
        if self.is_complete():
            print(f"  {self.record_id}: course already complete - no dose added.")
            return False
        if self.last_dose_date is not None and dose_date < self.last_dose_date:
            print(f"  {self.record_id}: dose date cannot be before the last dose.")
            return False
        self.doses_given += 1
        self.last_dose_date = dose_date
        return True

    def is_complete(self):
        return self.doses_given >= self.vaccine.doses_required

    def next_due_date(self) -> Optional[date]:
        """Date the next dose is due, or None if complete / not started."""
        if self.is_complete() or self.last_dose_date is None:
            return None
        return self.last_dose_date + timedelta(days=self.vaccine.interval_days)

    def status(self, today):
        if self.is_complete():
            return "COMPLETE"
        if self.doses_given == 0:
            return "NOT STARTED"
        due = self.next_due_date()
        return "OVERDUE" if due is not None and due < today else "IN PROGRESS"

    def update_record(self, new_age_group):
        """Correct the age group (e.g. a child moves to the next band)."""
        if VaccinationRecord.is_valid_age_group(new_age_group):
            self.age_group = new_age_group
            return True
        print(f"  Invalid age group: {new_age_group}")
        return False

    def display_info(self, today: Optional[date] = None) -> None:
        today = today or date.today()
        due = self.next_due_date()
        print(f"  {self.record_id} | {self.age_group:<12} | {self.vaccine.name:<12} | "
              f"{self.doses_given}/{self.vaccine.doses_required} doses | "
              f"{str(due) if due else '-':<10} | {self.status(today)}")


# data structure (dict)
def add_record(store, record):
    """Add a record to the dictionary, using its unique ID as the key."""
    if record.record_id in store:
        print(f"  ID {record.record_id} already exists - not added.")
        return False
    store[record.record_id] = record
    print(f"  Added record {record.record_id}.")
    return True


def display_records(store: Dict[str, "VaccinationRecord"], today: Optional[date] = None) -> None:
    """Loop through the dictionary and print every record."""
    if not store:
        print("  (no records yet)")
        return
    print("  ID      | Age group    | Vaccine      | Progress  | Due        | Status")
    print("  " + "-" * 76)
    for record in store.values():
        record.display_info(today)

# CLASS 3: VaccinationTracker
class VaccinationTracker:
    """A health post's register. Holds records in a dict: {record_id: record}."""

    def __init__(self, post_name):
        self.post_name = post_name         # a facility name, not a person
        self.records: Dict[str, VaccinationRecord] = {}

    def register(self, age_group: str, vaccine_name: str) -> "VaccinationRecord":
        """Create and store a record. Raises ValueError for bad input."""
        vaccine = Vaccine.catalogue().get(vaccine_name)
        if vaccine is None:
            raise ValueError(f"Unknown vaccine: {vaccine_name}")
        record = VaccinationRecord(age_group, vaccine)
        add_record(self.records, record)
        return record

    def find(self, record_id):
        return self.records.get(record_id)

    def give_dose(self, record_id, dose_date):
        record = self.find(record_id)
        if record is None:
            print(f"  No record with ID {record_id}.")
            return False
        ok = record.record_dose(dose_date)
        if ok:
            print(f"  Dose {record.doses_given}/{record.vaccine.doses_required} "
                  f"recorded for {record_id} on {dose_date}.")
        return ok

    def overdue(self, today):
        """Return the IDs of records whose next dose is overdue."""
        return [rid for rid, r in self.records.items() if r.status(today) == "OVERDUE"]

    def summary(self, today):
        total = len(self.records)
        complete = sum(1 for r in self.records.values() if r.is_complete())
        print(f"  Health post : {self.post_name}")
        print(f"  Records     : {total}")
        print(f"  Complete    : {complete}")
        print(f"  Overdue     : {len(self.overdue(today))}  {self.overdue(today)}")

# DEMO and MENU
def demo() -> None:
    today = date(2026, 10, 18)
    print("=" * 60)
    print(" COMMUNITY VACCINATION TRACKER ")
    print("=" * 60)

    print("\n[1]Vaccines available")
    for vaccine in Vaccine.catalogue().values():
        vaccine.display_info()

    print("\n[2] Creating the tracker and registering anonymous records")
    tracker = VaccinationTracker("Freetown Community Health Post")
    r1 = tracker.register("0-11 months", "Pentavalent")
    r2 = tracker.register("1-4 years", "Measles")
    r3 = tracker.register("15-49 years", "COVID-19")
    r4 = tracker.register("0-11 months", "Polio")

    print("\n[3] Recording doses ")
    tracker.give_dose(r1.record_id, date(2026, 8, 1))
    tracker.give_dose(r1.record_id, date(2026, 8, 29))
    tracker.give_dose(r1.record_id, date(2026, 9, 26))
    tracker.give_dose(r2.record_id, date(2026, 3, 1))
    tracker.give_dose(r3.record_id, date(2026, 9, 10))
    tracker.give_dose(r3.record_id, date(2026, 10, 8))
    tracker.give_dose(r1.record_id, date(2026, 10, 10))     # already complete
    tracker.give_dose("VR-9999", today)                      # unknown ID

    print(f"\n[4] All records as of {today}")
    display_records(tracker.records, today)

    print("\n[5] Updating a record ")
    r4.update_record("1-4 years")
    r4.update_record("100 years")
    r4.display_info(today)

    print("\n[6] Static and class methods")
    print("  is_valid_age_group('5-14 years') :", VaccinationRecord.is_valid_age_group("5-14 years"))
    print("  parse_date('2026-10-18')         :", VaccinationRecord.parse_date("2026-10-18"))
    print("  Total records created            :", VaccinationRecord.total_records())

    print("\n[7] Summary report")
    tracker.summary(today)
    print("\nPrivacy check: no names, phone numbers or addresses were stored.")


def menu() -> None:
    tracker = VaccinationTracker("Community Health Post")
    while True:
        print("\n1 Register  2 Give dose  3 Show all  4 Summary  5 Quit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                for i, g in enumerate(AGE_GROUPS, 1):
                    print(f"  {i}. {g}")
                group = AGE_GROUPS[int(input("Age group number: ")) - 1]
                print("  Vaccines:", ", ".join(Vaccine.catalogue()))
                tracker.register(group, input("Vaccine name: ").strip())
            elif choice == "2":
                rid = input("Record ID: ").strip().upper()
                when = VaccinationRecord.parse_date(input("Date (YYYY-MM-DD): ").strip())
                tracker.give_dose(rid, when)
            elif choice == "3":
                display_records(tracker.records, date.today())
            elif choice == "4":
                tracker.summary(date.today())
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("  Please choose 1-5.")
        except (ValueError, IndexError):
            print("  Invalid input - please try again.")


if __name__ == "__main__":
    if "--menu" in sys.argv:
        demo()
    else:
        menu()