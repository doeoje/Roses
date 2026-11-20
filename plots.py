import csv
import matplotlib.pyplot as plt
import itertools

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

#Set, Treatment, Wavelength, Fluence, Pulsecount, Survival Fraction, Rep Rate, Species
Treatments = []

controls = []
for m in metadata[1:]:
    for d in data[1:]: 
        if m[0] == d[0] and m[1]==d[4]:
            try:
                survival_fraction = float(d[3])
                if(d[5] == 'yes'):
                    Treatments.append([m[0],m[1],m[2],m[3],m[4],survival_fraction,d[9],d[10]])
                #Treated=='no' & Inoculated=='yes' & Coupon=='yes
                if(d[5] == 'no' and d[6] == 'yes' and d[7] == 'yes'):
                    controls.append([m[0],d[3]])
            except:
                pass


sets = sorted(set(Treatments[i][0] for i in range(len(Treatments))))
pulse_counts = sorted(set(Treatments[i][4] for i in range(len(Treatments))))
wavelengths = sorted(set(Treatments[i][2] for i in range(len(Treatments))))
repetition_rates = sorted(set(Treatments[i][6] for i in range(len(Treatments))))
for s in sets:
    sum = 0
    n = 0
    for control in controls:
        if control[0] == s:
            sum += float(control[1])
            n += 1
    avg = sum/n
    for treatment in Treatments:
        if treatment[0] == s:
            treatment[5] = treatment[5]/avg


fig, ax = plt.subplots()
fig2,ax2 = plt.subplots()



linestyles = itertools.cycle(['solid', 'dashed'])
markers = itertools.cycle(['o','^','s'])
for wavelength in wavelengths:
    if wavelength != 'NA':
        linestyle = next(linestyles)
        for pulse_count in pulse_counts:
            marker = next(markers)
            fluences =[]
            survivals = []
            wave_pulses =[]
            if pulse_count == '100000' or pulse_count == '10000' or pulse_count == '1000':
                for treatment in Treatments:
                    if treatment[2] == wavelength and treatment[4] == pulse_count and treatment[7] != 'subtilis':
                        try:
                            fluences.append(float(treatment[3]))
                            if float(treatment[5]) == 0:
                                survivals.append(1e-6)
                            else:
                                survivals.append(float(treatment[5]))
                            wave_pulses.append(pulse_count)
                        except:
                            pass
                
                fs = set(fluences[i] for i in range(len(fluences)))
                avg_survival_per_fluence = []
                fs = sorted(fs)
                maxs = []
                mins = []
                for f in fs:
                    sum = 0
                    n = 0
                    max = 0
                    min = 1
                    for i in range(len(fluences)):
                        if f == fluences[i]:
                            sum += survivals[i]
                            n += 1
                            if survivals[i] < min :
                                min = survivals[i]
                            if survivals[i] > max :
                                max = survivals[i]
                    avg = sum/n
                    avg_survival_per_fluence.append(avg)
                    maxs.append((max-avg))
                    mins.append((avg-min))
                errors = [mins,maxs]
                # ax.plot(list(fs),avg_survival_per_fluence,label=f'{wavelength} nm {pulse_count}pulses')
                ax.errorbar(list(fs),avg_survival_per_fluence,yerr=errors,capsize=6,label=f'{wavelength}nm {pulse_count}pulses', linestyle=linestyle, marker=marker)
                ax2.plot(list(fs),avg_survival_per_fluence,label=f'{wavelength}nm {pulse_count}pulses', linestyle=linestyle, marker=marker)
ax.set_yscale('log')
ax2.set_yscale('log')
ax.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
ax.set_title(f'Wavelength Survival')
ax.set_xlabel('Fluence')
ax.set_ylabel('Survival Fraction')
box = ax.get_position()
ax.set_position([box.y0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
ax.legend(loc ='upper center', bbox_to_anchor=(.5, -0.15), ncol = 3, frameon=False)
fig.savefig(f'plots/wavelength_survival.png')
ax2.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
ax2.set_title(f'Wavelength Survival Averages')
ax2.set_xlabel('Fluence')
ax2.set_ylabel('Survival Fraction')
box2 = ax2.get_position()
ax2.set_position([box2.y0, box2.y0 + box2.height * 0.2, box2.width, box2.height * 0.8])
ax2.legend(loc ='upper center', bbox_to_anchor=(.5, -0.15), ncol = 3, frameon=False)
fig2.savefig(f'plots/wavelength_survival_avg.png')
plt.close(fig2)
plt.close(fig)

#Reptition Rate with error bar per set
for wavelength in wavelengths:
    markers = itertools.cycle(['o','^','s','D'])
    fig, ax = plt.subplots()
    for repetition_rate in repetition_rates:
        if repetition_rate != 'NA' and repetition_rate != '':
            fluences = []
            survival = []
            for treatment in Treatments:
                if  treatment[6] == repetition_rate and treatment[4] == '10000' and wavelength == treatment[2] and treatment[7] == 'Subtilis':
                    try:
                        fluences.append(float(treatment[3]))
                        if float(treatment[5]) == 0:
                            survival.append(float(1e-6))
                        else:
                            survival.append(float(treatment[5]))
                    except:
                        pass
            fs = set(fluences)
            avg_survival_per_fluence = []
            fs = sorted(fs)
            maxs = []
            mins = []
            for f in fs:
                sum = 0
                n = 0
                max = 0
                min = 1
                for i in range(len(fluences)):
                    if f == fluences[i]:
                        sum += survival[i]
                        n += 1
                        if survival[i] < min :
                            min = survival[i]
                        if survival[i] > max :
                            max = survival[i]
                avg = sum/n
                avg_survival_per_fluence.append(avg)
                maxs.append((max-avg))
                mins.append((avg-min))
            ax.plot(list(fs),avg_survival_per_fluence,label=f'{repetition_rate}Hz', marker=next(markers))
    ax.set_yscale('log')
    ax.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
    ax.set_title(f'Repetition Rate Survival')
    ax.set_xlabel('Fluence')
    ax.set_ylabel('Survival Fraction')
    ax.legend()
    fig.savefig(f'plots/Repetition_Rate_Survival_{wavelength}.png')

    

for wavelength in wavelengths:
    if wavelength != 'NA':
        for pulse_count in pulse_counts:
            fluences = []
            survival = []
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
                    survival.append(y)
                    treatment_sets.append(s)
            if len(fluences) > 0 and len(survival) > 0:
                fig, ax = plt.subplots()
                for i in range(len(fluences)):
                    ax.scatter(fluences[i], survival[i], label=treatment_sets[i])
                ax.set_yscale('log')
                plt.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
                plt.title(f'Wavelength: {wavelength} nm, Pulse Count: {pulse_count}')
                plt.xlabel('Fluence')
                plt.ylabel('Survival Fraction')
                plt.legend()
                plt.savefig(f'plots/Wavelength_{wavelength}_PulseCount_{pulse_count}.png')
                plt.close(fig)
for set in sets:
    set_fluences = []
    set_pulses = []
    set_survival = []
    for pulse_count in pulse_counts:
        fluences = []
        survival = []
        for treatment in Treatments:
            if treatment[0] == set and treatment[4] == pulse_count:
                try:
                    fluences.append(float(treatment[3]))
                    if float(treatment[5]) == 0:
                        survival.append(float(1e-6))
                    else:
                        survival.append(float(treatment[5]))
                except:
                    pass
        if len(fluences) > 0 and len(survival) > 0:
            set_fluences.append(fluences)
            set_survival.append(survival)
            set_pulses.append(pulse_count)
    fig, ax = plt.subplots()
    for i in range(len(set_fluences)):
        ax.scatter(set_fluences[i], set_survival[i], label=set_pulses[i])
    ax.set_yscale('log')
    plt.axhline(y=1e-6, color='r', linestyle='--', label='No Survival')
    plt.title(f'Set: {set}')
    plt.xlabel('Fluence')
    plt.ylabel('Survival Fraction')
    plt.legend(ncol= 2)
    plt.savefig(f'plots/Set_{set}.png')
    plt.close(fig)






