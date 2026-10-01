import numpy as np
import matplotlib.pyplot as plt

#Ici nombre moyen d'arrivé par minute 
lambd = 18 / 60 


#Temps entre 0 et 20 minutes
t = np.linspace(0, 20)

# Densité de la loi exponentielle
f = lambd * np.exp(-lambd * t)


esperance = 1 / lambd
mediane = np.log(2) / lambd


print(lambd)
print(f)

    
plt.plot(t, f)


plt.plot([esperance for _ in range(50)], np.linspace(0, lambd) , label=f"Espérance: {esperance:.2f} min")
plt.plot([mediane for _ in range(50)], np.linspace(0, lambd) , label=f"Médiane: {mediane:.2f} min")
plt.title("Loi exponentielle")
plt.xlabel("Temps en minutes (t)")
plt.plot(0, lambd, 'ro', label=f"f(0) = lambda = {lambd:.2f}")
plt.ylabel("f(t)")
plt.legend()
plt.grid()
plt.show()
