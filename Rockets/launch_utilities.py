import krpc
import time

def initialize():
    conn = create_instance()
    vessel = initialize_active_vessel(conn)
    return conn, vessel

def create_instance():
    return krpc.connect(name='Launch')

def initialize_active_vessel(conn):
    return conn.space_center.active_vessel

def countdown_timer(mission_params):
    for countdown in range(mission_params.countdown_time,0,-1):
        if countdown % mission_params.countdown_time == 0:
            print("T - %d" % int(countdown))
        elif countdown < mission_params.countdown_time:
            print("T - %d" % int(countdown))
        time.sleep(1)
    
def throttle_from_twr(vessel, twr_desired):
    m0 =  vessel.mass
    g = vessel.orbit.body.surface_gravity
    ### twr = thrust/(m0*g)
    ### thrust = twr*m0*g
    return twr_desired*m0*g/(vessel.max_thrust)

def twr_altitude_control(vessel, telem):
        if telem.altitude() < 2500:
            vessel.control.throttle = throttle_from_twr(vessel, 1.3)
        elif telem.altitude() >= 2500 and telem.altitude() < 12000:
            vessel.control.throttle = throttle_from_twr(vessel, 1.5)
        elif telem.altitude() >= 12000:
            vessel.control.throttle = throttle_from_twr(vessel, 1.7)

def roll_program(vessel, mission_params):
    # Roll Program
    print("\nRoll Program Initiated")
    vessel.auto_pilot.target_heading = mission_params.target_heading
    vessel.auto_pilot.wait()
    print("Roll Complete")
    time.sleep(0.5)
    print("Entering Ascent Profile")

def gravity_turn(vessel, telem, mission_params):
    turn_angle = 0
    if telem.altitude() > mission_params.turn_start_altitude and telem.altitude() < mission_params.turn_end_altitude and vessel.flight().pitch > 45:
        frac = ((telem.altitude() - mission_params.turn_start_altitude) /
                (mission_params.turn_end_altitude - mission_params.turn_start_altitude))
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)

def side_boosters_sep(vessel, side_booster_fuel, side_boosters_seperated):
    # Separate side boosters when finished    
    if side_booster_fuel() < 2:
        vessel.parts.with_tag('CE1')[0].engine.active = True # Start main engine before seperating side boosters
        print("Main Engine Start")
        time.sleep(1.5)   
        vessel.control.activate_next_stage() # Seperate side boosters
        side_boosters_seperated = True
        print('BECO')
    return side_boosters_seperated

def main_boosters_sep(vessel, main_booster_fuel, main_booster_seperated):
    # Separate main boosters when finished
    if main_booster_fuel() < 0.1:
        print("Main Engine Shutdown")
        vessel.control.throttle = 0
        time.sleep(1)
        vessel.control.activate_next_stage()
        main_booster_seperated = True
        print('MECO')
    return main_booster_seperated

def payload_boosters_sep(vessel, payload_booster_fuel, payload_booster_seperated):
    # Separate payload boosters when finished
    if payload_booster_fuel() < 0.1:
        print("Payload Engine Shutdown")
        vessel.control.throttle = 0
        time.sleep(1)
        vessel.control.activate_next_stage()
        payload_booster_seperated = True
        print('PECO')
    return payload_booster_seperated

def fairing_seperation(vessel, fairing_jettison):
    #vessel.control.throttle = throttle_from_twr(vessel, 1.25)
    print("Direction Set to Prograde in Preperation for Fairing Jettison")
    vessel.auto_pilot.target_direction = vessel.flight().prograde
    vessel.auto_pilot.wait()    
    print("Target Direction Reached")
    print("Standby for Fairing Jettison")
    time.sleep(1)
    vessel.parts.with_tag('F1')[0].fairing.jettison()
    print("Fairing Jettison Confirmed")
    fairing_jettison = True
    time.sleep(1)
    return fairing_jettison

def universal_time(conn):
    return round(conn.space_center.ut, 2)

def mission_time(vessel):
    return round(vessel.met, 2)

def ut_format(x):
    seconds = x%60
    minutes = (x//60)%60
    hours = (x//3600)%6
    days = (x//21600)%426.08
    years = (x//9203328)

    return (f'Y{years+1:.0f}:D{days+1:.0f}:{hours:.0f}h:{minutes:.0f}m:{seconds:.0f}s UT')

def met_format(x, mission_params):
    x += mission_params.clamp_release_time
    seconds = x%60
    minutes = (x//60)%60
    hours = (x//3600)%6
    days = (x//21600)%426.08
    years = (x//9203328)

    return (f'T + {years:.0f}y:{days:.0f}d:{hours:.0f}h:{minutes:.0f}m:{seconds:.01f}s MET')