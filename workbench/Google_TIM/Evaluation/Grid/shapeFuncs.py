import numpy as np
import matplotlib.pyplot as plt

def plot_shape_functions_quad():
    # Define local coordinates for the 2D quadrilateral element
    xi = np.linspace(-1, 1, 100)
    eta = np.linspace(-1, 1, 100)
    xi, eta = np.meshgrid(xi, eta)
    
    # Shape functions for a 2D quadrilateral element
    N1 = 0.25 * (1 - xi) * (1 - eta)  # Node 1: (-1, -1)
    N2 = 0.25 * (1 + xi) * (1 - eta)  # Node 2: (1, -1)
    N3 = 0.25 * (1 + xi) * (1 + eta)  # Node 3: (1, 1)
    N4 = 0.25 * (1 - xi) * (1 + eta)  # Node 4: (-1, 1)
    
    # Plot the shape functions
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('2D Linear Shape Functions for a Quadrilateral Element', fontsize=16)
    
    # N1 plot
    axs[0, 0].contourf(xi, eta, N1, levels=50, cmap="viridis")
    axs[0, 0].set_title('Shape Function N1 (-1, -1)')
    axs[0, 0].set_xlabel('ξ')
    axs[0, 0].set_ylabel('η')

    # N2 plot
    axs[0, 1].contourf(xi, eta, N2, levels=50, cmap="viridis")
    axs[0, 1].set_title('Shape Function N2 (1, -1)')
    axs[0, 1].set_xlabel('ξ')
    axs[0, 1].set_ylabel('η')

    # N3 plot
    axs[1, 0].contourf(xi, eta, N3, levels=50, cmap="viridis")
    axs[1, 0].set_title('Shape Function N3 (1, 1)')
    axs[1, 0].set_xlabel('ξ')
    axs[1, 0].set_ylabel('η')

    # N4 plot
    axs[1, 1].contourf(xi, eta, N4, levels=50, cmap="viridis")
    axs[1, 1].set_title('Shape Function N4 (-1, 1)')
    axs[1, 1].set_xlabel('ξ')
    axs[1, 1].set_ylabel('η')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

plot_shape_functions_quad()
