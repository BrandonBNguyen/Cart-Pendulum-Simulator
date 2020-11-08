import tkinter as tk
from tkinter import messagebox
import re


class MainWindow:

    def __init__(self):
        # Create Tkinter root window
        self.root = tk.Tk()
        self.root.title("Cart Pendulum Simulation")

        # Create and place LabelFrame for each section
        self.frame = {
            'System Properties': tk.LabelFrame(self.root, text="System Properties"),
            'Initial Conditions': tk.LabelFrame(self.root, text="Initial Conditions"),
            'Cart Forcing': tk.LabelFrame(self.root, text="Cart Forcing", height=300),
            'Simulation Properties': tk.LabelFrame(self.root, text="Simulation Properties")
        }

        # Create all input elements on page
        self.input_elements = {
            'Cart mass': {
                'label': tk.Label(self.frame['System Properties'], text="Cart Mass: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['System Properties'], width=9),
                'units': tk.Label(self.frame['System Properties'], text="[kg]", width=6, anchor='w'),
                'expected': '>0'
            },
            'Pendulum mass': {
                'label': tk.Label(self.frame['System Properties'], text="Pendulum Mass: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['System Properties'], width=9),
                'units': tk.Label(self.frame['System Properties'], text="[kg]", width=6, anchor='w'),
                'expected': '>0'
            },
            'Pendulum length': {
                'label': tk.Label(self.frame['System Properties'], text="Pendulum Length: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['System Properties'], width=9),
                'units': tk.Label(self.frame['System Properties'], text="[m]", width=6, anchor='w'),
                'expected': '>0'
            },
            'Cart position': {
                'label': tk.Label(self.frame['Initial Conditions'], text="Cart Position: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Initial Conditions'], width=9),
                'units': tk.Label(self.frame['Initial Conditions'], text="[m]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Cart velocity': {
                'label': tk.Label(self.frame['Initial Conditions'], text="Cart Velocity: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Initial Conditions'], width=9),
                'units': tk.Label(self.frame['Initial Conditions'], text="[m/s]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Pendulum position': {
                'label': tk.Label(self.frame['Initial Conditions'], text="Pendulum Position: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Initial Conditions'], width=9),
                'units': tk.Label(self.frame['Initial Conditions'], text="[deg]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Pendulum velocity': {
                'label': tk.Label(self.frame['Initial Conditions'], text="Pendulum Velocity: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Initial Conditions'], width=9),
                'units': tk.Label(self.frame['Initial Conditions'], text="[deg/s]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Forcing amplitude': {
                'label': tk.Label(self.frame['Cart Forcing'], text="Amplitude: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Cart Forcing'], width=9),
                'units': tk.Label(self.frame['Cart Forcing'], text="[N]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Forcing frequency': {
                'label': tk.Label(self.frame['Cart Forcing'], text="Frequency: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Cart Forcing'], width=9),
                'units': tk.Label(self.frame['Cart Forcing'], text="[Hz]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Forcing phase shift': {
                'label': tk.Label(self.frame['Cart Forcing'], text="Phase Shift: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Cart Forcing'], width=9),
                'units': tk.Label(self.frame['Cart Forcing'], text="[deg]", width=6, anchor='w'),
                'expected': 'any'
            },
            'Time step': {
                'label': tk.Label(self.frame['Simulation Properties'], text="Time Step: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Simulation Properties'], width=9),
                'units': tk.Label(self.frame['Simulation Properties'], text="[s]", width=6, anchor='w'),
                'expected': '>0'
            },
            'End time': {
                'label': tk.Label(self.frame['Simulation Properties'], text="End Time: ", width=16, anchor='e'),
                'entry': tk.Entry(self.frame['Simulation Properties'], width=9),
                'units': tk.Label(self.frame['Simulation Properties'], text="[s]", width=6, anchor='w'),
                'expected': '>0'
            }
        }

        # Create forcing type dropdown
        forcing_type_options = ['None', 'Sinusoidal']
        self.forcing_type_variable = tk.StringVar()
        self.forcing_type_variable.set(forcing_type_options[1])
        forcing_type_label = tk.Label(self.frame['Cart Forcing'], text="Forcing Type: ", width=16, anchor='e')
        forcing_type_select = tk.OptionMenu(self.frame['Cart Forcing'], self.forcing_type_variable,
                                            *forcing_type_options, command=self.display_forcing_settings)
        forcing_type_select.config(width=8)

        # Create end time checkbox
        self.end_time_boolean = tk.BooleanVar()
        self.end_time_boolean.set(True)
        end_time_checkbox = tk.Checkbutton(self.frame['Simulation Properties'], text="Simulate only up to end time.",
                                           variable=self.end_time_boolean, command=self.enable_disable_end_time)

        # Create buttons
        self.button_apply = tk.Button(self.root, text="Apply", command=self.apply, pady=4, padx=7)
        self.button_run = tk.Button(self.root, text="Run", command=self.run, pady=4, padx=7, state='disabled')
        self.button_pause = tk.Button(self.root, text="Pause", command=self.pause, pady=4, padx=7, state='disabled')
        self.button_stop = tk.Button(self.root, text="Stop", command=self.stop, pady=4, padx=7, state='disabled')

        # Place system properties elements
        self.frame['System Properties'].grid(row=0, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
        self.input_elements['Cart mass']['label'].grid(row=0, column=0, pady=4)
        self.input_elements['Cart mass']['entry'].grid(row=0, column=1)
        self.input_elements['Cart mass']['units'].grid(row=0, column=2, padx=2)
        self.input_elements['Pendulum mass']['label'].grid(row=1, column=0, pady=4)
        self.input_elements['Pendulum mass']['entry'].grid(row=1, column=1)
        self.input_elements['Pendulum mass']['units'].grid(row=1, column=2, padx=2)
        self.input_elements['Pendulum length']['label'].grid(row=2, column=0, pady=4)
        self.input_elements['Pendulum length']['entry'].grid(row=2, column=1)
        self.input_elements['Pendulum length']['units'].grid(row=2, column=2, padx=2)

        # Place initial conditions elements
        self.frame['Initial Conditions'].grid(row=1, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
        self.input_elements['Cart position']['label'].grid(row=0, column=0, pady=4)
        self.input_elements['Cart position']['entry'].grid(row=0, column=1)
        self.input_elements['Cart position']['units'].grid(row=0, column=2, padx=2)
        self.input_elements['Cart velocity']['label'].grid(row=1, column=0, pady=4)
        self.input_elements['Cart velocity']['entry'].grid(row=1, column=1)
        self.input_elements['Cart velocity']['units'].grid(row=1, column=2, padx=2)
        self.input_elements['Pendulum position']['label'].grid(row=2, column=0, pady=4)
        self.input_elements['Pendulum position']['entry'].grid(row=2, column=1)
        self.input_elements['Pendulum position']['units'].grid(row=2, column=2, padx=2)
        self.input_elements['Pendulum velocity']['label'].grid(row=3, column=0, pady=4)
        self.input_elements['Pendulum velocity']['entry'].grid(row=3, column=1)
        self.input_elements['Pendulum velocity']['units'].grid(row=3, column=2, padx=2)

        # Place cart forcing elements
        self.frame['Cart Forcing'].grid(row=2, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
        forcing_type_label.grid(row=0, column=0, pady=4, sticky='E')
        forcing_type_select.grid(row=0, column=1, columnspan=2, sticky='W')
        self.input_elements['Forcing amplitude']['label'].grid(row=1, column=0, pady=4, sticky='E')
        self.input_elements['Forcing amplitude']['entry'].grid(row=1, column=1)
        self.input_elements['Forcing amplitude']['units'].grid(row=1, column=2, padx=2)
        self.input_elements['Forcing frequency']['label'].grid(row=2, column=0, pady=4, sticky='E')
        self.input_elements['Forcing frequency']['entry'].grid(row=2, column=1)
        self.input_elements['Forcing frequency']['units'].grid(row=2, column=2, padx=2)
        self.input_elements['Forcing phase shift']['label'].grid(row=3, column=0, pady=4, sticky='E')
        self.input_elements['Forcing phase shift']['entry'].grid(row=3, column=1)
        self.input_elements['Forcing phase shift']['units'].grid(row=3, column=2, padx=2)

        # Place simulation properties elements
        self.frame['Simulation Properties'].grid(row=3, column=0, columnspan=4, padx=10, pady=7, sticky='EW')
        self.input_elements['Time step']['label'].grid(row=0, column=0, pady=4)
        self.input_elements['Time step']['entry'].grid(row=0, column=1)
        self.input_elements['Time step']['units'].grid(row=0, column=2, padx=2)
        self.input_elements['End time']['label'].grid(row=1, column=0, pady=4)
        self.input_elements['End time']['entry'].grid(row=1, column=1)
        self.input_elements['End time']['units'].grid(row=1, column=2, padx=2)
        end_time_checkbox.grid(row=2, column=0, columnspan=3)

        # Place buttons
        self.button_apply.grid(row=4, column=0, pady=5)
        self.button_run.grid(row=4, column=1)
        self.button_pause.grid(row=4, column=2)
        self.button_stop.grid(row=4, column=3)

        # Create and place Turtle canvas
        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.grid(row=0, column=4, rowspan=6)

        # Load inputs from file if it exists. If inputs are valid, apply settings.
        self.load_inputs_from_text()
        if self.verify_inputs(False):
            self.apply()

    def display_forcing_settings(self, *args):
        if self.forcing_type_variable.get() == 'Sinusoidal':
            # If forcing type is set to 'Sinusoidal', display forcing inputs
            self.input_elements['Forcing amplitude']['label'].grid(row=1, column=0, pady=4, sticky='E')
            self.input_elements['Forcing amplitude']['entry'].grid(row=1, column=1)
            self.input_elements['Forcing amplitude']['units'].grid(row=1, column=2, padx=2)
            self.input_elements['Forcing frequency']['label'].grid(row=2, column=0, pady=4, sticky='E')
            self.input_elements['Forcing frequency']['entry'].grid(row=2, column=1)
            self.input_elements['Forcing frequency']['units'].grid(row=2, column=2, padx=2)
            self.input_elements['Forcing phase shift']['label'].grid(row=3, column=0, pady=4, sticky='E')
            self.input_elements['Forcing phase shift']['entry'].grid(row=3, column=1)
            self.input_elements['Forcing phase shift']['units'].grid(row=3, column=2, padx=2)
        elif self.forcing_type_variable.get() == 'None':
            # If forcing type is set to 'None', remove forcing inputs
            self.input_elements['Forcing amplitude']['label'].grid_forget()
            self.input_elements['Forcing amplitude']['entry'].grid_forget()
            self.input_elements['Forcing amplitude']['units'].grid_forget()
            self.input_elements['Forcing frequency']['label'].grid_forget()
            self.input_elements['Forcing frequency']['entry'].grid_forget()
            self.input_elements['Forcing frequency']['units'].grid_forget()
            self.input_elements['Forcing phase shift']['label'].grid_forget()
            self.input_elements['Forcing phase shift']['entry'].grid_forget()
            self.input_elements['Forcing phase shift']['units'].grid_forget()

    def enable_disable_end_time(self):
        if self.end_time_boolean.get():
            # Enable 'End time' entry if 'stop at end time' checkbox is checked.
            self.input_elements['End time']['entry'].config(state='normal')
        else:
            # Disable 'End time' entry if 'stop at end time' checkbox is not checked.
            self.input_elements['End time']['entry'].config(state='disabled')

    def get_settings_from_entries(self):
        settings = {}
        for input_type, input_dict in self.input_elements.items():
            if 'Forcing amplitude' in input_type:  # Put 'Forcing type' before 'Forcing amplitude' in settings
                settings['Forcing type'] = self.forcing_type_variable.get()
            elif 'End time' in input_type:  # Put 'Timed simulation' before 'End time' in dictionary
                settings['Timed simulation'] = self.end_time_boolean.get()
            try:
                settings[input_type] = float(input_dict['entry'].get())
            except ValueError:
                settings[input_type] = input_dict['entry'].get()
        return settings

    def verify_inputs(self, return_error_messages=True):
        valid = True
        error_messages = []
        for input_type, input_dict in self.input_elements.items():
            value = input_dict['entry'].get().strip()
            if len(value) == 0:
                if not (
                        ('Forcing' in input_type and self.forcing_type_variable.get() == 'None')
                        # Permit forcing values to be empty if dropdown is set to 'None'
                        or ('End time' in input_type and not self.end_time_boolean.get())
                        # Permit 'End time' to be empty if 'stop at end time' checkbox is not checked.
                ):
                    valid = False
                    error_messages.append(input_type + ' does not have any value')
            else:
                try:
                    float(value)
                except ValueError:
                    valid = False
                    error_messages.append(input_type + ' does not have a valid numeric value')
                if float(value) < 0 and input_dict['expected'] == '>0':
                    valid = False
                    error_messages.append(input_type + ' cannot be less than or equal to 0')
        if return_error_messages:
            return valid, error_messages
        else:
            return valid

    @staticmethod
    def save_inputs_to_text(settings):
        """Saves given inputs to 'cart_pendulum_simulation_settings.txt'."""
        written_output = ''
        for setting, value in settings.items():
            written_output = written_output + setting + ": " + str(value) + '\n'
        with open("cart_pendulum_simulation_settings.txt", 'w') as file:
            file.write(written_output)

    def load_inputs_from_text(self):
        """Loads inputs from 'cart_pendulum_simulation_settings.txt'."""
        try:
            with open('cart_pendulum_simulation_settings.txt', 'r') as file:
                text_from_file = file.read()
            for input_type, input_dict in self.input_elements.items():
                if input_type in text_from_file:
                    input_dict['entry'].insert(0, re.search(input_type + ':(.*)\n', text_from_file).group(1).strip())
            if 'Forcing type:' in text_from_file:
                if re.search('Forcing type:(.*)\n', text_from_file).group(1).lower().strip() == 'none':
                    self.forcing_type_variable.set('None')
                elif re.search('Forcing type:(.*)\n', text_from_file).group(1).lower().strip() == 'sinusoidal':
                    self.forcing_type_variable.set('Sinusoidal')
                self.display_forcing_settings()
            if 'Timed simulation:' in text_from_file:
                if re.search('Timed simulation:(.*)\n', text_from_file).group(1).lower().strip() == 'false':
                    self.end_time_boolean.set(False)
                    self.enable_disable_end_time()
        except FileNotFoundError:
            pass

    def apply(self):
        inputs_valid, error_messages = self.verify_inputs()
        if inputs_valid:
            self.button_apply.config(state='normal')
            self.button_run.config(state='normal')
            self.button_pause.config(state='disabled')
            self.button_stop.config(state='disabled')
            MainWindow.save_inputs_to_text(self.get_settings_from_entries())
            # self.transmitter.send(('apply', self.get_settings_from_entries()))
            # until_button_pushed.set()

        else:
            # Generate error message
            error_message = 'Please fix the following inputs before continuing:\n'
            for error in error_messages:
                error_message = error_message + '\n-' + error
            messagebox.showerror('Invalid Inputs', error_message)

    def run(self):
        self.button_apply.config(state='disabled')
        self.button_run.config(state='disabled')
        self.button_pause.config(state='normal')
        self.button_stop.config(state='normal')
        # transmitter.send(('run', None))
        # until_button_pushed.set()

    def pause(self):
        self.button_apply.config(state='disabled')
        self.button_run.config(state='normal')
        self.button_pause.config(state='disabled')
        self.button_stop.config(state='normal')
        # transmitter.send(('run', None))
        # until_button_pushed.set()

    def stop(self):
        self.button_apply.config(state='normal')
        self.button_run.config(state='normal')
        self.button_pause.config(state='disabled')
        self.button_stop.config(state='disabled')
        # transmitter.send(('stop', None))
        # until_button_pushed.set()

    def get_canvas(self):
        return self.canvas

    def close_command(self):
        return


if __name__ == "__main__":
    new_window = MainWindow()
    new_window.root.mainloop()
