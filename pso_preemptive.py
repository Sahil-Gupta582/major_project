import numpy as np


# Define the problem
def objective_function(x):
    # Your objective function here
    y = np.sum(np.square(x))  # Sum of squares of all elements in x
    return y
    # pass


# Initialize the particles
n_particles = 50
n_dimensions = 10
particles = np.random.rand(n_particles, n_dimensions)  # Initialize the positions
velocities = np.random.rand(n_particles, n_dimensions)  # Initialize the velocities

# Define the best positions of the particles
best_positions = particles.copy()
best_fitnesses = np.array([objective_function(p) for p in particles])

# Define the best position of the swarm
global_best_position = best_positions[np.argmin(best_fitnesses)]
global_best_fitness = np.min(best_fitnesses)

# Set the PSO parameters
w = 0.8  # Inertia weight
c1 = 2.0  # Cognitive weight
c2 = 2.0  # Social weight

# Run the PSO algorithm
max_iterations = 100
for i in range(max_iterations):
    # Update the velocities
    r1, r2 = np.random.rand(n_particles, n_dimensions), np.random.rand(n_particles, n_dimensions)
    velocities = w * velocities + c1 * r1 * (best_positions - particles) + c2 * r2 * (global_best_position - particles)

    # Update the positions
    particles = particles + velocities

    # Evaluate the fitnesses
    fitnesses = np.array([objective_function(p) for p in particles])

    # Update the best positions
    improved_indices = fitnesses < best_fitnesses
    best_positions[improved_indices] = particles[improved_indices]
    best_fitnesses[improved_indices] = fitnesses[improved_indices]

    # Update the best position of the swarm
    new_global_best_index = np.argmin(best_fitnesses)
    if best_fitnesses[new_global_best_index] < global_best_fitness:
        global_best_position = best_positions[new_global_best_index]
        global_best_fitness = best_fitnesses[new_global_best_index]

    # Stopping criterion
    if i % 10 == 0:
        print(f"Iteration {i}: Best fitness = {global_best_fitness}")
