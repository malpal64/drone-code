import numpy as np

# Parameters
target_height_window = []  
window_size = 5  

def get_smoothed_target(target_height):
    target_height_window.append(target_height)
    if len(target_height_window) > window_size:
        target_height_window.pop(0)
    return np.mean(target_height_window)

# Parameters for sensor
weight_altimeter = 0.6
weight_accelerometer = 0.4

def sensor_fusion(altimeter_height, accelerometer_height):
    return weight_altimeter * altimeter_height + weight_accelerometer * accelerometer_height


# Adaptive PID tuning based on load
base_kp = 1.0
base_ki = 0.5
base_kd = 0.1

def adjust_pid_for_load(error, drone_response_speed):
    # Tune PID gains based on load (response speed)
    kp = base_kp * (1 + 0.1 * (1 - drone_response_speed))
    ki = base_ki * (1 + 0.1 * (1 - drone_response_speed))
    kd = base_kd * (1 + 0.1 * (1 - drone_response_speed))
    return kp, ki, kd

# Battery management
battery_threshold = 30 
thrust_limit_low_battery = 0.8  

def adjust_thrust_for_battery(current_thrust, battery_level):
    if battery_level < battery_threshold:
        return current_thrust * thrust_limit_low_battery
    return current_thrust

# Parameters
target_height_window = []
last_filtered_signal = 0.0
battery_level = 100  # Assume fully charged at start
response_speed = 1.0  # Assume ideal response initially

while drone_flight_active:
    # Inputs
    randomized_target_height = np.random.uniform(0.8, 1.2)  # Random height
    noisy_signal = np.random.normal(0, 0.05)  # Simulated noise
    altimeter_height = 1.0  # Mock reading
    accelerometer_height = 0.98  # Mock reading
    
    # Adaptations
    smoothed_target_height = get_smoothed_target(randomized_target_height)
    filtered_signal = low_pass_filter(noisy_signal, last_filtered_signal)
    last_filtered_signal = filtered_signal
    fused_height = sensor_fusion(altimeter_height, accelerometer_height)
    kp, ki, kd = adjust_pid_for_load(current_error, response_speed)
    adjusted_thrust = adjust_thrust_for_battery(current_thrust, battery_level)

    # PID control logic
    error = smoothed_target_height - fused_height
    control_output = kp * error + ki * integral + kd * derivative
    current_thrust = max(min(control_output, adjusted_thrust), 0)

    # Update drone state and battery
    battery_level -= 0.1  # Example of gradual battery drain


