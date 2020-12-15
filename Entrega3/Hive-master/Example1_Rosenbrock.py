import math

import numpy as np
from Hive import Utilities
from Hive import Hive


# ---- CREATE TEST CASE

def Rosenbrock(vector, a=1, b=100):
    """

    The Rosenbrock function is a non-convex function used as a performance test
    problem for optimization algorithms introduced by Howard H. Rosenbrock in
    1960. It is also known as Rosenbrock's valley or Rosenbrock's banana
    function.

    The function is defined by

                        f(x, y) = (a-x)^2 + b(y-x^2)^2

    It has a global minimum at (x, y) = (a, a**2), where f(x, y) = 0.

    """

    vector = np.array(vector)

    return (a - vector[0])**2 + b * (vector[1] - vector[0]**2)**2




def run():

    # Crea el modelo
    ndim = int(2)
    model = Hive.BeeHive(lower     = [0 for i in range(ndim)],
                         upper     = [10 for i in range(ndim)],
                         fun       = Rosenbrock ,
                         numb_bees =  50       ,
                         max_itrs  =  60       ,)

    # Corre el modelo
    cost = model.run()

    # Grafica de convergencia
    Utilities.ConvergencePlot(cost)

    # Prints
    print("Fitness Value ABC: {0}".format(model.best))
    print("Solution: {0}".format(cost["solution"]))


if __name__ == "__main__":
    run()


# ---- END
