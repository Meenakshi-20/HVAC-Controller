import random
import time
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

class HVACController:
    def __init__(self):
        self.temp_history = []
        self.humidity_history = []
        self.occupancy_history = []
        self.ac_status_history = []
        self.timestamps = []
        
        # Occupancy schedule (8AM-6PM work hours)
        self.occupancy_schedule = np.zeros(24*60)
        for t in range(8*60, 18*60):  # 8AM-6PM
            self.occupancy_schedule[t] = 1 if random.random() < 0.7 else 0  # 70% chance occupied

    def get_current_occupancy(self):
        now = datetime.now()
        minute_of_day = now.hour * 60 + now.minute
        return self.occupancy_schedule[minute_of_day % (24*60)]

    def decide(self, temp: float, humidity: float) -> str:
        occupied = self.get_current_occupancy()
        
        self.temp_history.append(temp)
        self.humidity_history.append(humidity)
        self.occupancy_history.append(occupied)
        self.timestamps.append(datetime.now())
        
        if len(self.temp_history) >= 5:
            avg_temp = sum(self.temp_history[-5:]) / 5
            avg_humidity = sum(self.humidity_history[-5:]) / 5
            
            # More sophisticated decision making
            if (avg_temp > (26 if occupied else 22)) or (avg_humidity > (75 if occupied else 85)):
                status = "AC ON"
            else:
                status = "AC OFF"
        else:
            status = "AC OFF"
            
        self.ac_status_history.append(1 if status == "AC ON" else 0)
        return status

def plot_data(controller: HVACController, ax1, ax2):
    # Clear previous frame but keep window open
    ax1.clear()
    ax2.clear()
    
    # Set light grey background for both subplots
    ax1.set_facecolor('#f5f5f5')  # Light grey
    ax2.set_facecolor('#f5f5f5')  # Light grey
    
    # Temperature and Humidity Plot
    ax1.plot(controller.timestamps, controller.temp_history, 'r-', label='Temperature (°C)')
    ax1.plot(controller.timestamps, controller.humidity_history, 'g--', label='Humidity (%)')
    ax1.axhline(y=25, color='orange', linestyle=':', label='Temp Threshold')
    ax1.set_ylabel('Temperature/Humidity')
    ax1.legend(loc='upper left')
    
    # Occupancy and AC Status Plot
    ax2.step(controller.timestamps, controller.occupancy_history, 'b-', 
             where='post', label='Occupancy', alpha=0.7)
    ax2.step(controller.timestamps, controller.ac_status_history, 'm-', 
             where='post', label='AC Status', alpha=0.7)
    ax2.set_ylabel('Occupancy/AC Status')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['OFF', 'ON'])
    ax2.legend(loc='upper right')
    
    # Formatting
    plt.title('HVAC System Monitoring - Live Data')
    plt.xlabel('Time')
    ax1.grid(True, color='white', linestyle='-', linewidth=0.5)
    ax2.grid(True, color='white', linestyle='-', linewidth=0.5)
    plt.gcf().set_facecolor('#f5f5f5')  # Light grey for figure background
    plt.tight_layout()

def main():
    controller = HVACController()
    
    # Set up the figure and axes once
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.set_facecolor('#f5f5f5')  # Light grey for the entire figure
    
    try:
        while True:
            temp = random.uniform(20, 30)
            humidity = random.uniform(30, 90)
            action = controller.decide(temp, humidity)
            
            print(f"{datetime.now().strftime('%H:%M:%S')} | "
                  f"{temp:.1f}°C | {humidity:.1f}% | "
                  f"Occupied: {controller.occupancy_history[-1]} | {action}")
            
            plot_data(controller, ax1, ax2)
            plt.pause(2)  # Update every 2 seconds
            
    except KeyboardInterrupt:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()
