from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.gcode.printer_library.singletool.base_settings as base_settings

def set_up(user_overrides: dict):
    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {
        'primer': 'front_lines_then_xy',
        # 0.6mm is the default Extrusion Width for the 0.50mm nozzle
        'extrusion_width': 0.6,
        'print_speed': 1000,
        'nozzle_temp': 215,
        'bed_temp': 60,
        'travel_speed': 18000
    }
    
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(text='; Time to print!!!!!\n; GCode created with FullControl'))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; START OF STARTING PROCEDURE\n;-----\n'))
    
    starting_procedure_steps.append(ManualGcode(text='M106 P2 S255 ; turn on exhaust fan'))

    # Manually set Ultra One Rev.0 / Rev.1 bed temperature
    starting_procedure_steps.append(ManualGcode (text='M140 P0 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P1 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P2 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P3 S' + str(initialization_data["bed_temp"])))
    
    # Wait for bed temperature to reach target temperature
    starting_procedure_steps.append(ManualGcode (text='M190 P0 S' + str(initialization_data["bed_temp"])))

    # Home all axes 
    starting_procedure_steps.append(PrinterCommand(id='home')) #good

    # Fast home (may damage kapton tape on bed)
    #starting_procedure_steps.append(ManualGcode (text='G28 XY'))
    #starting_procedure_steps.append(ManualGcode (text='G28 Z'))
                                
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))

    # Enable Tool 0 fan 
    starting_procedure_steps.append(ManualGcode(text='M106 P0 S' + str(initialization_data["fan_percent"]) + ' ; turn on tool_0 part cooling fan'))    

    # Heat up Tool_0 hotend
    starting_procedure_steps.append(ManualGcode (text='M104 P0 S' + str(initialization_data["nozzle_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M109 P0 S' + str(initialization_data["nozzle_temp"])))

    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 D0 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage'))
    
    starting_procedure_steps.append(Printer(travel_speed=200))
    starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
    
    # Disable software endstops
    starting_procedure_steps.append(ManualGcode (text='G92 E0'))
    starting_procedure_steps.append(ManualGcode (text='M564 S0'))

    # Move? but why? 
    starting_procedure_steps.append(Point(x=25.0, y=25.0, z=0.3))

    #turn on for the purge script
    starting_procedure_steps.append(Extruder(on=True))    
    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ending_procedure_steps = []
    ending_procedure_steps.append(ManualGcode(text='\n;-----\n; START OF ENDING PROCEDURE\n;-----'))
    ending_procedure_steps.append(ManualGcode(text='M106 P2 S0 ; turn off exhaust fan'))

    ending_procedure_steps.append(ManualGcode(text=';'))
    ending_procedure_steps.append(ManualGcode(text='M104 S0 ; turn off extruder'))
    ending_procedure_steps.append(ManualGcode(text='M104 S0 T0 ; turn off extruder'))
    ending_procedure_steps.append(ManualGcode(text='M104 S0 T1; turn off extruder'))
    ending_procedure_steps.append(ManualGcode(text='M140 P0 S0 ; turn off bed'))
    ending_procedure_steps.append(ManualGcode(text='M140 P1 S0 ; turn off bed'))
    ending_procedure_steps.append(ManualGcode(text='M140 P2 S0 ; turn off bed'))
    ending_procedure_steps.append(ManualGcode(text='M140 P3 S0 ; turn off bed'))
    ending_procedure_steps.append(ManualGcode(text='M106 S0 ; turn off cooling fan'))
    ending_procedure_steps.append(ManualGcode(text='G91 ; relative mode'))
    ending_procedure_steps.append(ManualGcode(text='G1 Z20 ; move Z down 20mm'))
    ending_procedure_steps.append(ManualGcode(text='G90;  absolute mode'))
    ending_procedure_steps.append(ManualGcode(text=';'))
    
    ending_procedure_steps.append(ManualGcode(text='G28 XY ; home tool/s'))
    ending_procedure_steps.append(ManualGcode(text='M502 ; set to firmware default values'))
    ending_procedure_steps.append(ManualGcode(text='T0 ; defualt tool should always be T0'))


    initialization_data['starting_procedure_steps'] = starting_procedure_steps
    initialization_data['ending_procedure_steps'] = ending_procedure_steps

    return initialization_data
