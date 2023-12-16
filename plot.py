import matplotlib.pyplot as plt

colorsDict = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'purple',
    5: 'cyan',
    6: 'magenta',
    7: 'yellow',
    8: 'brown',
    9: 'pink'
}

def plot(startTimeMatrix, endTimeMatrix):
    nJobs = len(startTimeMatrix)
    nMachines = len(startTimeMatrix[0])

    fig, ax = plt.subplots()
    handles = []
    labels = []

    for machine in range(nMachines):
        for job in range(nJobs):
            ax.hlines(job, startTimeMatrix[job, machine], endTimeMatrix[job, machine],
                      colors=colorsDict[machine], lw=4)
        
        # Add a handle and label for the legend
        handle, = ax.plot([], [], color=colorsDict[machine], label=f"Machine {machine}")
        handles.append(handle)
        labels.append(f"Machine {machine}")

    # Set the y-axis limits based on the number of jobs
    ax.set_ylim(-0.5, nJobs + 1)

    # Set the y-tick labels to display job numbers
    ax.set_yticks(range(nJobs))
    ax.set_yticklabels([f"Job {job}" for job in range(nJobs)])

    # Add the legend
    ax.legend(handles, labels)

    # Set margins and display the plot
    plt.margins(0.1)
    plt.show()