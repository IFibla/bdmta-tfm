<script lang="ts">
	import Speedometer from '$lib/components/Speedometer.svelte';
	import StartGrid from '$lib/components/StartGrid.svelte';
	import Header from '$lib/components/Header.svelte';
	import { drivers } from '../state/carTelemetry';
	import type { Driver } from '../types/driver';
	import { onMount } from 'svelte';
	import RadialMap from '$lib/components/RadialMap.svelte';
	import { writable } from 'svelte/store';

	let socket;
	let selectedDriver: number = 0;

	let enginerpm = writable(0);
	let brake = writable(0);
	let throttle = writable(0);
	let speed = writable(0);
	let position = writable(0);

	onMount(() => {
		// Establish a WebSocket connection
		socket = new WebSocket('ws://127.0.0.1:30000');

		socket.onopen = () => {
			console.log('WebSocket connection established');
		};

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.driver === selectedDriver && data.packet_name === "Car Telemetry") {
				enginerpm.set(data.filtered_packet.engine_rpm);
				brake.set(data.filtered_packet.brake);
				throttle.set(data.filtered_packet.throttle);
				speed.set(data.filtered_packet.speed);
			}
			else if (data.driver === selectedDriver && data.packet_name === "Motion") {
				position.set(data.filtered_packet.world_position_perc);
				console.log($position);
			}
		};

		socket.onerror = (error) => {
			console.error('WebSocket Error:', error);
		};

		socket.onclose = () => {
			console.log('WebSocket connection closed');
		};
	});
</script>

<link rel="stylesheet" href="/smui.css" media="(prefers-color-scheme: light)" />
<main>
	<div id="grid-layout">
		<div id="header">
			<Header />
		</div>
		<div id="start-grid">
			<StartGrid drivers={$drivers} />
		</div>
		<div id="dashboards">
			<div id="gauges">
				<RadialMap driverPosition={$position}/>
				<Speedometer
					rpm={$enginerpm}
					speed={$speed}
					throttlePerc={$throttle}
					brakePerc={$brake}
				/>
				<Speedometer
					rpm={3012}
					speed={120}
					throttlePerc={90}
					brakePerc={50}
				/>
			</div>
			<h1>Strategy</h1>
		</div>
	</div>
</main>

<style>
    #grid-layout {
        display: grid;
        grid-template-columns: 1fr 5fr;
        grid-template-rows: 1fr 20fr;
				height: 98vh;
    }

    #start-grid {
				grid-area: 1 / 1 / 3 / 2;
        max-width: calc(70px + 70px + 20px);
				overflow-y: scroll;
				border-right: black solid 1px;
				padding: 0 10px 0 0;
		}
    #header {
				grid-area: 1 / 2 / 3 / 3;
				height: 5vh;
				width: calc(99vw - 200px);
				border-bottom: black solid 1px;
    }
    #dashboards {
				grid-area: 2 / 2 / 3 / 3;
				display: flex;
				flex-direction: column;
				justify-content: space-evenly;
        width: calc(99vw - 200px);
				overflow-y: scroll;
    }

		#gauges {
				display: grid;
				grid-template-columns: repeat(3, 1fr);
				justify-items: center;
		}
</style>