#!/usr/bin/env python3

from ActualRssiData import ActualRssiData


class Beacon:
    MOVE_SIZE_FEET = 12

    def __init__(self, actual_rssi_data: ActualRssiData):
        self.distance_from_receiver = 0
        self.actual_rssi_data = actual_rssi_data

        self.max_distance = self.actual_rssi_data.get_number_distances() - 1
        self.max_distance *= self.MOVE_SIZE_FEET

    def __str__(self):
        return f"Beacon, {self.distance_from_receiver} feet away"

    def get_rssi(self):
        step = self.distance_from_receiver // self.MOVE_SIZE_FEET
        return self.actual_rssi_data.get_random_rssi_at_step(step)

    def move_farther(self):
        if self.distance_from_receiver >= self.max_distance:
            print(f"Can't simulate distances farther than {self.max_distance} "
                  "feet away from the receiver.")
        else:
            self.distance_from_receiver += self.MOVE_SIZE_FEET

    def move_closer(self):
        if self.distance_from_receiver == 0:
            print("Can't simulate distances closer than 0 away from the "
                  "receiver.")
        else:
            self.distance_from_receiver -= self.MOVE_SIZE_FEET


if __name__ == '__main__':
    RSSI_DATAFILE = 'rssi_readings/puck/air_to_air.xlsx'
    DEVICE = 's7'

    print(f"Datafile: {RSSI_DATAFILE}\n"
          f"Device: {DEVICE}")

    actual_rssi_data = ActualRssiData(RSSI_DATAFILE, DEVICE)
    beacon = Beacon(actual_rssi_data)

    while True:
        print(beacon)
        print(f"RSSI: {beacon.get_rssi()}\n")

        command = input("Move the beacon (f)arther or (c)loser: ")

        if command == 'f':
            beacon.move_farther()
        elif command == 'c':
            beacon.move_closer()
