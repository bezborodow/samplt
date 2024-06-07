# Part A.
# Open loop.
tm, mm = datalog_step('openloop', 'Open Loop Step Response')

# Transfer function.
fig, ax = newplot()
plt.title('Open Loop Transfer Function')
ax.plot(tm, mm, linestyle='-', linewidth=1, color='black')

lti = signal.lti([50 * 0.9], [0.115, 1.0])
t, y = signal.step(lti)
plt.plot(t, y, linewidth=1.5, linestyle='--', color='red')
#plt.plot(t, 50 * 0.9 * (1 - np.exp(-t / 0.115)), linewidth=1.5, linestyle='--', color='blue')
plt.legend(['Averaged Plant Step Response', 'Transfer Function Step Response'])
plt.savefig(f'plots/tf.pdf',
            bbox_inches='tight', pad_inches=0)
plt.close()
datalog_step('i_count_50ms', 'Integral Count 50 ms')
datalog_actuating('i_count_50ms', 'Integral Count 50 ms')
datalog_step('pi_count_50ms', 'PI Count 50 ms')
datalog_actuating('pi_count_50ms', 'PI Count 50 ms')
datalog_step('pi_count_10ms', 'PI Count 10 ms')
datalog_actuating('pi_count_10ms', 'PI Count 10 ms')
datalog_step('pi_interval_10ms', 'PI Interval 10 ms')
datalog_actuating('pi_interval_10ms', 'PI Interval 10 ms')
