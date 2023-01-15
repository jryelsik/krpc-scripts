import collections
import launch_utilities as utils
import callbacks as cb
import mission_params_telem as mpt
import mission_logging as log
from launch import launch
from landing import landing
collections.Iterable = collections.abc.Iterable

def main():
    conn, vessel = utils.initialize()
    flight_stats = mpt.FlightStats(vessel_mass = vessel.mass)
    mission_params = mpt.MissionParameters(mission_type = "Test Flight", # [Contract, Research, Test Flight]
                                            gravity_turn = False,
                                            srb_flag = True,
                                            landing_flag = True,
                                            countdown_time = 0,
                                            first_decouple_stage = 0,
                                            second_decouple_stage = 0,
                                            third_decouple_stage = 0,
                                            srb_stage = 0,
                                            target_apoapsis = None,
                                            target_pitch = 90,
                                            target_heading = 90,
                                            target_roll = None,
                                            turn_angle = None,
                                            turn_start_altitude = None,
                                            turn_end_altitude = None,
                                            parachute_altitude = 380,
                                            side_boosters_seperated = False,
                                            main_booster_seperated = False,
                                            payload_booster_seperated = False,
                                            fairing_jettison = False,
                                            roll = False,
                                            clamp_release_time = 0.5)

    # Start callbacks
    cb.start_callbacks(vessel, conn, flight_stats)

    # Mission Start
    vessel = launch(conn, vessel, mission_params, flight_stats)

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
    flight_stats.end_time = utils.universal_time(conn)
    flight_stats.total_mission_time = utils.mission_time(vessel)

    # Generate mission logs
    log.generate_log_file(conn, vessel, mission_params, flight_stats)

if __name__ == "__main__":
    main()
    print("DONE")
    quit()
