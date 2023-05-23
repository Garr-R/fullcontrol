from fullcontrol.gcode import Point, Printer, Extruder, ManualGcode, PrinterCommand, GcodeComment, Buildplate, Hotend, Fan, StationaryExtrusion
import fullcontrol.gcode.printer_library.singletool.base_settings as base_settings


def set_up(user_overrides: dict):
    ''' DO THIS
    '''

    # overrides for this specific printer relative those defined in base_settings.py
    printer_overrides = {}
    # update default initialization settings with printer-specific overrides and user-defined overrides
    initialization_data = {**base_settings.default_initial_settings, **printer_overrides}
    initialization_data = {**initialization_data, **user_overrides}

    starting_procedure_steps = []
    starting_procedure_steps.append(ManualGcode(
        text='; Time to print!!!!!\n; GCode created with FullControl - tell us what you\'re printing!\n; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok \n'))
    starting_procedure_steps.append(ManualGcode(text=';-----\n; START OF STARTING PROCEDURE\n;-----\n'))
    starting_procedure_steps.append(ManualGcode(text='M106 P2 S255 ; turn on exhaust fan'))

    #starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=False)) 
    #starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=False))
    #starting_procedure_steps.append(Buildplate(temp=initialization_data["bed_temp"], wait=True))
    #starting_procedure_steps.append(Hotend(temp=initialization_data["nozzle_temp"], wait=True))

    # Manually set Ultra One Rev.0 / Rev.1 bed temperature
    starting_procedure_steps.append(ManualGcode (text='M140 P0 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P1 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P2 S' + str(initialization_data["bed_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M140 P3 S' + str(initialization_data["bed_temp"])))
    
    # Wait for bed temperature to reach target temperature
    starting_procedure_steps.append(ManualGcode (text='M190 P0 S' + str(initialization_data["bed_temp"])))

    # Home all axes 
    starting_procedure_steps.append(PrinterCommand(id='home')) #good
    #starting_procedure_steps.append(ManualGcode (text='G28 XY'))
    #starting_procedure_steps.append(ManualGcode (text='G28 Z'))
                                
    starting_procedure_steps.append(PrinterCommand(id='absolute_coords'))
    starting_procedure_steps.append(PrinterCommand(id='units_mm'))

    # Ultra One doesn't use relative extrusion - commented out
    #starting_procedure_steps.append(Extruder(relative_gcode=initialization_data["relative_e"]))

    # Enable Tool 0 fan 
    starting_procedure_steps.append(ManualGcode(text='M106 P0 S255 ; turn on tool_0 part cooling fan'))    
    
    # Enable Tool 1 fan - Not using Tool_1
    #starting_procedure_steps.append(ManualGcode(text='M106 P1 S255 ; turn on part cooling fan'))

    # Heat up Tool_0 hotend
    starting_procedure_steps.append(ManualGcode (text='M104 P0 S' + str(initialization_data["nozzle_temp"])))
    starting_procedure_steps.append(ManualGcode (text='M109 P0 S' + str(initialization_data["nozzle_temp"])))

    # Heat up Tool_1 hotend - Not using Tool_1
    #starting_procedure_steps.append(ManualGcode (text='M104 P1 S' + str(initialization_data["nozzle_temp"])))
    #starting_procedure_steps.append(ManualGcode (text='M109 P1 S' + str(initialization_data["nozzle_temp"])))

    starting_procedure_steps.append(ManualGcode(
        text='M220 S' + str(initialization_data["print_speed_percent"])+' ; set speed factor override percentage'))
    starting_procedure_steps.append(ManualGcode(
        text='M221 D0 S' + str(initialization_data["material_flow_percent"])+' ; set extrude factor override percentage')) # D0 is for Tool_0
    #starting_procedure_steps.append(Extruder(on=False))

    # wiggle starting position
    #starting_procedure_steps.append(Point(x=203, y=127, z=10))
    
    starting_procedure_steps.append(Printer(travel_speed=200))
    starting_procedure_steps.append(Printer(travel_speed=initialization_data["travel_speed"]))
    
    # Disable software endstops
    starting_procedure_steps.append(ManualGcode (text='G92 E0'))
    starting_procedure_steps.append(ManualGcode (text='M564 S0')) 
    starting_procedure_steps.append(Point(x=25.0, y=25.0, z=0.3))

    #turn on for the purge script
    starting_procedure_steps.append(Extruder(on=True))    

    starting_procedure_steps.append(ManualGcode(text=';-----\n; END OF STARTING PROCEDURE\n;-----\n'))

    # move the home command in the start procedure to be after temperatures (to work with bed levelling)

    # commented this out, doing it in the starting procedure steps
    #del starting_procedure_steps[1]
    #starting_procedure_steps.insert(5, PrinterCommand(id='home'))
    #tarting_procedure_steps.insert(6, GcodeComment(end_of_previous_line_text='; including mesh bed level'))





    #ending scripts are all set 
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
