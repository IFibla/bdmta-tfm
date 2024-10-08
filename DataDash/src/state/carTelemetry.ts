import { writable } from 'svelte/store';
import type { Driver } from '../types/driver';

const initialDrivers: Driver[] = [
	{
		name: 'Max',
		surname: 'Verstappen',
		number: 1,
		team_name: 'Red Bull Racing',
		team_color: '#1E41FF',
		position: 1,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Sergio',
		surname: 'Pérez',
		number: 11,
		team_name: 'Red Bull Racing',
		team_color: '#1E41FF',
		position: 2,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Lewis',
		surname: 'Hamilton',
		number: 44,
		team_name: 'Mercedes-AMG Petronas Formula One Team',
		team_color: '#00D2BE',
		position: 3,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'George',
		surname: 'Russell',
		number: 63,
		team_name: 'Mercedes-AMG Petronas Formula One Team',
		team_color: '#00D2BE',
		position: 4,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Charles',
		surname: 'Leclerc',
		number: 16,
		team_name: 'Scuderia Ferrari',
		team_color: '#DC0000',
		position: 5,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Carlos',
		surname: 'Sainz',
		number: 55,
		team_name: 'Scuderia Ferrari',
		team_color: '#DC0000',
		position: 6,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Lando',
		surname: 'Norris',
		number: 4,
		team_name: 'McLaren F1 Team',
		team_color: '#FF8700',
		position: 7,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Oscar',
		surname: 'Piastri',
		number: 81,
		team_name: 'McLaren F1 Team',
		team_color: '#FF8700',
		position: 8,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Esteban',
		surname: 'Ocon',
		number: 31,
		team_name: 'Alpine F1 Team',
		team_color: '#00A3E0',
		position: 9,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Pierre',
		surname: 'Gasly',
		number: 10,
		team_name: 'Alpine F1 Team',
		team_color: '#00A3E0',
		position: 10,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Valtteri',
		surname: 'Bottas',
		number: 77,
		team_name: 'Alfa Romeo F1 Team',
		team_color: '#900000',
		position: 11,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Guanyu',
		surname: 'Zhou',
		number: 24,
		team_name: 'Alfa Romeo F1 Team',
		team_color: '#900000',
		position: 12,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Lance',
		surname: 'Stroll',
		number: 18,
		team_name: 'Aston Martin Aramco Cognizant Formula One Team',
		team_color: '#004D40',
		position: 13,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Fernando',
		surname: 'Alonso',
		number: 14,
		team_name: 'Aston Martin Aramco Cognizant Formula One Team',
		team_color: '#004D40',
		position: 14,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Yuki',
		surname: 'Tsunoda',
		number: 22,
		team_name: 'AlphaTauri',
		team_color: '#1E41FF',
		position: 15,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Nyck',
		surname: 'de Vries',
		number: 21,
		team_name: 'AlphaTauri',
		team_color: '#1E41FF',
		position: 16,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Nicholas',
		surname: 'Latifi',
		number: 6,
		team_name: 'Williams Racing',
		team_color: '#005AFF',
		position: 17,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Logan',
		surname: 'Sargeant',
		number: 2,
		team_name: 'Williams Racing',
		team_color: '#005AFF',
		position: 18,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Kevin',
		surname: 'Magnussen',
		number: 27,
		team_name: 'Haas F1 Team',
		team_color: '#D5D5D5',
		position: 18,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	},
	{
		name: 'Nico',
		surname: 'Hülkenberg',
		number: 20,
		team_name: 'Haas F1 Team',
		team_color: '#D5D5D5',
		position: 18,
		world_position_x: 0,
		world_position_y: 0,
		world_position_z: 0,
		speed: 0,
		throttle: 0,
		brake: 0,
		gear: 0,
		engine_rpm: 0,
		drs: 0,
		rear_left_brakes_temperature: 0,
		rear_right_brakes_temperature: 0,
		front_left_brakes_temperature: 0,
		front_right_brakes_temperature: 0,
		rear_left_tyres_surface_temperature: 0,
		rear_right_tyres_surface_temperature: 0,
		front_left_tyres_surface_temperature: 0,
		front_right_tyres_surface_temperature: 0,
		rear_left_tyres_inner_temperature: 0,
		rear_right_tyres_inner_temperature: 0,
		front_left_tyres_inner_temperature: 0,
		front_right_tyres_inner_temperature: 0,
		engine_temperature: 0,
		rear_left_tyres_pressure: 0,
		rear_right_tyres_pressure: 0,
		front_left_tyres_pressure: 0,
		front_right_tyres_pressure: 0,
		rear_left_surface_type: 0,
		rear_right_surface_type: 0,
		front_left_surface_type: 0,
		front_right_surface_type: 0,
		fuelMix: 0,
		frontBrakeBias: 0,
		pitLimiterStatus: 0,
		fuelInTank: 0,
		fuelCapacity: 0,
		fuelRemainingLaps: 0,
		drsAllowed: 0,
		drsActivationDistance: 0,
		ersStoreEnergy: 0,
		ersDeployMode: 0,
		ersDeployedThisLap: 0,
		rear_left_tyresDamage: 0,
		rear_right_tyresDamage: 0,
		front_left_tyresDamage: 0,
		front_right_tyresDamage: 0
	}
];

export const drivers = writable(initialDrivers);
