from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.gcode.printer_library.singletool.base_settings as base_settings

def set_up(user_overrides: dict):
    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {
        'primer': 'front_lines_then_xy',
        'extrusion_width': 0.42,
        'nozzle_temp': 215,
        'bed_temp': 60,
        'travel_speed': 12000,
        }
    
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(text='; Time to print!!!!!\n; GCode created with FullControl'))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; START OF STARTING PROCEDURE\n;-----\n'))

    # Heat up the bed
    starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))

    # Home axes
    starting_procedure_steps.append(PrinterCommand(id='home'))

    # Move forward to avoid binder clips
    starting_procedure_steps.append(Point(y=50, z=0.3))

    # Heat up the nozzle
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=False))

    # Turn on part cooling fan
    starting_procedure_steps.append(Fan(speed_percent=initialization_data["fan_percent"]))

    # Wait for the nozzle to heat up
    starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))

    # I don't know if the M2 can use this yet
    # Set print speed
    starting_procedure_steps.append(ManualGcode(text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    # Set material flow
    starting_procedure_steps.append(ManualGcode(text='M221 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))

    # Zero extruder
    starting_procedure_steps.append(ManualGcode(text='G92 E0 ; zero extruder'))

    # Enable extruder
    starting_procedure_steps.append(Extruder(on=True))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='M104 S0 ; turn off extruder'))
    ending_procedure_steps.append(ManualGcode(text='M140 S0 ; turn off bed'))
    ending_procedure_steps.append(ManualGcode(text='G91 ; relative positioning'))
    ending_procedure_steps.append(ManualGcode(text='G1 Z10 ; lift Z-axis 10mm'))
    ending_procedure_steps.append(ManualGcode(text='G90 ; absolute positioning'))
    ending_procedure_steps.append(ManualGcode(text='G28 X'))
    ending_procedure_steps.append(ManualGcode(text='M84 ; disable motors'))

    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
