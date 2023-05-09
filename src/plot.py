import pandas as pd
import matplotlib.pyplot as plt


csv_file = "./res.csv"
data = pd.read_csv(csv_file)

plt.plot(data["minute"], data["total_power"])
plt.xlabel("Minute")
plt.ylabel("Rated power")
plt.title("Device schedule")
plt.show()
