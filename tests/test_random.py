import random
import matplotlib.pyplot as pg

if __name__ == "__main__":
    m_random_values = [random.gauss(0, 1) for _ in range(10000)]
    pg.hist(m_random_values, bins=50)
    pg.xlabel("Sample Index")
    pg.ylabel("Random Value")
    pg.title("Random Gaussian Values Scatter Plot")
    pg.grid()
    pg.show()