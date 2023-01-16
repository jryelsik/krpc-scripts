import yaml
from mission_init import MissionParameters as mp, VesselParameters as vp

with open('Rockets/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def setup_MP():
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
    return mission_params

def setup_VP():
    vessel_params = vp(srb_flag = config['VesselParams']['srb_flag'],
                                                fairing_flag = config['VesselParams']['fairing_flag'],
                                                srb_stage = config['VesselParams']['srb_stage'],
                                                first_decouple_stage = config['VesselParams']['first_decouple_stage'],
                                                second_decouple_stage = config['VesselParams']['second_decouple_stage'],
                                                third_decouple_stage = config['VesselParams']['third_decouple_stage'])

    return vessel_params