#!/usr/bin/python

import multiprocessing
import random
import time


def patient_shooter(patient_times, doctor_times, hospital_slots):
    i = 1
    while True:
        time.sleep(random.uniform(patient_times[0], patient_times[1]))
        multiprocessing.Process(target=patient_arrive, args=(hospital_slots, doctor_times, i)).start()
        i += 1


def patient_arrive(hospital_slots, doctor_times, i):
    print("--> Patient", i, "just arrived.", hospital_slots.get_value(), "free slots")

    hospital_slots.acquire()
    print("<-- Patient", i, "is getting attended.", hospital_slots.get_value(), "free slots.")
    time.sleep(random.uniform(doctor_times[0], doctor_times[1]))
    hospital_slots.release()
    print("<-- Patient", i, "leaving.", hospital_slots.get_value(), "free slots")



def main():
    patient_times = (1, 3)
    doctor_times = (5, 7)
    hospital_slots = multiprocessing.Semaphore(5)

    patient_shooter(patient_times, doctor_times, hospital_slots)


if __name__ == '__main__':
    main()
