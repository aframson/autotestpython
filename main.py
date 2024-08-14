import datetime

# Define the message to log
message = f"Script ran successfully at {datetime.datetime.now()}"

# Write the message to a log file
with open("python_log.txt", "a") as log_file:
    log_file.write(message + "\n")

print("Python script completed.")
