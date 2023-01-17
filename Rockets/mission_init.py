from dataclasses import dataclass, field

@dataclass
class MissionParameters():
    mission_type: str
    countdown_time: int
    clamp_release_time: int
    roll_flag: bool
    gravity_turn_flag: bool
    landing_flag: bool
    side_boosters_seperated: bool
    main_booster_seperated: bool
    payload_booster_seperated: bool
    fairing_jettison: bool
    target_apoapsis: int
    target_pitch: int
    target_heading: int
    target_roll: int
    turn_angle: int
    turn_start_altitude: int
    turn_end_altitude: int
    parachute_altitude: int
    warp_flag: bool

@dataclass
class VesselParameters():
    srb_flag: bool
    fairing_flag: bool
    srb_stage: int
    first_decouple_stage: int
    second_decouple_stage: int
    third_decouple_stage: int

@dataclass
class FlightStats():
    max_alt: list[int] = field(default_factory=list)
    max_ap: list[int] = field(default_factory=list)
    max_vel: list[int] = field(default_factory=list)
    start_time: int = 0
    end_time: int = 0
    total_mission_time: int = 0
    max_g: list[int] = field(default_factory=list)
    vessel_mass: int = 0
    max_thrust: int = 0
    isp: int = 0
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