import particleDataStructures
import math

def normalise(particles):
    tot_weight = 0
    for (x, y, theta, w) in particles:
        tot_weight += w
    i = 0
    for (x, y, theta, w) in particles:
        particles[i] = (x, y, theta, w / (tot_weight * 1.0))
        i=i+1;
    return particles


#p = [(0, 0, 1, 2), (0, 1, 2, 3), (1, 0, 3, 4), (1, 1, 3, 1)]
#n_p = normalise(p[:])
#print("Particles: ", p)
#print("Normalised particles: ", n_p)