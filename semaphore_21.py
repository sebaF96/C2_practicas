#!/usr/bin/python

import multiprocessing
import random
import time
import signal
import sys
import getopt


def read_options():
    patient_min, patient_max = (1, 3)
    doctor_min, doctor_max = (5, 7)
    hospital_rooms = 5

    # If no opt given in each case, it will use v1 default values.
    (opt, arg) = getopt.getopt(sys.argv[1:], 's:', ['p1=', 'p2=', 'd1=', 'd2='])

    for (option, argument) in opt:
        if option == '--p1' and int(argument) >= 0:
            patient_min = int(argument)
        elif option == '--p2' and int(argument) > 0:
            patient_max = int(argument)
        elif option == '--d1' and int(argument) > 0:
            doctor_min = int(argument)
        elif option == '--d2' and int(argument) >= 0:
            doctor_max = int(argument)
        elif option == '-s' and int(argument) > 0:
            hospital_rooms = int(argument)

    if patient_min >= patient_max:
        patient_max = patient_min + 1

    if doctor_min >= doctor_max:
        doctor_max = doctor_min + 2

    return (patient_min, patient_max), (doctor_min, doctor_max), hospital_rooms


def clean_end(s, f):
    sys.exit(0)


def patient_shooter(patient_times, doctor_times, hospital_slots):
    i = 1
    while True:
        time.sleep(random.uniform(patient_times[0], patient_times[1]))
        multiprocessing.Process(target=patient_arrive, args=(hospital_slots, doctor_times, i)).start()
        i += 1


def patient_arrive(hospital_slots, doctor_times, i):
    print("--> Patient", i, "just arrived.", hospital_slots.get_value(), "free slots")

    hospital_slots.acquire()
    print("[+] Patient", i, "is getting attended.", hospital_slots.get_value(), "free slots.")
    time.sleep(random.uniform(doctor_times[0], doctor_times[1]))
    hospital_slots.release()

    print("<-- Patient", i, "leaving.", hospital_slots.get_value(), "free slots")


def main():
    patient_times, doctor_times, rooms = read_options()
    hospital_slots = multiprocessing.Semaphore(rooms)

    patient_shooter(patient_times, doctor_times, hospital_slots)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, clean_end)
    try:
        main()
    except ValueError:
        print('Arguments must be possitive integers')
    except getopt.GetoptError as ge:
        print(ge)
