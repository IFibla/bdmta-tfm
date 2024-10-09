import copy
import random
import matplotlib.pyplot as plt
from tqdm import tqdm


def evaluate_pitting_strategy_plot(
    strategy,
    number_laps,
    target_lap_time,
    target_lap_tyre_damage,
    target_lap_tyre_damage_time,
    pit_delta_time,
):
    total_race_list = []
    accumulated_tyre_damage_list = []
    total_race_time = 0
    accumulated_tyre_damage = 0

    # Initial stint from lap 0 to the first pit stop
    lap_end = strategy["pit_lap"][0]
    for lap in range(lap_end):
        total_race_time += target_lap_time + (target_lap_tyre_damage_time * lap)
        accumulated_tyre_damage += target_lap_tyre_damage
        total_race_list.append(target_lap_time + (target_lap_tyre_damage_time * (lap)))
        accumulated_tyre_damage_list.append(accumulated_tyre_damage)
        if accumulated_tyre_damage > 100:
            return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    for i in range(len(strategy["pit_lap"]) - 1):
        lap_start = strategy["pit_lap"][i]
        lap_end = strategy["pit_lap"][i + 1]

        total_race_time += target_lap_time + pit_delta_time
        accumulated_tyre_damage = target_lap_tyre_damage
        total_race_list.append(target_lap_time + pit_delta_time)
        accumulated_tyre_damage_list.append(accumulated_tyre_damage)

        if accumulated_tyre_damage > 100:
            return float("inf")

        for lap in range(lap_start + 1, lap_end):
            total_race_time += target_lap_time + (
                target_lap_tyre_damage_time * (lap - lap_start)
            )
            accumulated_tyre_damage += target_lap_tyre_damage
            total_race_list.append(
                target_lap_time + (target_lap_tyre_damage_time * (lap - lap_start))
            )
            accumulated_tyre_damage_list.append(accumulated_tyre_damage)

            if accumulated_tyre_damage > 100:
                return float("inf")

    lap_start = strategy["pit_lap"][-1]

    # Set the lap time for the first lap of the final stint
    total_race_time += target_lap_time + pit_delta_time
    accumulated_tyre_damage = 0
    total_race_list.append(target_lap_time + pit_delta_time)
    accumulated_tyre_damage_list.append(accumulated_tyre_damage)

    if accumulated_tyre_damage > 100:
        return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    # Add the remaining laps in the final stint
    for lap in range(lap_start + 1, number_laps):
        total_race_time += target_lap_time + (
            target_lap_tyre_damage_time * (lap - lap_start)
        )
        accumulated_tyre_damage += target_lap_tyre_damage
        total_race_list.append(
            target_lap_time + (target_lap_tyre_damage_time * (lap - lap_start))
        )
        accumulated_tyre_damage_list.append(accumulated_tyre_damage)

        if accumulated_tyre_damage > 100:
            return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(accumulated_tyre_damage_list)
    ax1.set_xlabel("Lap")
    ax1.set_ylabel("Tyre Damage")

    ax2.bar([i for i in range(len(total_race_list))], total_race_list)
    ax2.set_xlabel("Lap")
    ax2.set_ylabel("Lap Time")
    ax2.set_ylim(60, 100)

    ax1.set_title(f"Strategy time {total_race_time}")
    plt.show()


def evaluate_pitting_strategy(
    strategy,
    number_laps,
    target_lap_time,
    target_lap_tyre_damage,
    target_lap_tyre_damage_time,
    pit_delta_time,
):
    total_race_time = 0
    accumulated_tyre_damage = 0

    lap_end = strategy["pit_lap"][0]
    for lap in range(lap_end):
        total_race_time += target_lap_time + (target_lap_tyre_damage_time * lap)
        accumulated_tyre_damage += target_lap_tyre_damage
        if accumulated_tyre_damage > 100:
            return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    total_race_time += pit_delta_time

    # Remaining stints between pit stops
    for i in range(len(strategy["pit_lap"]) - 1):
        lap_start = strategy["pit_lap"][i]
        lap_end = strategy["pit_lap"][i + 1]

        total_race_time += target_lap_time
        accumulated_tyre_damage = target_lap_tyre_damage
        if accumulated_tyre_damage > 100:
            return float("inf")

        for lap in range(lap_start + 1, lap_end):
            total_race_time += target_lap_time + (
                target_lap_tyre_damage_time * (lap - lap_start)
            )
            accumulated_tyre_damage += target_lap_tyre_damage
            if accumulated_tyre_damage > 100:
                return float("inf")

        total_race_time += pit_delta_time

    # Add final segment after last pit stop
    lap_start = strategy["pit_lap"][-1]

    # Set the lap time for the first lap of the final stint
    total_race_time += target_lap_time
    accumulated_tyre_damage = target_lap_tyre_damage
    if accumulated_tyre_damage > 100:
        return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    # Add the remaining laps in the final stint
    for lap in range(lap_start + 1, number_laps):
        total_race_time += target_lap_time + (
            target_lap_tyre_damage_time * (lap - lap_start)
        )
        accumulated_tyre_damage += target_lap_tyre_damage
        if accumulated_tyre_damage > 100:
            return float("inf")  # Invalid strategy if tyre damage exceeds 100%

    return total_race_time


def generate_neighbor(strategy, number_laps):
    new_strategy = copy.deepcopy(strategy)

    operation = random.choice(["add", "delete", "adjust"])

    if operation == "add":
        new_pit_lap = random.randint(1, number_laps)
        new_strategy["pit_lap"].append(new_pit_lap)

    elif operation == "delete" and len(new_strategy["pit_lap"]) > 1:
        index_to_delete = random.randint(0, len(new_strategy["pit_lap"]) - 1)
        new_strategy["pit_lap"].pop(index_to_delete)

    elif operation == "adjust":
        index_to_adjust = random.randint(0, len(new_strategy["pit_lap"]) - 1)
        new_strategy["pit_lap"][index_to_adjust] += random.choice([-1, 1])
        # Ensure the adjusted lap is within valid range
        new_strategy["pit_lap"][index_to_adjust] = max(
            1, min(number_laps, new_strategy["pit_lap"][index_to_adjust])
        )
    new_strategy["pit_lap"].sort()
    new_strategy["pit_lap"] = list(set(new_strategy["pit_lap"]))

    return new_strategy


# Hill Climbing Example
def hill_climbing(
    initial_strategy,
    number_laps,
    target_lap_time,
    target_lap_tyre_damage,
    target_lap_tyre_damage_time,
    pit_delta_time,
    iterations,
):
    current_strategy = initial_strategy
    current_score = evaluate_pitting_strategy(
        current_strategy,
        number_laps,
        target_lap_time,
        target_lap_tyre_damage,
        target_lap_tyre_damage_time,
        pit_delta_time,
    )

    for _ in tqdm(range(iterations)):
        # Generate a neighboring strategy
        new_strategy = generate_neighbor(current_strategy, number_laps)
        new_score = evaluate_pitting_strategy(
            new_strategy,
            number_laps,
            target_lap_time,
            target_lap_tyre_damage,
            target_lap_tyre_damage_time,
            pit_delta_time,
        )

        if new_score < current_score:
            current_strategy, current_score = new_strategy, new_score
            print(
                f"New better strategy found: {current_strategy} with score {current_score}"
            )

    return current_strategy, current_score


# Initial strategy
initial_strategy = {"pit_lap": [10, 46]}  # Example lap numbers for pit stops
target_lap_time = 70
target_lap_tyre_damage = 2.5
target_lap_tyre_damage_time = 0.084
number_laps = 72
pit_delta_time = 20

# Run the hill climbing search
best_strategy, best_score = hill_climbing(
    initial_strategy,
    number_laps,
    target_lap_time,
    target_lap_tyre_damage,
    target_lap_tyre_damage_time,
    pit_delta_time,
    1000000,
)
evaluate_pitting_strategy_plot(
    best_strategy,
    number_laps,
    target_lap_time,
    target_lap_tyre_damage,
    target_lap_tyre_damage_time,
    pit_delta_time,
)
print("Best strategy found:", best_strategy)
print("Best score:", best_score)
