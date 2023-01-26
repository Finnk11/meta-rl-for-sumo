import matplotlib.pyplot as plt


probs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
avg_queue_length_lst = [1.5391849529780564, 2.2836879432624113, 3.255039439088519, 4.468416735028712, 9.510853835021708, 10.445, 10.505714285714285, 10.560714285714285]
fairness_index_lst = [0.6651037970432295, 0.7013265780258279, 0.7463656199111278, 0.7829499350254596, 0.8562516100029591, 0.9011555575096744, 0.9186178199400529, 0.9114161227768788]

#peaks
peaks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
avg_queue_length_lst_dyn = [1.8969957081545064, 3.048048048048048, 6.442356959863365, 10.04335260115607, 10.128612716763005, 10.207913669064748, 10.361428571428572, 10.505714285714285, 10.502142857142857, 10.52]
fairness_index_lst_dyn = [0.670399486758653, 0.74442194414501, 0.7171261801336191, 0.8652786623481107, 0.8800947639660441, 0.8899770942736861, 0.9094041792702219, 0.9031957478270247, 0.9093102054073449, 0.9110129195406327]


fig, axs = plt.subplots(2, 1, figsize=(7, 15))
axs[0].plot(probs,avg_queue_length_lst,'--bo')
axs[0].set(xlabel='prob', ylabel='Average queue length per lane (vehicle)')
axs[0].legend(['Fixed', 'Second List'], loc='upper left')

axs[1].plot(probs, fairness_index_lst, '--bo')
axs[1].set(xlabel='prob', ylabel='Jain fairness index')
axs[1].legend(['Fixed', 'Second List'], loc='upper left')

fig.suptitle('Performance comparison between fixed, queue-length-based,\n'
             'and delay-based agent with static uniform\n'
             'arrivals at all lanes with probability prob.')


plt.show()

raise Exception('exit')



fig, axs = plt.subplots(2, 1, figsize=(7, 15))
axs[0].plot(peaks, avg_queue_length_lst_dyn, '--bo')
axs[0].set(xlabel='peak', ylabel='Average queue length per lane (vehicle)')
axs[0].legend(['Fixed', 'Second List'], loc='upper left')

axs[1].plot(peaks, fairness_index_lst_dyn, '--bo')
axs[1].set(xlabel='peak', ylabel='Jain fairness index')
axs[1].legend(['Fixed', 'Second List'], loc='upper left')

fig.suptitle('Performance comparison between fixed, queue-length-based,\n'
             'and delay-based agent with dynamic uniform\n'
             'arrivals at all lanes wrt certain peaks.')


plt.show()

















