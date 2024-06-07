import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
import csv


def newplot():
    fig, ax = plt.subplots(1)

    ax.set_ylabel('Rotational Frequency')
    ax.set_xlabel('Time')
    ax.grid(axis='both', which='minor', linestyle='--', linewidth=0.5, color='gainsboro')
    ax.grid(axis='both', which='major')
    ax.minorticks_on()
    plt.title('Bezborodov', loc='right', color='grey')
    plt.xlim(right=2.5)
    return fig, ax


def read_datalog(fname, setpoint_column=2):
    '''
    Average aggregate step responses from datalogs.
    '''

    with open(f'datalogs/{fname}.csv') as csvfile:
        recording = False # Do not begin taking data until first sample.
        prev_setpoint = None # Store setpoint to detect start of a step.
        d = [] # Sample datum.
        D = [] # Sample data.

        reader = csv.reader(csvfile)
        next(reader, None) # Skip header row.
        for row in reader:
            setpoint = int(row[setpoint_column])

            # Check if start of a step input.
            if prev_setpoint is not None and setpoint > prev_setpoint:
                recording = True
                if d: D.append(d) # If datum is not empty, append it to data.
                d = [] # Clear datum for next sample.

            prev_setpoint = setpoint

            if recording: d.append(row)

        D = np.array(D).astype(float)
        D = np.swapaxes(D, 1, 2)
        Dm = np.mean(D, axis=0)
        return D, Dm


def datalog_step(fname, title):
    samples, means = read_datalog(fname)
    fig, ax = newplot()

    for sample in samples:
        ax.plot(sample[1], sample[3], linestyle='--', linewidth=0.25)

    ax.plot(means[1], means[3], linestyle='-', linewidth=1, color='black')

    plt.title(title)
    plt.savefig(f'plots/{fname}_step.pdf',
                bbox_inches='tight', pad_inches=0)
    plt.close()

    return means[1], means[3]


def datalog_actuating(fname, title):
    samples, means = read_datalog(fname)
    fig, ax = newplot()

    ax.plot(means[1], means[3], linestyle='-', linewidth=1, color='black')

    ax.plot(means[1], np.sum(means[4:6], axis=0), linestyle='-', linewidth=1, color='blue')
    ax.plot(means[1], means[4], linestyle='-', linewidth=1, color='green')
    ax.plot(means[1], means[5], linestyle='-', linewidth=1, color='red')
    ax.plot(means[1], means[6], linestyle='-', linewidth=1, color='purple')
    ax.legend(['Step Response', 'Actuating Signal', 'Proprtional Component', 'Integral Component', 'Derivative Component'])
    ax.set_ylabel('Rotational Frequency / Actuating Signal')

    plt.title(title)
    plt.savefig(f'plots/{fname}_actuating.pdf',
                bbox_inches='tight', pad_inches=0)
    plt.close()
