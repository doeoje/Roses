import csv
import matplotlib.pyplot as plt

data = []
metadata = []

with open('Data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

with open('MetaData.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        metadata.append(row)

#Set, Treatment, Wavelength, Fluence, Pulsecount, Survival Fraction,
Treatments = []


for m in metadata[1:]:
    for d in data[1:]: 
        if m[0] == d[0] and m[1]==d[4]:
            try:
                survival_fraction = float(d[3])/float(d[8])
                Treatments.append((m[0],m[1],m[2],m[3],m[4],survival_fraction))
            except:
                pass

#plot 515, 10k pulse count

sets = set(Treatments[i][0] for i in range(len(Treatments)))
pulse_counts = set(Treatments[i][4] for i in range(len(Treatments)))
wavelengths = set(Treatments[i][2] for i in range(len(Treatments)))
print(f'Sets: {sets}')

for wavelength in wavelengths:
    if wavelength != 'NA':

        for pulse_count in pulse_counts:
            fluences = []
            pulses = []
            treatment_sets = []
            for s in sets:
                x = []
                y = []
                for treatment in Treatments:
                    if treatment[0] == s and treatment[2] == wavelength and treatment[4] == pulse_count:
                        try:
                            x.append(float(treatment[3]))
                            if float(treatment[5]) == 0:
                                y.append(float(1e-6))
                            else:
                                y.append(float(treatment[5]))
                        except:
                            pass
                if len(x) > 0 and len(y) > 0:
                    fluences.append(x)
                    pulses.append(y)
                    treatment_sets.append(s)
            if len(fluences) > 0 and len(pulses) > 0:
                fig, ax = plt.subplots()
                for i in range(len(fluences)):
                    ax.scatter(fluences[i], pulses[i], label=treatment_sets[i])
                ax.set_yscale('log')
                plt.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
                plt.title(f'Wavelength: {wavelength} nm, Pulse Count: {pulse_count}')
                plt.xlabel('Fluence')
                plt.ylabel('Survival Fraction')
                plt.legend()
                plt.savefig(f'plots/Wavelength_{wavelength}_PulseCount_{pulse_count}.png')

#print each set
for s in sets:
    xs = []
    ys = []
    pulses = []
    for pulse_count in pulse_counts:
        fluences = []
        survival_fractions = []
        for treatment in Treatments:

            if treatment[0] == s and treatment[4] == pulse_count:
                try:
                    fluences.append(float(treatment[3]))
                    if float(treatment[5]) == 0:
                        survival_fractions.append(float(1e-6))
                    else:
                        survival_fractions.append(float(treatment[5]))
                except:
                    pass
        if len(fluences) > 0 and len(survival_fractions) > 0:
            xs.append(fluences)
            ys.append(survival_fractions)
            pulses.append(pulse_count)
    fig, ax = plt.subplots()
    for i in range(len(xs)):

        ax.scatter(xs[i], ys[i], label=f'Pulse Count: {pulses[i]}')
    ax.set_yscale('log')
    plt.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
    plt.title(f'Set: {s}, Pulse Count: {pulses[i]}')
    plt.xlabel('Fluence')
    plt.ylabel('Survival Fraction')
    plt.legend()
    plt.savefig(f'plots/Set_{s}_PulseCount_{pulses[i]}.png')
            


# fig, ax = plt.subplots()

# for s in sets:
#     x = []
#     y = []
#     for treatment in Treatments:
#         if treatment[0] == s[0] and treatment[4] == '10000':
#             x.append(float(treatment[3]))
#             if float(treatment[5]) == 0:
#                 y.append(float(1e-6))
#             else:
#                 y.append(float(treatment[5]))
#     if len(x) > 0 and len(y) > 0:
#         ax.scatter(x, y, label=s[0])
# ax.set_yscale('log')
# plt.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
# plt.legend()



