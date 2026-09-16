######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################


airport_info = ("OUL", 1, "14-09-2026")

allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}

restricted_destinations = {"Moscow", "Pyongyang"}

flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"],
    },
}


def _normalize_key(text):
    """Strip surrounding whitespace and uppercase a flight key."""
    return text.strip().upper()


def _normalize_name(text):
    """Strip surrounding whitespace and lowercase a passenger name."""
    return text.strip().lower()


def find_flight(flights, flight_number):
    """Return the normalized (existing) flight key or None."""
    target = _normalize_key(flight_number)

    for key in flights:
        if _normalize_key(key) == target:
            return key

    return None


def passenger_exists(passengers, passenger_name):
    """Return True if the passenger is present (case-insensitive)."""
    target = _normalize_name(passenger_name)

    return any(
        _normalize_name(name) == target
        for name in passengers
    )


def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    """Add a passenger to a flight.

    Returns one of:
    OK, FLIGHT_NOT_FOUND, EMPTY_NAME, DUPLICATE, FULL, RESTRICTED
    """
    key = find_flight(flights, flight_number)

    if key is None:
        return "FLIGHT_NOT_FOUND"

    name = passenger_name.strip()

    if not name:
        return "EMPTY_NAME"

    name = name.title()

    flight = flights[key]

    if passenger_exists(flight["passengers"], name):
        return "DUPLICATE"

    if any(
        _normalize_name(destination) == _normalize_name(flight["destination"])
        for destination in restricted_destinations
    ):
        return "RESTRICTED"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    flight["passengers"].append(name)
    return "OK"

def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    """Remove a passenger from a flight.

    Returns one of: OK, FLIGHT_NOT_FOUND, PASSENGER_NOT_FOUND
    """
    key = find_flight(flights, flight_number)

    if key is None:
        return "FLIGHT_NOT_FOUND"

    flight = flights[key]
    target = _normalize_name(passenger_name)

    for index, name in enumerate(flight["passengers"]):
        if _normalize_name(name) == target:
            flight["passengers"].pop(index)
            return "OK"

    return "PASSENGER_NOT_FOUND"


def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    """Change the gate of a flight.

    Returns one of: OK, FLIGHT_NOT_FOUND, INVALID_GATE
    """
    key = find_flight(flights, flight_number)

    if key is None:
        return "FLIGHT_NOT_FOUND"

    normalized_gate = _normalize_key(new_gate)

    if normalized_gate not in {
        _normalize_key(gate)
        for gate in allowed_gates
    }:
        return "INVALID_GATE"

    flights[key]["gate"] = normalized_gate
    return "OK"


def flight_status(flight):
    """Return AVAILABLE, ALMOST FULL, or FULL based on occupancy."""
    capacity = flight["capacity"]
    count = len(flight["passengers"])

    if capacity <= 0:
        return "FULL" if count > 0 else "AVAILABLE"

    percentage = count / capacity * 100

    if percentage == 100:
        return "FULL"

    if percentage >= 75:
        return "ALMOST FULL"

    return "AVAILABLE"


def sorted_manifest(
    flights,
    flight_number
):
    """Return a sorted copy of the passenger list, or None."""
    key = find_flight(flights, flight_number)

    if key is None:
        return None

    return sorted(flights[key]["passengers"])


def total_passengers(flights):
    """Return the total number of passengers across all flights."""
    return sum(
        len(flight["passengers"])
        for flight in flights.values()
    )


def any_full_flight(flights):
    """Return True if any flight has reached its capacity."""
    return any(
        len(flight["passengers"]) >= flight["capacity"]
        for flight in flights.values()
    )


def all_flights_have_passengers(flights):
    """Return True if every flight has at least one passenger."""
    return all(
        len(flight["passengers"]) > 0
        for flight in flights.values()
    )
