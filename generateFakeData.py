"""
Python script to simulate a fintech-like environment with a realistic hierarchy,
and populate a PostgreSQL database with users, employees, transactions,
foreign exchange rates, and support tickets.
"""

import random
import psycopg2
from faker import Faker
from uuid import uuid4
from datetime import datetime, timedelta

# ---------------- CONFIG ------------------
TOTAL_USERS = 100
CUSTOMER_RATIO = 10
STAFF_RATIO = 1
DB_CONFIG = {
    "host": "localhost",
    "dbname": "global_financial_services_db",
    "user": "postgres",
    "password": "admin1",
    "port": 5432
}

# Hierarchy structure (ordered from top to bottom)
HIERARCHY = [
    ("CEO", 1),
    ("CTO", 1),
    ("CFO", 1),
    ("Head of Compliance", 1),
    ("Head of Support", 1),
    ("Engineering Manager", 2),
    ("Finance Manager", 2),
    ("Compliance Officer", 3),
    ("Support Agent", 4),
    ("Software Engineer", 5),
    ("Finance Analyst", 5)
]

DEPARTMENTS = {
    "CEO": "Executive",
    "CTO": "IT",
    "CFO": "Finance",
    "Head of Compliance": "Compliance",
    "Head of Support": "Support",
    "Engineering Manager": "IT",
    "Finance Manager": "Finance",
    "Compliance Officer": "Compliance",
    "Support Agent": "Support",
    "Software Engineer": "IT",
    "Finance Analyst": "Finance"
}

fake = Faker()

# ---------------- DATABASE ------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Drop & Create fresh tables
cur.execute("""
DROP TABLE IF EXISTS Transactions, FXRates, SupportTickets, Employees, Users CASCADE;

CREATE TABLE Users (
    user_id UUID PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20),
    role VARCHAR(20),
    created_at TIMESTAMP
);

CREATE TABLE Employees (
    employee_id UUID PRIMARY KEY,
    user_id UUID REFERENCES Users(user_id),
    department VARCHAR(100),
    position VARCHAR(100),
    date_joined DATE
);

CREATE TABLE Transactions (
    transaction_id UUID PRIMARY KEY,
    user_id UUID REFERENCES Users(user_id),
    amount DECIMAL(12, 2),
    currency VARCHAR(5),
    description TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE FXRates (
    rate_id UUID PRIMARY KEY,
    from_currency VARCHAR(5),
    to_currency VARCHAR(5),
    rate DECIMAL(10, 4),
    timestamp TIMESTAMP
);

CREATE TABLE SupportTickets (
    ticket_id UUID PRIMARY KEY,
    user_id UUID REFERENCES Users(user_id),
    issue TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
);
""")
conn.commit()

# ---------------- DATA GENERATION ------------------
def generate_user(role):
    return {
        "user_id": uuid4(),
        "full_name": fake.name(),
        "email": fake.unique.email(),
        "phone_number": fake.phone_number(),
        "role": role,
        "created_at": fake.date_time_this_decade()
    }

def generate_employee(user_id, position):
    return {
        "employee_id": uuid4(),
        "user_id": user_id,
        "department": DEPARTMENTS[position],
        "position": position,
        "date_joined": fake.date_this_decade()
    }

# Split users
num_customers = int(TOTAL_USERS * (CUSTOMER_RATIO / (CUSTOMER_RATIO + STAFF_RATIO)))
num_staff = TOTAL_USERS - num_customers

users = []
staff_records = []

# Generate customers
for _ in range(num_customers):
    users.append(generate_user("customer"))

# Generate staff by hierarchy
staff_count = 0
for position, count in HIERARCHY:
    for _ in range(count):
        if staff_count >= num_staff:
            break
        staff_user = generate_user("staff")
        users.append(staff_user)
        staff_records.append(generate_employee(staff_user["user_id"], position))
        staff_count += 1

# ---------------- INSERT USERS & EMPLOYEES ------------------
for u in users:
    cur.execute("""
    INSERT INTO Users (user_id, full_name, email, phone_number, role, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (str(u["user_id"]), u["full_name"], u["email"], u["phone_number"], u["role"], u["created_at"]))

for e in staff_records:
    cur.execute("""
    INSERT INTO Employees (employee_id, user_id, department, position, date_joined)
    VALUES (%s, %s, %s, %s, %s)
    """, (str(e["employee_id"]), str(e["user_id"]), e["department"], e["position"], e["date_joined"]))

conn.commit()

# ---------------- INSERT TRANSACTIONS ------------------
currencies = ["USD", "NGN", "EUR", "GBP"]

for u in users:
    if u["role"] == "customer":
        for _ in range(random.randint(2, 10)):
            cur.execute("""
            INSERT INTO Transactions (transaction_id, user_id, amount, currency, description, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid4()), str(u["user_id"]),
                round(random.uniform(100, 10000), 2),
                random.choice(currencies),
                fake.sentence(),
                fake.date_time_this_year()
            ))

# ---------------- INSERT FX RATES ------------------
for _ in range(20):
    from_curr, to_curr = random.sample(currencies, 2)
    cur.execute("""
    INSERT INTO FXRates (rate_id, from_currency, to_currency, rate, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        str(uuid4()), from_curr, to_curr,
        round(random.uniform(0.5, 1500), 4),
        datetime.now() - timedelta(days=random.randint(0, 30))
    ))

# ---------------- INSERT SUPPORT TICKETS ------------------
statuses = ["open", "in progress", "resolved"]
for u in users:
    if u["role"] == "customer" and random.random() < 0.3:
        created = fake.date_time_this_year()
        resolved = created + timedelta(days=random.randint(1, 5)) if random.random() < 0.7 else None
        cur.execute("""
        INSERT INTO SupportTickets (ticket_id, user_id, issue, status, created_at, resolved_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            str(uuid4()), str(u["user_id"]),
            fake.sentence(), random.choice(statuses),
            created, resolved
        ))

conn.commit()
cur.close()
conn.close()
print("Database populated with users, employees, transactions, FX rates, and tickets.")
