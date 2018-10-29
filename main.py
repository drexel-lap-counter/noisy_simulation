#!/usr/bin/env python3
from threading import Thread
import time

from ActualRssiData import ActualRssiData
from Beacon import Beacon

class LpfExample:
    # The percent of the previous LPF value the filter should retain when
    # encountering a new RSSI reading.
    LPF_ALPHA = 0.8

    # How often in seconds to send out RSSI readings.
    RSSI_FREQ_SECS = 1

    DEVICE = 's7'
    RSSI_DATAFILE = 'rssi_readings/puck/air_to_air.xlsx'

    def __init__(self):
        print(f"Simulation of LPF filter (alpha={self.LPF_ALPHA}) against "
              f"regression for Puck air-to-air RSSI readings on '{self.DEVICE}'")

        print(f"Datafile: {self.RSSI_DATAFILE}\n"
              f"Device: {self.DEVICE}")

        self.beacon = Beacon(ActualRssiData(self.RSSI_DATAFILE, self.DEVICE))
        self.lpf_rssi = None

    def run(self):
        Thread(target=self.tick, daemon=True).start()

        while True:
            command = input("Move the beacon (f)arther or (c)loser: ")

            if command == 'f':
                self.beacon.move_farther()
            elif command == 'c':
                self.beacon.move_closer()

    def regression_puck_s7_a2a(self, rssi):
        # This is the regression pulled and rearranged from the graph of
        # distance vs. rssi for the air-to-air Puck measurements on the s7.
        return 66.03215 ** ((rssi - 78.6) / 8.57)

    def estimate_distance(self, rssi):
        # Just using the regression for the dataset to show a proof of concept.
        # The distances will likely be inaccurate.
        return self.regression_puck_s7_a2a(rssi)

    def tick(self):
        while True:
            print(self.beacon)
            raw_rssi_received = self.beacon.get_rssi()

            if not self.lpf_rssi:
                self.lpf_rssi = raw_rssi_received

            print(f"Raw RSSI received: {raw_rssi_received}")
            print(f"Previous LPF RSSI: {self.lpf_rssi}")

            self.lpf_rssi = (self.LPF_ALPHA * self.lpf_rssi +
                                  (1 - self.LPF_ALPHA) * raw_rssi_received)

            print(f"New LPF RSSI: {self.lpf_rssi}")
            print("Regression distance: "
                  f"{self.estimate_distance(self.lpf_rssi)} feet")

            print()
            time.sleep(self.RSSI_FREQ_SECS)



if __name__ == '__main__':
    LpfExample().run()

