import numpy as np
import matplotlib.pyplot as plt

# Initial setup
time_steps = 200
dt = 0.1  # Time step duration
target_height = 1.0  # Initial target height in meters
altitude = 0.0  # Initial drone altitude
altitude_history = []
control_signal_history = []


Kp = 0.8
Ki = 0.2
Kd = 0.1


random_target_changes = True  # Randomize target height
interference_signals = True  # Introduce interference
sensor_calibration_error = True  # Sensor drift
varying_load = True  # Simulate load changes
battery_fluctuations = True  # Simulate battery drain or motor limitations


integral = 0.0
prev_error = 0.0


target_height_variation = 0.5  # Max variation for target height changes
interference_amplitude = 0.02  # Magnitude of interference signal
sensor_drift_rate = 0.001  # Drift rate of sensor calibration error
load_variation_amplitude = 0.05  # Amplitude of varying load effect
battery_drain_rate = 0.0005  # Rate of battery limitation over time

# Simulation
for t in range(time_steps):
    time = t * dt
    
    # Randomize target height at specific intervals
    if random_target_changes and t % 50 == 0:
        target_height = 1.0 + np.random.uniform(-target_height_variation, target_height_variation)
    
    # Calculate error and update PID controller
    error = target_height - altitude
    integral += error * dt
    derivative = (error - prev_error) / dt
    prev_error = error
    
 
    control_signal = Kp * error + Ki * integral + Kd * derivative
    
  
    if battery_fluctuations:
        control_signal *= (1 - battery_drain_rate * t)  # Simulate battery power decrease over time
    

    if interference_signals:
        control_signal += np.random.uniform(-interference_amplitude, interference_amplitude)
    

    if sensor_calibration_error:
        altitude += sensor_drift_rate * t  # Simulate gradual sensor drift
    
    if varying_load:
        control_signal += np.random.uniform(-load_variation_amplitude, load_variation_amplitude)
    
   
    altitude += control_signal * dt
    
  
    altitude = max(0, altitude)
    
  
    altitude_history.append(altitude)
    control_signal_history.append(control_signal)

# Plot results
plt.figure(figsize=(14, 6))

# Plot altitude
plt.subplot(1, 2, 1)
plt.plot(np.arange(0, time_steps * dt, dt), altitude_history, color='blue')
plt.axhline(y=1.0, color='red', linestyle='--', linewidth=1)  # Target height line
plt.title('Drone Altitude Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.grid(True)

# Plot control signal
plt.subplot(1, 2, 2)
plt.plot(np.arange(0, time_steps * dt, dt), control_signal_history, color='green')
plt.title('Control Signal Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Control Signal')
plt.grid(True)

plt.tight_layout()
plt.show()
