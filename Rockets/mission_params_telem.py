class MissionParameters():
    def __init__(self,
                    mission_type = "Test Flight",
                    gravity_turn = False,
                    srb_flag = False,
                    landing_flag = False,
                    countdown_time = 10,
                    first_decouple_stage = 3,
                    second_decouple_stage = 2,
                    third_decouple_stage = 1,
                    srb_stage = 0,
                    target_apoapsis = 80000,
                    target_pitch = 90,
                    target_heading = 90,
                    target_roll = 0,
                    turn_angle = 0,
                    turn_start_altitude = 250,
                    turn_end_altitude = 45000,
                    parachute_altitude = 1200,
                    side_boosters_seperated = False,
                    main_booster_seperated = False,
                    payload_booster_seperated = False,
                    fairing_jettison = False,
                    roll = False,
                    clamp_release_time = 0):
        self.mission_type = mission_type
        self.gravity_turn = gravity_turn
        self.srb_flag = srb_flag
        self.landing_flag = landing_flag
        self.countdown_time = countdown_time
        self.first_decouple_stage = first_decouple_stage
        self.second_decouple_stage = second_decouple_stage
        self.third_decouple_stage = third_decouple_stage
        self.srb_stage = srb_stage
        self.target_apoapsis = target_apoapsis
        self.target_pitch = target_pitch
        self.target_heading = target_heading
        self.target_roll = target_roll
        self.turn_angle = turn_angle
        self.turn_start_altitude = turn_start_altitude
        self.turn_end_altitude = turn_end_altitude
        self.parachute_altitude = parachute_altitude
        self.side_boosters_seperated = side_boosters_seperated
        self.main_booster_seperated =main_booster_seperated
        self.payload_booster_seperated = payload_booster_seperated
        self.fairing_jettison = fairing_jettison
        self.roll = roll
        self.clamp_release_time = clamp_release_time

class FlightStats():
    def __init__(self,
                    max_alt = [0],
                    max_ap = [0],
                    max_vel = [0],
                    start_time = 0,
                    end_time = 0,
                    total_mission_time = 0,
                    max_g = [0],
                    vessel_mass = 0,
                    max_thrust = 0,
                    isp = 0,
                    touchdown_speed = 0):
        self.max_alt = max_alt
        self.max_ap = max_ap
        self.max_vel = max_vel
        self.start_time = start_time
        self.end_time = end_time
        self.total_mission_time = total_mission_time
        self.max_g = max_g
        self.vessel_mass = vessel_mass
        self.max_thrust = max_thrust
        self.isp = isp
        self.touchdown_speed = touchdown_speed

class Telemetry():
    def __init__(self, conn, vessel):
        self.surface_altitude = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'surface_altitude')
        self.altitude = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'mean_altitude')
        self.apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
        self.velocity = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
        self.vertical_vel = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'vertical_speed')
        self.periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')

class LaunchVehicle():
    def __init__(self, conn, vessel, mission_params):
        self.first_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=mission_params.first_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.second_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=mission_params.second_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.third_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=mission_params.third_decouple_stage, 
                                                cumulative=False).amount, 
                                                'LiquidFuel')
        self.srb_stage_LF = conn.add_stream(vessel.resources_in_decouple_stage(stage=mission_params.srb_stage, 
                                                cumulative=False).amount, 
                                                'SolidFuel')