import time
import launch_utilities as utils
import mission_params_telem

def launch(conn, vessel, mission_params, flight_stats):
    # Countdown to launch
    utils.countdown_timer(mission_params)
    flight_stats.start_time = utils.universal_time(conn)
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading = 90

    # Booster Ignition
    print("\nBOOSTER IGNITION\n")
    vessel.control.activate_next_stage()
    flight_stats.max_thrust = vessel.available_thrust
    flight_stats.isp = vessel.specific_impulse

    if not mission_params.srb_flag:
        vessel.control.throttle = utils.throttle_from_twr(vessel, 1.5)

    # Release launch clamps
    time.sleep(mission_params.clamp_release_time)
    vessel.control.activate_next_stage() 
    print("LIFTOFF of " + vessel.name)
    time.sleep(1)

    if mission_params.roll:
        print("true")
        # Roll Program
        utils.roll_program(vessel, mission_params)

    if mission_params.gravity_turn:
        print("Targeting altitude of " + str(mission_params.target_apoapsis/1000) + "km")

        # Ascent Profile
        ascent(vessel, conn, mission_params)

    return vessel

def ascent(vessel, conn, mission_params):
    telem = mission_params_telem.Telemetry(conn, vessel)
    resources = mission_params_telem.LaunchVehicle(conn, vessel, mission_params)
    #resources.first_stage_LF
    #resources.second_stage_LF
    #resources.third_stage_LF

    # Main Ascent Loop
    gravity_turn_end = str((mission_params.turn_end_altitude)/1000) + " km"

    print("Gravity Turn End Altitude is " + gravity_turn_end)

    # Ascent profile until 90% target altitude
    while telem.apoapsis() < mission_params.target_apoapsis*0.99:
        utils.twr_altitude_control(vessel, telem)
        # Gravity turn
        utils.gravity_turn(vessel, telem, mission_params)

        # BECO if applicable
        if not mission_params.side_boosters_seperated:
            mission_params.side_boosters_seperated = utils.side_boosters_sep(vessel, resources.first_stage_LF, mission_params.side_boosters_seperated)            
        
        # MECO if applicable
        if not mission_params.main_booster_seperated:
            mission_params.main_booster_seperated = utils.main_boosters_sep(vessel, resources.second_stage_LF, mission_params.main_booster_seperated)
        
    # Decrease throttle when approaching target apoapsis
    print("Approaching target apoapsis")
    print("Engine Throttle Reduced")        
    
    # Ascent profile between 90% target altitude and target altitude
    while telem.apoapsis() >= mission_params.target_apoapsis*0.99:
        vessel.control.throttle = utils.throttle_from_twr(vessel, 1.25)
        # MECO if applicable
        if not mission_params.main_booster_seperated:
            mission_params.main_booster_seperated = utils.main_boosters_sep(vessel, resources.second_stage_LF, mission_params.main_booster_seperated)
        # Wait until target apoapsis is reached
        if telem.apoapsis() >= mission_params.target_apoapsis:
            print('Target apoapsis reached')

            # Main Engine Shutdown
            vessel.control.throttle = 0.0
            print("Main Engine Shutdown")
            if not mission_params.main_booster_seperated:
                mission_params.main_booster_seperated = utils.main_boosters_sep(vessel, resources.second_stage_LF, mission_params.main_booster_seperated)
            break

    # Wait until out of atmosphere
    if telem.altitude() < 50000:
        print('Coasting out of atmosphere')
        while telem.altitude() < 50000:
            pass

    print("RCS Thrusters Enabled")
    vessel.control.rcs = True

    if not mission_params.fairing_jettison:
        mission_params.fairing_jettison = utils.fairing_seperation(vessel, mission_params.fairing_jettison)

    # Pitch Profile
    print("Starting Pitch Maneuver")  
    vessel.auto_pilot.target_pitch = 0
    vessel.auto_pilot.wait()
    print("Target Pitch Reached")
    print("Waiting for Target Altitude of " + str((mission_params.target_apoapsis*0.9)/1000) + " km")

    # Wait until vessel is 90% to target apoapsis
    while telem.altitude() < mission_params.target_apoapsis*0.9:
        if not mission_params.main_booster_seperated:
            mission_params.main_booster_seperated = utils.main_boosters_sep(vessel, resources.second_stage_LF, mission_params.main_booster_seperated)
        pass

    if not mission_params.main_booster_seperated:
        print("Main Engine Restart")
    if not mission_params.payload_booster_seperated:
        print("Payload Booster Start")

    while not mission_params.main_booster_seperated or not mission_params.payload_booster_seperated:
        vessel.control.throttle = utils.throttle_from_twr(vessel, 2.0)
        if telem.apoapsis() > mission_params.target_apoapsis:
            vessel.control.throttle = 0.0
            break

        # MECO or PECO if applicable
        if not mission_params.main_booster_seperated:
            mission_params.main_booster_seperated = utils.main_boosters_sep(vessel, resources.second_stage_LF, mission_params.main_booster_seperated)
        if not mission_params.payload_booster_seperated:
            mission_params.payload_booster_seperated = utils.main_boosters_sep(vessel, resources.third_stage_LF, mission_params.payload_booster_seperated)
        pass

    vessel.auto_pilot.disengage()    
    vessel.control.sas = True
    #vessel.control.set_action_group(1, True) # Deploy relay antennas

    print("Starting Orbit Profile")