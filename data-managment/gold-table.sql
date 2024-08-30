CREATE TABLE aggregated_data (
    driver INT,
    lap INT,

    -- Aggregations for g_force_lateral
    count_g_force_lateral BIGINT,
    mean_g_force_lateral FLOAT8,
    stddev_g_force_lateral FLOAT8,
    min_g_force_lateral FLOAT8,
    max_g_force_lateral FLOAT8,
    "25th_percentile_g_force_lateral" FLOAT8,
    "50th_percentile_g_force_lateral" FLOAT8,
    "75th_percentile_g_force_lateral" FLOAT8,

    -- Aggregations for g_force_longitudinal
    count_g_force_longitudinal BIGINT,
    mean_g_force_longitudinal FLOAT8,
    stddev_g_force_longitudinal FLOAT8,
    min_g_force_longitudinal FLOAT8,
    max_g_force_longitudinal FLOAT8,
    "25th_percentile_g_force_longitudinal" FLOAT8,
    "50th_percentile_g_force_longitudinal" FLOAT8,
    "75th_percentile_g_force_longitudinal" FLOAT8,

    -- Aggregations for g_force_vertical
    count_g_force_vertical BIGINT,
    mean_g_force_vertical FLOAT8,
    stddev_g_force_vertical FLOAT8,
    min_g_force_vertical FLOAT8,
    max_g_force_vertical FLOAT8,
    "25th_percentile_g_force_vertical" FLOAT8,
    "50th_percentile_g_force_vertical" FLOAT8,
    "75th_percentile_g_force_vertical" FLOAT8,

    -- Aggregations for yaw
    count_yaw BIGINT,
    mean_yaw FLOAT8,
    stddev_yaw FLOAT8,
    min_yaw FLOAT8,
    max_yaw FLOAT8,
    "25th_percentile_yaw" FLOAT8,
    "50th_percentile_yaw" FLOAT8,
    "75th_percentile_yaw" FLOAT8,

    -- Aggregations for pitch
    count_pitch BIGINT,
    mean_pitch FLOAT8,
    stddev_pitch FLOAT8,
    min_pitch FLOAT8,
    max_pitch FLOAT8,
    "25th_percentile_pitch" FLOAT8,
    "50th_percentile_pitch" FLOAT8,
    "75th_percentile_pitch" FLOAT8,

    -- Aggregations for roll
    count_roll BIGINT,
    mean_roll FLOAT8,
    stddev_roll FLOAT8,
    min_roll FLOAT8,
    max_roll FLOAT8,
    "25th_percentile_roll" FLOAT8,
    "50th_percentile_roll" FLOAT8,
    "75th_percentile_roll" FLOAT8,

    -- Aggregations for rear_left_brakes_temperature
    count_rear_left_brakes_temperature BIGINT,
    mean_rear_left_brakes_temperature FLOAT8,
    stddev_rear_left_brakes_temperature FLOAT8,
    min_rear_left_brakes_temperature FLOAT8,
    max_rear_left_brakes_temperature FLOAT8,
    "25th_percentile_rear_left_brakes_temperature" FLOAT8,
    "50th_percentile_rear_left_brakes_temperature" FLOAT8,
    "75th_percentile_rear_left_brakes_temperature" FLOAT8,

    -- Aggregations for rear_right_brakes_temperature
    count_rear_right_brakes_temperature BIGINT,
    mean_rear_right_brakes_temperature FLOAT8,
    stddev_rear_right_brakes_temperature FLOAT8,
    min_rear_right_brakes_temperature FLOAT8,
    max_rear_right_brakes_temperature FLOAT8,
    "25th_percentile_rear_right_brakes_temperature" FLOAT8,
    "50th_percentile_rear_right_brakes_temperature" FLOAT8,
    "75th_percentile_rear_right_brakes_temperature" FLOAT8,

    -- Aggregations for front_left_brakes_temperature
    count_front_left_brakes_temperature BIGINT,
    mean_front_left_brakes_temperature FLOAT8,
    stddev_front_left_brakes_temperature FLOAT8,
    min_front_left_brakes_temperature FLOAT8,
    max_front_left_brakes_temperature FLOAT8,
    "25th_percentile_front_left_brakes_temperature" FLOAT8,
    "50th_percentile_front_left_brakes_temperature" FLOAT8,
    "75th_percentile_front_left_brakes_temperature" FLOAT8,

    -- Aggregations for front_right_brakes_temperature
    count_front_right_brakes_temperature BIGINT,
    mean_front_right_brakes_temperature FLOAT8,
    stddev_front_right_brakes_temperature FLOAT8,
    min_front_right_brakes_temperature FLOAT8,
    max_front_right_brakes_temperature FLOAT8,
    "25th_percentile_front_right_brakes_temperature" FLOAT8,
    "50th_percentile_front_right_brakes_temperature" FLOAT8,
    "75th_percentile_front_right_brakes_temperature" FLOAT8,

    -- Aggregations for rear_left_tyres_surface_temperature
    count_rear_left_tyres_surface_temperature BIGINT,
    mean_rear_left_tyres_surface_temperature FLOAT8,
    stddev_rear_left_tyres_surface_temperature FLOAT8,
    min_rear_left_tyres_surface_temperature FLOAT8,
    max_rear_left_tyres_surface_temperature FLOAT8,
    "25th_percentile_rear_left_tyres_surface_temperature" FLOAT8,
    "50th_percentile_rear_left_tyres_surface_temperature" FLOAT8,
    "75th_percentile_rear_left_tyres_surface_temperature" FLOAT8,

    -- Aggregations for rear_right_tyres_surface_temperature
    count_rear_right_tyres_surface_temperature BIGINT,
    mean_rear_right_tyres_surface_temperature FLOAT8,
    stddev_rear_right_tyres_surface_temperature FLOAT8,
    min_rear_right_tyres_surface_temperature FLOAT8,
    max_rear_right_tyres_surface_temperature FLOAT8,
    "25th_percentile_rear_right_tyres_surface_temperature" FLOAT8,
    "50th_percentile_rear_right_tyres_surface_temperature" FLOAT8,
    "75th_percentile_rear_right_tyres_surface_temperature" FLOAT8,

    -- Aggregations for front_left_tyres_surface_temperature
    count_front_left_tyres_surface_temperature BIGINT,
    mean_front_left_tyres_surface_temperature FLOAT8,
    stddev_front_left_tyres_surface_temperature FLOAT8,
    min_front_left_tyres_surface_temperature FLOAT8,
    max_front_left_tyres_surface_temperature FLOAT8,
    "25th_percentile_front_left_tyres_surface_temperature" FLOAT8,
    "50th_percentile_front_left_tyres_surface_temperature" FLOAT8,
    "75th_percentile_front_left_tyres_surface_temperature" FLOAT8,

    -- Aggregations for front_right_tyres_surface_temperature
    count_front_right_tyres_surface_temperature BIGINT,
    mean_front_right_tyres_surface_temperature FLOAT8,
    stddev_front_right_tyres_surface_temperature FLOAT8,
    min_front_right_tyres_surface_temperature FLOAT8,
    max_front_right_tyres_surface_temperature FLOAT8,
    "25th_percentile_front_right_tyres_surface_temperature" FLOAT8,
    "50th_percentile_front_right_tyres_surface_temperature" FLOAT8,
    "75th_percentile_front_right_tyres_surface_temperature" FLOAT8,

    -- Aggregations for rear_left_tyres_inner_temperature
    count_rear_left_tyres_inner_temperature BIGINT,
    mean_rear_left_tyres_inner_temperature FLOAT8,
    stddev_rear_left_tyres_inner_temperature FLOAT8,
    min_rear_left_tyres_inner_temperature FLOAT8,
    max_rear_left_tyres_inner_temperature FLOAT8,
    "25th_percentile_rear_left_tyres_inner_temperature" FLOAT8,
    "50th_percentile_rear_left_tyres_inner_temperature" FLOAT8,
    "75th_percentile_rear_left_tyres_inner_temperature" FLOAT8,

    -- Aggregations for rear_right_tyres_inner_temperature
    count_rear_right_tyres_inner_temperature BIGINT,
    mean_rear_right_tyres_inner_temperature FLOAT8,
    stddev_rear_right_tyres_inner_temperature FLOAT8,
    min_rear_right_tyres_inner_temperature FLOAT8,
    max_rear_right_tyres_inner_temperature FLOAT8,
    "25th_percentile_rear_right_tyres_inner_temperature" FLOAT8,
    "50th_percentile_rear_right_tyres_inner_temperature" FLOAT8,
    "75th_percentile_rear_right_tyres_inner_temperature" FLOAT8,

    -- Aggregations for front_left_tyres_inner_temperature
    count_front_left_tyres_inner_temperature BIGINT,
    mean_front_left_tyres_inner_temperature FLOAT8,
    stddev_front_left_tyres_inner_temperature FLOAT8,
    min_front_left_tyres_inner_temperature FLOAT8,
    max_front_left_tyres_inner_temperature FLOAT8,
    "25th_percentile_front_left_tyres_inner_temperature" FLOAT8,
    "50th_percentile_front_left_tyres_inner_temperature" FLOAT8,
    "75th_percentile_front_left_tyres_inner_temperature" FLOAT8,

    -- Aggregations for front_right_tyres_inner_temperature
    count_front_right_tyres_inner_temperature BIGINT,
    mean_front_right_tyres_inner_temperature FLOAT8,
    stddev_front_right_tyres_inner_temperature FLOAT8,
    min_front_right_tyres_inner_temperature FLOAT8,
    max_front_right_tyres_inner_temperature FLOAT8,
    "25th_percentile_front_right_tyres_inner_temperature" FLOAT8,
    "50th_percentile_front_right_tyres_inner_temperature" FLOAT8,
    "75th_percentile_front_right_tyres_inner_temperature" FLOAT8,

    -- Aggregations for engine_temperature
    count_engine_temperature BIGINT,
    mean_engine_temperature FLOAT8,
    stddev_engine_temperature FLOAT8,
    min_engine_temperature FLOAT8,
    max_engine_temperature FLOAT8,
    "25th_percentile_engine_temperature" FLOAT8,
    "50th_percentile_engine_temperature" FLOAT8,
    "75th_percentile_engine_temperature" FLOAT8,

    -- Aggregations for rear_left_tyres_pressure
    count_rear_left_tyres_pressure BIGINT,
    mean_rear_left_tyres_pressure FLOAT8,
    stddev_rear_left_tyres_pressure FLOAT8,
    min_rear_left_tyres_pressure FLOAT8,
    max_rear_left_tyres_pressure FLOAT8,
    "25th_percentile_rear_left_tyres_pressure" FLOAT8,
    "50th_percentile_rear_left_tyres_pressure" FLOAT8,
    "75th_percentile_rear_left_tyres_pressure" FLOAT8,

    -- Aggregations for rear_right_tyres_pressure
    count_rear_right_tyres_pressure BIGINT,
    mean_rear_right_tyres_pressure FLOAT8,
    stddev_rear_right_tyres_pressure FLOAT8,
    min_rear_right_tyres_pressure FLOAT8,
    max_rear_right_tyres_pressure FLOAT8,
    "25th_percentile_rear_right_tyres_pressure" FLOAT8,
    "50th_percentile_rear_right_tyres_pressure" FLOAT8,
    "75th_percentile_rear_right_tyres_pressure" FLOAT8,

    -- Aggregations for front_left_tyres_pressure
    count_front_left_tyres_pressure BIGINT,
    mean_front_left_tyres_pressure FLOAT8,
    stddev_front_left_tyres_pressure FLOAT8,
    min_front_left_tyres_pressure FLOAT8,
    max_front_left_tyres_pressure FLOAT8,
    "25th_percentile_front_left_tyres_pressure" FLOAT8,
    "50th_percentile_front_left_tyres_pressure" FLOAT8,
    "75th_percentile_front_left_tyres_pressure" FLOAT8,

    -- Aggregations for front_right_tyres_pressure
    count_front_right_tyres_pressure BIGINT,
    mean_front_right_tyres_pressure FLOAT8,
    stddev_front_right_tyres_pressure FLOAT8,
    min_front_right_tyres_pressure FLOAT8,
    max_front_right_tyres_pressure FLOAT8,
    "25th_percentile_front_right_tyres_pressure" FLOAT8,
    "50th_percentile_front_right_tyres_pressure" FLOAT8,
    "75th_percentile_front_right_tyres_pressure" FLOAT8,

    -- Aggregations for fuelMix
    count_fuelMix BIGINT,
    mean_fuelMix FLOAT8,
    stddev_fuelMix FLOAT8,
    min_fuelMix FLOAT8,
    max_fuelMix FLOAT8,
    "25th_percentile_fuelMix" FLOAT8,
    "50th_percentile_fuelMix" FLOAT8,
    "75th_percentile_fuelMix" FLOAT8,

    -- Aggregations for frontBrakeBias
    count_frontBrakeBias BIGINT,
    mean_frontBrakeBias FLOAT8,
    stddev_frontBrakeBias FLOAT8,
    min_frontBrakeBias FLOAT8,
    max_frontBrakeBias FLOAT8,
    "25th_percentile_frontBrakeBias" FLOAT8,
    "50th_percentile_frontBrakeBias" FLOAT8,
    "75th_percentile_frontBrakeBias" FLOAT8,

    -- Aggregations for pitLimiterStatus
    count_pitLimiterStatus BIGINT,
    mean_pitLimiterStatus FLOAT8,
    stddev_pitLimiterStatus FLOAT8,
    min_pitLimiterStatus FLOAT8,
    max_pitLimiterStatus FLOAT8,
    "25th_percentile_pitLimiterStatus" FLOAT8,
    "50th_percentile_pitLimiterStatus" FLOAT8,
    "75th_percentile_pitLimiterStatus" FLOAT8,

    -- Aggregations for fuelInTank
    count_fuelInTank BIGINT,
    mean_fuelInTank FLOAT8,
    stddev_fuelInTank FLOAT8,
    min_fuelInTank FLOAT8,
    max_fuelInTank FLOAT8,
    "25th_percentile_fuelInTank" FLOAT8,
    "50th_percentile_fuelInTank" FLOAT8,
    "75th_percentile_fuelInTank" FLOAT8,

    -- Aggregations for fuelCapacity
    count_fuelCapacity BIGINT,
    mean_fuelCapacity FLOAT8,
    stddev_fuelCapacity FLOAT8,
    min_fuelCapacity FLOAT8,
    max_fuelCapacity FLOAT8,
    "25th_percentile_fuelCapacity" FLOAT8,
    "50th_percentile_fuelCapacity" FLOAT8,
    "75th_percentile_fuelCapacity" FLOAT8,

    -- Aggregations for fuelRemainingLaps
    count_fuelRemainingLaps BIGINT,
    mean_fuelRemainingLaps FLOAT8,
    stddev_fuelRemainingLaps FLOAT8,
    min_fuelRemainingLaps FLOAT8,
    max_fuelRemainingLaps FLOAT8,
    "25th_percentile_fuelRemainingLaps" FLOAT8,
    "50th_percentile_fuelRemainingLaps" FLOAT8,
    "75th_percentile_fuelRemainingLaps" FLOAT8,

    -- Aggregations for drsAllowed
    count_drsAllowed BIGINT,
    mean_drsAllowed FLOAT8,
    stddev_drsAllowed FLOAT8,
    min_drsAllowed FLOAT8,
    max_drsAllowed FLOAT8,
    "25th_percentile_drsAllowed" FLOAT8,
    "50th_percentile_drsAllowed" FLOAT8,
    "75th_percentile_drsAllowed" FLOAT8,

    -- Aggregations for drsActivationDistance
    count_drsActivationDistance BIGINT,
    mean_drsActivationDistance FLOAT8,
    stddev_drsActivationDistance FLOAT8,
    min_drsActivationDistance FLOAT8,
    max_drsActivationDistance FLOAT8,
    "25th_percentile_drsActivationDistance" FLOAT8,
    "50th_percentile_drsActivationDistance" FLOAT8,
    "75th_percentile_drsActivationDistance" FLOAT8,

    -- Aggregations for ersStoreEnergy
    count_ersStoreEnergy BIGINT,
    mean_ersStoreEnergy FLOAT8,
    stddev_ersStoreEnergy FLOAT8,
    min_ersStoreEnergy FLOAT8,
    max_ersStoreEnergy FLOAT8,
    "25th_percentile_ersStoreEnergy" FLOAT8,
    "50th_percentile_ersStoreEnergy" FLOAT8,
    "75th_percentile_ersStoreEnergy" FLOAT8,

    -- Aggregations for ersDeployMode
    count_ersDeployMode BIGINT,
    mean_ersDeployMode FLOAT8,
    stddev_ersDeployMode FLOAT8,
    min_ersDeployMode FLOAT8,
    max_ersDeployMode FLOAT8,
    "25th_percentile_ersDeployMode" FLOAT8,
    "50th_percentile_ersDeployMode" FLOAT8,
    "75th_percentile_ersDeployMode" FLOAT8,

    -- Aggregations for ersDeployedThisLap
    count_ersDeployedThisLap BIGINT,
    mean_ersDeployedThisLap FLOAT8,
    stddev_ersDeployedThisLap FLOAT8,
    min_ersDeployedThisLap FLOAT8,
    max_ersDeployedThisLap FLOAT8,
    "25th_percentile_ersDeployedThisLap" FLOAT8,
    "50th_percentile_ersDeployedThisLap" FLOAT8,
    "75th_percentile_ersDeployedThisLap" FLOAT8,

    -- Aggregations for rear_left_tyresDamage
    count_rear_left_tyresDamage BIGINT,
    mean_rear_left_tyresDamage FLOAT8,
    stddev_rear_left_tyresDamage FLOAT8,
    min_rear_left_tyresDamage FLOAT8,
    max_rear_left_tyresDamage FLOAT8,
    "25th_percentile_rear_left_tyresDamage" FLOAT8,
    "50th_percentile_rear_left_tyresDamage" FLOAT8,
    "75th_percentile_rear_left_tyresDamage" FLOAT8,

    -- Aggregations for rear_right_tyresDamage
    count_rear_right_tyresDamage BIGINT,
    mean_rear_right_tyresDamage FLOAT8,
    stddev_rear_right_tyresDamage FLOAT8,
    min_rear_right_tyresDamage FLOAT8,
    max_rear_right_tyresDamage FLOAT8,
    "25th_percentile_rear_right_tyresDamage" FLOAT8,
    "50th_percentile_rear_right_tyresDamage" FLOAT8,
    "75th_percentile_rear_right_tyresDamage" FLOAT8,

    -- Aggregations for front_left_tyresDamage
    count_front_left_tyresDamage BIGINT,
    mean_front_left_tyresDamage FLOAT8,
    stddev_front_left_tyresDamage FLOAT8,
    min_front_left_tyresDamage FLOAT8,
    max_front_left_tyresDamage FLOAT8,
    "25th_percentile_front_left_tyresDamage" FLOAT8,
    "50th_percentile_front_left_tyresDamage" FLOAT8,
    "75th_percentile_front_left_tyresDamage" FLOAT8,

    -- Aggregations for front_right_tyresDamage
    count_front_right_tyresDamage BIGINT,
    mean_front_right_tyresDamage FLOAT8,
    stddev_front_right_tyresDamage FLOAT8,
    min_front_right_tyresDamage FLOAT8,
    max_front_right_tyresDamage FLOAT8,
    "25th_percentile_front_right_tyresDamage" FLOAT8,
    "50th_percentile_front_right_tyresDamage" FLOAT8,
    "75th_percentile_front_right_tyresDamage" FLOAT8,

    PRIMARY KEY (driver, lap)
);
