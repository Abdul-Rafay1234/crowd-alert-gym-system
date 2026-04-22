import csv
import time
from datetime import datetime

# CONFIGURATION
MAX_CAPACITY = 150

# SEND WHATSAPP ALERT (DISABLED FOR NOW)
def send_whatsapp_alert(message_body):
    print(f"[WHATSAPP DISABLED] {message_body}")

# CALCULATE OCCUPANCY
def calculate_current_occupancy(filename):
    occupancy = 0

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) >= 3:
                    event = row[2].strip().lower()

                    if event == 'entry':
                        occupancy += 1
                    elif event == 'exit':
                        occupancy -= 1

        return max(0, occupancy)

    except FileNotFoundError:
        print("[ERROR] CSV file not found!")
        return 0

# CROWD LEVEL LOGIC
def crowding_levels(number):
    percentage = (number / MAX_CAPACITY) * 100

    if percentage < 45:
        return "Gym is Free"
    elif percentage < 75:
        return "Gym is Busy"
    elif percentage < 95:
        return "Gym is Crowded"
    else:
        return "Gym is Overcrowded"

# LOG ALERTS
def log_alert(message):
    with open("alerts_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# MAIN PROGRAM
filename = "gym_log.csv"
previous_status = None

print("System Started: Monitoring Gym Crowd...\n")

while True:
    occupancy = calculate_current_occupancy(filename)
    status = crowding_levels(occupancy)

    print(f"Occupancy: {occupancy} | Status: {status}")

    if status != previous_status and status in [
        "Gym is Free",
        "Gym is Crowded",
        "Gym is Overcrowded"
    ]:
        message = f"{status} | Current occupancy: {occupancy}"

        send_whatsapp_alert(message)
        log_alert(message)

        print("[INFO] Alert logged.")

    previous_status = status

    time.sleep(60)
