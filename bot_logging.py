import datetime


def log_break():
    print("\n")
    with open("logs/log.txt", "a") as logfile:
        logfile.write("\n")


def log(message):
    prefix = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S - ")
    message = prefix + message
    print(message)
    message = message + "\n"
    with open("logs/log.txt", "a") as logfile:
        logfile.write(message)

