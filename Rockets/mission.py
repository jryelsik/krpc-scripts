import collections
import yaml
from launch_utilities import initialize, universal_time, mission_time
from callbacks import start_callbacks
from mission_logging import generate_log_file
from mission_params_telem import MissionParameters as mp, VesselParameters as vp, FlightStats as fs
from launch import launch
from landing import landing
collections.Iterable = collections.abc.Iterable

with open('Rockets/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def main():
    conn, vessel = initialize()
    flight_stats = fs(vessel_mass = vessel.mass)
    mission_params = mp(mission_type = config['MissionParams']['mission_type'],
                                            countdown_time = config['MissionParams']['countdown_time'],
                                            clamp_release_time = config['MissionParams']['clamp_release_time'],
                                            roll_flag = config['MissionParams']['roll_flag'],
                                            gravity_turn_flag = config['MissionParams']['gravity_turn_flag'],
                                            landing_flag = config['MissionParams']['landing_flag'],
                                            side_boosters_seperated = config['MissionParams']['side_boosters_seperated'],
                                            main_booster_seperated = config['MissionParams']['main_booster_seperated'],
                                            payload_booster_seperated = config['MissionParams']['payload_booster_seperated'],
                                            fairing_jettison = config['MissionParams']['fairing_jettison'],
                                            target_apoapsis = config['MissionParams']['target_apoapsis'],
                                            target_pitch = config['MissionParams']['target_pitch'],
                                            target_heading = config['MissionParams']['target_heading'],
                                            target_roll = config['MissionParams']['target_roll'],
                                            turn_angle = config['MissionParams']['turn_angle'],
                                            turn_start_altitude = config['MissionParams']['turn_start_altitude'],
                                            turn_end_altitude = config['MissionParams']['turn_end_altitude'],
                                            parachute_altitude = config['MissionParams']['parachute_altitude'])
    
    vessel_params = vp(srb_flag = config['VesselParams']['srb_flag'],
                                            fairing_flag = config['VesselParams']['fairing_flag'],
                                            srb_stage = config['VesselParams']['srb_stage'],
                                            first_decouple_stage = config['VesselParams']['first_decouple_stage'],
                                            second_decouple_stage = config['VesselParams']['second_decouple_stage'],
                                            third_decouple_stage = config['VesselParams']['third_decouple_stage'])

    # Start callbacks
    start_callbacks(vessel, conn, flight_stats)

    # Mission Start
    vessel = launch(conn, vessel, mission_params, vessel_params, flight_stats)

    ### Need to unlock tracking station ###
    # TODO: Create orbit profile

    if mission_params.landing_flag:
        # Mission Landing
        vessel = landing(vessel, conn, mission_params, flight_stats)

    # Wait for user input to end mission
    mission_end_input = str(input("Type 'e' and Press Enter to End Mission\n"))
    while mission_end_input != "e":
        pass

    # Record mission end times
    flight_stats.end_time = universal_time(conn)
    flight_stats.total_mission_time = mission_time(vessel)

    # Generate mission logs
    generate_log_file(conn, vessel, mission_params, vessel_params, flight_stats)

if __name__ == "__main__":
    main()
    print("DONE")
    quit()
