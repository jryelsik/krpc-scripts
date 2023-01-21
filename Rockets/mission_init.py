from dataclasses import dataclass, field
import yaml

with open('Rockets/mission_config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

@dataclass
class MissionParameters():
    mission_type: str = config['MissionParams']['mission_type']
    countdown_time: int = config['MissionParams']['countdown_time']
    clamp_release_time: int = config['MissionParams']['clamp_release_time']
    roll_flag: bool = config['MissionParams']['roll_flag']
    gravity_turn_flag: bool = config['MissionParams']['gravity_turn_flag']
    landing_flag: bool = config['MissionParams']['landing_flag']
    side_boosters_seperated: bool = config['MissionParams']['side_boosters_seperated']
    main_booster_seperated: bool = config['MissionParams']['main_booster_seperated']
    payload_booster_seperated: bool = config['MissionParams']['payload_booster_seperated']
    fairing_jettison: bool = config['MissionParams']['fairing_jettison']
    target_apoapsis: int = config['MissionParams']['target_apoapsis']
    target_pitch: int = config['MissionParams']['target_pitch']
    target_heading: int = config['MissionParams']['target_heading']
    target_roll: int = config['MissionParams']['target_roll']
    turn_angle: int = config['MissionParams']['turn_angle']
    turn_start_altitude: int = config['MissionParams']['turn_start_altitude']
    turn_end_altitude: int = config['MissionParams']['turn_end_altitude']
    parachute_altitude: int = config['MissionParams']['parachute_altitude']
    warp_flag: bool = config['MissionParams']['warp_flag']

@dataclass
class VesselParameters():
    srb_flag: bool = config['VesselParams']['srb_flag']
    fairing_flag: bool = config['VesselParams']['fairing_flag']
    srb_stage: int = config['VesselParams']['srb_stage']
    first_decouple_stage: int = config['VesselParams']['first_decouple_stage']
    second_decouple_stage: int = config['VesselParams']['second_decouple_stage']
    third_decouple_stage: int = config['VesselParams']['third_decouple_stage']

@dataclass
class VesselStats():
    vessel_name: str
    vessel_type: str
    vessel_mass: int = 0
    vessel_liftoff_thrust: int = 0
    vessel_liftoff_isp: int = 0

    # Determines the number of launch clamps attached to the vessel 
    # and returns the total weight of all launch clamps
    def launch_clamp_weight(vessel):
        clamp_weight = 100 #kg or 0.1t
        total_clamp_weight = 0
        for i in range(len(vessel.parts.with_title("TT18-A Launch Stability Enhancer"))):
            total_clamp_weight += clamp_weight
        return total_clamp_weight

    def total_vessel_mass(vessel):
        return vessel.mass + VesselStats.launch_clamp_weight(vessel) # in kg

@dataclass
class FlightStats():
    max_alt: list[int] = field(default_factory=list)
    max_ap: list[int] = field(default_factory=list)
    max_vel: list[int] = field(default_factory=list)
    max_g: list[int] = field(default_factory=list)   
    start_time: int = 0
    end_time: int = 0
    total_mission_time: int = 0 
    touchdown_speed: int = 0

class Telemetry():
    def __init__(self, conn, vessel):
        self.surface_altitude = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'surface_altitude')
        self.altitude = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'mean_altitude')
        self.apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
        self.velocity = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
        self.vertical_vel = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'vertical_speed')
        self.periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')

class LaunchVehicle():
    def __init__(self, conn, vessel, vessel_params):
        self.first_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=vessel_params.first_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.second_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=vessel_params.second_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.third_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=vessel_params.third_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.srb_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=vessel_params.srb_stage, 
                                                cumulative=False).amount, 
                                                'SolidFuel')