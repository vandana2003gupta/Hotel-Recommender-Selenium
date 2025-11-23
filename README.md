<img width="1919" height="1099" alt="Screenshot 2025-11-23 210340" src="https://github.com/user-attachments/assets/fccdfe18-4720-484f-b3a8-68dccb5624a9" />

<img width="1919" height="1140" alt="Screenshot 2025-11-23 210359" src="https://github.com/user-attachments/assets/2e464ef3-b430-46e6-9271-788864d6debd" />

<img width="1184" height="605" alt="image" src="https://github.com/user-attachments/assets/b565c3a1-64f7-4530-a3d4-aef9c2a59972" />

---

# Booking.com Selenium Automation

Automated hotel search, filtering, and data extraction from Booking.com using **Python + Selenium**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![ChromeDriver](https://img.shields.io/badge/ChromeDriver-Auto--Managed-orange?logo=googlechrome)
![License](https://img.shields.io/badge/License-MIT-purple)
![Status](https://img.shields.io/badge/Project-Active-success)


## Overview

This project provides a **fully automated hotel search bot** for Booking.com using Selenium.
It allows you to:

* Enter a destination
* Select check-in & check-out dates
* Choose number of adults
* Automatically search for hotels
* Apply filters (star rating, sort by price, etc.)
* Extract hotel name, price, and guest score
* Display results in a beautifully formatted table

The codebase follows a clean **package structure** with modular automation logic.

---

## Project Structure

```
Seleniumproj/
│── run.py
│── requirements.txt
│── README.md
│── booking/
│   ├── __init__.py
│   ├── booking.py
│   ├── filtration.py
│   └── report.py
```

---

## Features

| Feature                            | 
| ---------------------------------- |    
| Automated browser launch           |
| Destination + date selection       | 
| Adults picker                      | 
| Star-rating filters                | 
| Sort by lowest price               | 
| Scrape Price, Score, Hotel Name    | 
| Formatted table output             | 
| Works with 2025 Booking.com layout |

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/booking-automation.git
cd booking-automation
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **ChromeDriver is auto-managed by Selenium 4.10+**
> No manual driver download required.

---

## Usage

Run:

```bash
python run.py
```

You will be prompted:

```
Where do you want to go? Mumbai
Check-in date (YYYY-MM-DD): 2025-12-01
Check-out date (YYYY-MM-DD): 2025-12-05
Number of adults: 2
```

Example output:

```
╒════════════════════╤══════════╤════════╕
│ Hotel              │ Price    │ Score  │
╞════════════════════╪══════════╪════════╡
│ Trident Nariman    │ $158     │ 9.0    │
│ Taj Lands End      │ $184     │ 8.7    │
╘════════════════════╧══════════╧════════╛
```

---

## Customization

Modify filters in:

```
booking/filtration.py
```

Modify extraction logic in:

```
booking/report.py
```

Edit core browser actions in:

```
booking/booking.py
```

---

## Troubleshooting

### Currency popup not found

Not all regions show the currency button — script continues safely.

### NoSuchElement

Booking.com frequently changes HTML.
If this happens:

* Increase waiting time
* Re-run in non-headless mode
* Update CSS selectors in `booking.py`



<img width="1919" height="1060" alt="image" src="https://github.com/user-attachments/assets/fce00507-eb98-4d08-9bef-ced2b01bebfa" />
