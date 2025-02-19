import json

# Load data from a JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Save data to a JSON file
def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Add a new user
def add_user(user_id, name, role="guest", house_id=None):
    users_data = load_json('users.json')
    new_user = {
        "user_id": user_id,
        "name": name,
        "role": role,
        "house_id": house_id
    }
    users_data['users'].append(new_user)
    save_json('users.json', users_data)

# Add a new house
def add_house(house_id, name):
    houses_data = load_json('houses.json')
    new_house = {
        "house_id": house_id,
        "name": name,
        "floors": [],
        "rooms": [],
        "devices": []
    }
    houses_data['houses'].append(new_house)
    save_json('houses.json', houses_data)

# Add a new floor
def add_floor_to_house(house_id, floor_id, floor_name):
    floors_data = load_json('floors.json')
    new_floor = {
        "floor_id": floor_id,
        "name": floor_name,
        "rooms": []
    }
    floors_data['floors'].append(new_floor)
    save_json('floors.json', floors_data)

    # Update the house with the new floor
    houses_data = load_json('houses.json')
    for house in houses_data['houses']:
        if house['house_id'] == house_id:
            house['floors'].append(floor_id)
            break
    save_json('houses.json', houses_data)

# Add a new room
def add_room_to_floor(floor_id, room_id, room_name):
    rooms_data = load_json('rooms.json')
    new_room = {
        "room_id": room_id,
        "name": room_name,
        "floor_id": floor_id,
        "devices": []
    }
    rooms_data['rooms'].append(new_room)
    save_json('rooms.json', rooms_data)

    # Update the floor with the new room
    floors_data = load_json('floors.json')
    for floor in floors_data['floors']:
        if floor['floor_id'] == floor_id:
            floor['rooms'].append(room_id)
            break
    save_json('floors.json', floors_data)

# Add a new device to a room
def add_device_to_room(room_id, device_id):
    rooms_data = load_json('rooms.json')
    devices_data = load_json('devices.json')
    
    for room in rooms_data['rooms']:
        if room['room_id'] == room_id:
            room['devices'].append(device_id)
            break
    save_json('rooms.json', rooms_data)

    # Add device to devices.json (if not already there)
    if not any(device['device_id'] == device_id for device in devices_data['devices']):
        new_device = {
            "device_id": device_id,
            "name": f"Device {device_id}",
            "device_type": "generic",
            "status": "off"
        }
        devices_data['devices'].append(new_device)
        save_json('devices.json', devices_data)

# Update device status
def update_device_status(device_id, status, temperature=None, humidity=None):
    devices_data = load_json('devices.json')
    for device in devices_data['devices']:
        if device['device_id'] == device_id:
            device['status'] = status
            if temperature is not None:
                device['temperature'] = temperature
            if humidity is not None:
                device['humidity'] = humidity
            break
    save_json('devices.json', devices_data)

# Example of how to use the above functions
add_user(1, "John Doe", "admin", house_id=101)
add_house(101, "John's House")
add_floor_to_house(101, 1, "First Floor")
add_room_to_floor(1, 1, "Living Room")
add_device_to_room(1, 1)
update_device_status(1, "on", temperature=22)
