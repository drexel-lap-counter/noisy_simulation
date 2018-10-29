#!/usr/bin/env python3

import numpy as np
import pandas as pd


class ActualRssiData:
    def __init__(self, rssi_data_filename, sheet):
        self.observations = pd.read_excel(rssi_data_filename, sheet_name=sheet)
        self.means = self.observations.mean(1)
        self.standard_deviations = self.observations.std(1)
        self.num_distances = self.observations.shape[0]

    def get_random_rssi_at_step(self, step):
        return self.get_several_random_rssi_at_step(step, None)

    def get_several_random_rssi_at_step(self, step, num_values):
        assert(0 <= step < self.num_distances)
        mean = self.means.iloc[step]
        std = self.standard_deviations.iloc[step]
        return np.round(np.random.normal(mean, std, num_values))

    def get_number_distances(self):
        return self.num_distances


if __name__ == '__main__':
    RSSI_DATAFILE = 'rssi_readings/puck/air_to_air.xlsx'
    DEVICE = 'moto'

    print(f"Datafile: {RSSI_DATAFILE}\n"
          f"Device: {DEVICE}")

    actual_rssi_data = ActualRssiData(RSSI_DATAFILE, DEVICE)

    STEP_SIZE_FEET = 12
    EXAMPLE_STEP = 3
    NUM_SIMULATED_READINGS = 100

    r = actual_rssi_data.get_several_random_rssi_at_step(EXAMPLE_STEP,
                                                         NUM_SIMULATED_READINGS)

    print(f"Here are {NUM_SIMULATED_READINGS} simulated readings at "
          f"{STEP_SIZE_FEET * EXAMPLE_STEP} feet away from device '{DEVICE}':")

    print(r)
