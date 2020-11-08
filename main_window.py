import tkinter as tk
from tkinter import messagebox
import re
from PendulumTurtleCanvas import ThreadTransmitter, Simulator
import threading

root = tk.Tk()
root.title("Cart Pendulum Simulation")

# Create LabelFrame for all sections.
system_properties_frame = tk.LabelFrame(root, text="System Properties")
initial_conditions_frame = tk.LabelFrame(root, text="Initial Conditions")
forcing_frame = tk.LabelFrame(root, text="Cart Forcing", height=300)
simulation_properties_frame = tk.LabelFrame(root, text="Simulation Properties")

# Place LabelFrame for all sections.
system_properties_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
initial_conditions_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
forcing_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
simulation_properties_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=7, sticky='EW')

# System Properties Frame
# Labels
cart_mass_label = tk.Label(system_properties_frame, text="Cart Mass: ", width=16, anchor='e')
pendulum_mass_label = tk.Label(system_properties_frame, text="Pendulum Mass: ", width=16, anchor='e')
pendulum_length_label = tk.Label(system_properties_frame, text="Pendulum Length: ", width=16, anchor='e')

# Entries
cart_mass_entry = tk.Entry(system_properties_frame, width=9)
pendulum_mass_entry = tk.Entry(system_properties_frame, width=9)
pendulum_length_entry = tk.Entry(system_properties_frame, width=9)

# Units
cart_mass_units = tk.Label(system_properties_frame, text="[kg]", width=6, anchor='w')
pendulum_mass_units = tk.Label(system_properties_frame, text="[kg]", width=6, anchor='w')
pendulum_length_units = tk.Label(system_properties_frame, text="[m]", width=6, anchor='w')

# Placements
cart_mass_label.grid(row=0, column=0, pady=4)
pendulum_mass_label.grid(row=1, column=0, pady=4)
pendulum_length_label.grid(row=2, column=0, pady=4)

cart_mass_entry.grid(row=0, column=1)
pendulum_mass_entry.grid(row=1, column=1)
pendulum_length_entry.grid(row=2, column=1)

cart_mass_units.grid(row=0, column=2, padx=2)
pendulum_mass_units.grid(row=1, column=2, padx=2)
pendulum_length_units.grid(row=2, column=2, padx=2)

# Initial Conditions Frame
# Labels
cart_position_label = tk.Label(initial_conditions_frame, text="Cart Position: ", width=16, anchor='e')
cart_velocity_label = tk.Label(initial_conditions_frame, text="Cart Velocity: ", width=16, anchor='e')
pendulum_position_label = tk.Label(initial_conditions_frame, text="Pendulum Position: ", width=16, anchor='e')
pendulum_velocity_label = tk.Label(initial_conditions_frame, text="Pendulum Velocity: ", width=16, anchor='e')

# Entries
cart_position_entry = tk.Entry(initial_conditions_frame, width=9)
cart_velocity_entry = tk.Entry(initial_conditions_frame, width=9)
pendulum_position_entry = tk.Entry(initial_conditions_frame, width=9)
pendulum_velocity_entry = tk.Entry(initial_conditions_frame, width=9)

# Units
cart_position_units = tk.Label(initial_conditions_frame, text="[m]", width=6, anchor='w')
cart_velocity_units = tk.Label(initial_conditions_frame, text="[m/s]", width=6, anchor='w')
pendulum_position_units = tk.Label(initial_conditions_frame, text="[deg]", width=6, anchor='w')
pendulum_velocity_units = tk.Label(initial_conditions_frame, text="[deg/s]", width=6, anchor='w')

# Placements
cart_position_label.grid(row=0, column=0, pady=4)
cart_velocity_label.grid(row=1, column=0, pady=4)
pendulum_position_label.grid(row=2, column=0, pady=4)
pendulum_velocity_label.grid(row=3, column=0, pady=4)

cart_position_entry.grid(row=0, column=1)
cart_velocity_entry.grid(row=1, column=1)
pendulum_position_entry.grid(row=2, column=1)
pendulum_velocity_entry.grid(row=3, column=1)

cart_position_units.grid(row=0, column=2, padx=2)
cart_velocity_units.grid(row=1, column=2, padx=2)
pendulum_position_units.grid(row=2, column=2, padx=2)
pendulum_velocity_units.grid(row=3, column=2, padx=2)


# Forcing Frame
# Forcing Type Dropdown
def display_forcing_settings(*args):
    if forcing_type_variable.get() == 'Sinusoidal':
        amplitude_label.grid(row=1, column=0, pady=4, sticky='E')
        frequency_label.grid(row=2, column=0, pady=4, sticky='E')
        phase_shift_label.grid(row=3, column=0, pady=4, sticky='E')

        amplitude_entry.grid(row=1, column=1)
        frequency_entry.grid(row=2, column=1)
        phase_shift_entry.grid(row=3, column=1)

        amplitude_units.grid(row=1, column=2, padx=2)
        frequency_units.grid(row=2, column=2, padx=2)
        phase_shift_units.grid(row=3, column=2, padx=2)
    elif forcing_type_variable.get() == 'None':
        amplitude_label.grid_forget()
        frequency_label.grid_forget()
        phase_shift_label.grid_forget()
        amplitude_entry.grid_forget()
        frequency_entry.grid_forget()
        phase_shift_entry.grid_forget()
        amplitude_units.grid_forget()
        frequency_units.grid_forget()
        phase_shift_units.grid_forget()


forcing_type_options = ['None', 'Sinusoidal']
forcing_type_variable = tk.StringVar()
forcing_type_variable.set(forcing_type_options[1])
forcing_type_label = tk.Label(forcing_frame, text="Forcing Type: ", width=16, anchor='e')
forcing_type_select = tk.OptionMenu(forcing_frame, forcing_type_variable, *forcing_type_options,
                                    command=display_forcing_settings)
forcing_type_select.config(width=8)

# Labels
amplitude_label = tk.Label(forcing_frame, text="Amplitude: ", width=16, anchor='e')
frequency_label = tk.Label(forcing_frame, text="Frequency: ", width=16, anchor='e')
phase_shift_label = tk.Label(forcing_frame, text="Phase Shift: ", width=16, anchor='e')

# Entries
amplitude_entry = tk.Entry(forcing_frame, width=9)
frequency_entry = tk.Entry(forcing_frame, width=9)
phase_shift_entry = tk.Entry(forcing_frame, width=9)

# Units
amplitude_units = tk.Label(forcing_frame, text="[N]", width=6, anchor='w')
frequency_units = tk.Label(forcing_frame, text="[Hz]", width=6, anchor='w')
phase_shift_units = tk.Label(forcing_frame, text="[deg]", width=6, anchor='w')

# Placements
forcing_type_label.grid(row=0, column=0, pady=4, sticky='E')
forcing_type_select.grid(row=0, column=1, columnspan=2, sticky='W')

amplitude_label.grid(row=1, column=0, pady=4, sticky='E')
frequency_label.grid(row=2, column=0, pady=4, sticky='E')
phase_shift_label.grid(row=3, column=0, pady=4, sticky='E')

amplitude_entry.grid(row=1, column=1)
frequency_entry.grid(row=2, column=1)
phase_shift_entry.grid(row=3, column=1)

amplitude_units.grid(row=1, column=2, padx=2)
frequency_units.grid(row=2, column=2, padx=2)
phase_shift_units.grid(row=3, column=2, padx=2)

# Simulation Properties Frame
# Labels
time_step_label = tk.Label(simulation_properties_frame, text="Time Step: ", width=16, anchor='e')
end_time_label = tk.Label(simulation_properties_frame, text="End Time: ", width=16, anchor='e')

# Entries
time_step_entry = tk.Entry(simulation_properties_frame, width=9)
end_time_entry = tk.Entry(simulation_properties_frame, width=9)

# Units
time_step_units = tk.Label(simulation_properties_frame, text="[s]", width=6, anchor='w')
end_time_units = tk.Label(simulation_properties_frame, text="[s]", width=6, anchor='w')

# Stop at end time checkbox
end_time_boolean = tk.BooleanVar()
end_time_boolean.set(True)


def enable_disable_end_time():
    if end_time_boolean.get():
        end_time_entry.config(state='normal')
    else:
        end_time_entry.config(state='disabled')


end_time_checkbox = tk.Checkbutton(simulation_properties_frame, text="Simulate only up to end time.",
                                   variable=end_time_boolean, command=enable_disable_end_time)

# Placements
time_step_label.grid(row=0, column=0, pady=4)
end_time_label.grid(row=1, column=0, pady=4)

time_step_entry.grid(row=0, column=1)
end_time_entry.grid(row=1, column=1)

time_step_units.grid(row=0, column=2, padx=2)
end_time_units.grid(row=1, column=2, padx=2)
end_time_checkbox.grid(row=2, column=0, columnspan=3)


# Control Buttons
# Commands
def apply():
    inputs_valid, error_messages = verify_inputs()
    if inputs_valid:
        apply_button.config(state='normal')
        run_button.config(state='normal')
        pause_button.config(state='disabled')
        stop_button.config(state='disabled')
        save_inputs_to_text(get_settings_from_entries())
        transmitter.send(('apply', get_settings_from_entries()))
        until_button_pushed.set()

    else:
        # Generate error message
        error_message = 'Please fix the following inputs before continuing:\n'
        for error in error_messages:
            error_message = error_message + '\n-' + error
        messagebox.showerror('Invalid Inputs', error_message)


def run():
    apply_button.config(state='disabled')
    run_button.config(state='disabled')
    pause_button.config(state='normal')
    stop_button.config(state='normal')
    transmitter.send(('run', None))
    until_button_pushed.set()


def pause():
    apply_button.config(state='disabled')
    run_button.config(state='normal')
    pause_button.config(state='disabled')
    stop_button.config(state='normal')
    transmitter.send(('pause', None))
    until_button_pushed.set()


def stop():
    apply_button.config(state='normal')
    run_button.config(state='normal')
    pause_button.config(state='disabled')
    stop_button.config(state='disabled')
    transmitter.send(('stop', None))
    until_button_pushed.set()


# Buttons
apply_button = tk.Button(root, text="Apply", command=apply, pady=4, padx=7)
run_button = tk.Button(root, text="Run", command=run, pady=4, padx=7, state='disabled')
pause_button = tk.Button(root, text="Pause", command=pause, pady=4, padx=7, state='disabled')
stop_button = tk.Button(root, text="Stop", command=stop, pady=4, padx=7, state='disabled')

# Placements
apply_button.grid(row=4, column=0, pady=5)
run_button.grid(row=4, column=1)
pause_button.grid(row=4, column=2)
stop_button.grid(row=4, column=3)


# Verification and Setup Functions
def verify_inputs():
    """
    Checks all entry widgets to verify that their values are valid. Returns a tuple with the first entry being a boolean
    that is True if all entries are valid or false if otherwise. The second entry is a list containing all the error
    messages associated with the provided entries.
    """
    valid = True
    error_messages = []
    always_non_empty_entries = [
        (cart_mass_entry, 'Cart mass'),
        (pendulum_mass_entry, 'Pendulum mass'),
        (pendulum_length_entry, 'Pendulum length'),
        (cart_position_entry, 'Initial cart position'),
        (cart_velocity_entry, 'Initial cart velocity'),
        (pendulum_position_entry, 'Initial pendulum position'),
        (pendulum_velocity_entry, 'Initial pendulum velocity'),
        (time_step_entry, 'Time step'),
    ]
    sometime_empty_entries = [
        (amplitude_entry, 'Forcing amplitude'),
        (frequency_entry, 'Forcing frequency'),
        (phase_shift_entry, 'Forcing phase shift'),
        (end_time_entry, 'End time')
    ]
    non_zero_or_negative_entries = [
        (cart_mass_entry, 'Cart mass'),
        (pendulum_mass_entry, 'Pendulum mass'),
        (time_step_entry, 'Time step')
    ]

    # Check for empty entries
    for entry in always_non_empty_entries:
        try:
            if len(entry[0].get()) == 0:
                error_messages.append(entry[1] + ' does not have any value.')
                valid = False
            else:
                float(entry[0].get())
        except ValueError:
            valid = False
            error_messages.append(entry[1] + ' does not have a valid numeric value.')

    # Check for entries that may be allowed to be empty sometimes
    for entry in sometime_empty_entries:
        if ('Forcing' in entry[1] and forcing_type_variable.get() == 'Sinusoidal') or \
                ('End time' in entry[1] and end_time_boolean.get()):
            try:
                if len(entry[0].get()) == 0:
                    error_messages.append(entry[1] + ' does not have any value.')
                    valid = False
                else:
                    float(entry[0].get())
            except ValueError:
                valid = False
                error_messages.append(entry[1] + ' does not have a valid numeric value.')

    # Check for entries with values <= 0
    for entry in non_zero_or_negative_entries:
        try:
            if float(entry[0].get()) <= 0:
                error_messages.append(entry[1] + ' cannot be less than or equal to 0.')
                valid = False
        except ValueError:
            pass

    return valid, error_messages


def get_settings_from_entries():
    """Gets settings from entries and returns dictionary with the settings."""
    all_entries = [
        (cart_mass_entry, 'Cart mass'),
        (pendulum_mass_entry, 'Pendulum mass'),
        (pendulum_length_entry, 'Pendulum length'),
        (cart_position_entry, 'Initial cart position'),
        (cart_velocity_entry, 'Initial cart velocity'),
        (pendulum_position_entry, 'Initial pendulum position'),
        (pendulum_velocity_entry, 'Initial pendulum velocity'),
        (amplitude_entry, 'Forcing amplitude'),
        (frequency_entry, 'Forcing frequency'),
        (phase_shift_entry, 'Forcing phase shift'),
        (time_step_entry, 'Time step'),
        (end_time_entry, 'End time')
    ]
    settings = {}
    for entry in all_entries:
        if 'Forcing amplitude' in entry[1]:
            settings['Forcing type'] = forcing_type_variable.get()
        try:
            settings[entry[1]] = float(entry[0].get().strip())
        except ValueError:
            settings[entry[1]] = entry[0].get().strip()
    settings['Timed simulation'] = end_time_boolean.get()
    return settings


def save_inputs_to_text(settings):
    """Saves given inputs to .txt file."""
    written_output = ''
    for setting, value in settings.items():
        written_output = written_output + setting + ": " + str(value) + '\n'
    with open("cart_pendulum_simulation_settings.txt", 'w') as file:
        file.write(written_output)


def load_inputs_from_text():
    all_entries = [
        (cart_mass_entry, 'Cart mass'),
        (pendulum_mass_entry, 'Pendulum mass'),
        (pendulum_length_entry, 'Pendulum length'),
        (cart_position_entry, 'Initial cart position'),
        (cart_velocity_entry, 'Initial cart velocity'),
        (pendulum_position_entry, 'Initial pendulum position'),
        (pendulum_velocity_entry, 'Initial pendulum velocity'),
        (amplitude_entry, 'Forcing amplitude'),
        (frequency_entry, 'Forcing frequency'),
        (phase_shift_entry, 'Forcing phase shift'),
        (time_step_entry, 'Time step'),
        (end_time_entry, 'End time')
    ]
    try:
        with open('cart_pendulum_simulation_settings.txt', 'r') as file:
            text_from_file = file.read()
        for input in all_entries:
            if input[1] in text_from_file:
                input[0].insert(0, re.search(input[1] + ':(.*)\n', text_from_file).group(1).strip())
        if 'Forcing type: ' in text_from_file:
            if re.search('Forcing type:(.*)\n', text_from_file).group(1).lower().strip() == 'none':
                forcing_type_variable.set('None')
                display_forcing_settings()
        if 'Timed simulation: ' in text_from_file:
            if re.search('Timed simulation:(.*)\n', text_from_file).group(1).lower().strip() == 'false':
                end_time_boolean.set(False)
                enable_disable_end_time()
    except FileNotFoundError:
        pass


load_inputs_from_text()

# Turtle Canvas
canvas = tk.Canvas(root, width=800, height=800)
canvas.grid(row=0, column=4, rowspan=6)

# Thread transmitter
transmitter = ThreadTransmitter()
until_button_pushed = threading.Event()


def start_simulator(valid):
    if valid:
        Simulator(get_settings_from_entries(), canvas, transmitter, until_button_pushed)
    else:
        Simulator(
            {'Pendulum length': 0.4, 'Initial cart position': 0, 'Initial pendulum position': 0},
            canvas, transmitter, until_button_pushed
        )


valid, _ = verify_inputs()
thread = threading.Thread(target=start_simulator, args=(valid,))
thread.start()
if valid:
    run_button.config(state='normal')
    apply()
else:
    pass


def close_command():
    until_button_pushed.set()
    transmitter.send(('close', None))
    root.quit()


root.protocol('WM_DELETE_WINDOW', close_command)
root.resizable(False, False)
root.mainloop()
