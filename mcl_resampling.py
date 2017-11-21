import particleDataStructures
import math
import random

def resample(particles):
    n = len(particles)
    weight_sum = 0
    cumulative_weights = [0] * n
    i = 0
    for (x, y, theta, w) in particles:
        weight_sum += w
        cumulative_weights[i] = weight_sum
        i = i+1
        
    #print(cumulative_weights)
    
    new_particle_set = [(0,0,0,0)] * n
    for n_i, (x, y, theta, w) in enumerate(new_particle_set):
        r = random.uniform(0, 1);
        #print(r)
        r_particle_index = 0;
        for cw_i, weight in enumerate(cumulative_weights):
            if r <= weight:
                (x_old, y_old, theta_old, w_old) = particles[cw_i]
                new_particle_set[n_i] = (x_old, y_old, theta_old, weight_sum / (n * 1.0))
                break
            
    
    return new_particle_set


#p = [(0, 0, 1, 0.1), (0, 1, 2, 0.1), (1, 0, 3, 0.1), (1, 1, 3, 0.7)]
#n_p = resample(p[:])
#print("Particles: ", p)
#print("Resampled particles: ", n_p)