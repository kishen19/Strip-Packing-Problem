def visual_plot(l, w, h):  # Function for Visualization of Packing
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    # print(l)
    for i in range(len(l)):
        ax.add_patch(patches.Rectangle(
            tuple(l[i][0]), l[i][1][0]-l[i][0][0], l[i][1][1]-l[i][0][1], linewidth=0.5, edgecolor='black', facecolor='none'
        ))
        # fontsize=10*round((l[i][1][1]-l[i][0][1]), 1)
        ax.text(l[i][1][0]-0.5*(l[i][1][0]-l[i][0][0]), l[i][1][1]-0.5 *
                (l[i][1][1]-l[i][0][1]), str(i), horizontalalignment='center')
    plt.show()
