# insurance-exposure-rating-algorithm

## Description

This Python script defines a Drone and DetachableCamera class, which models the exposure rating and insurance premium pricing using the attributes of the drones and cameras detailed in ```Initial File - hx Interview Model.xlsm```.

## Dependencies

To use this script, ensure you have Python installed on your system. No additional libraries are required as the script uses standard Python libraries.

## Usage

Just run the script once and the intermediate values for the drones and cameras will be calculated and printed to terminal followed by the table of premiums and then another table of premiums which is the result of Extensions 1 and 2.

For Extension 1 and 2, the user must input the quantities of each drone and detachable camera that they are looking to get priced. By default there are just one of each drone and detachable camera, as in the base case.

### Create an instance of the Drone class
    drone_instance = Drone(Serial Number, Value, Weight, Has Detachable Camera?, TPL Limit, TPL Excess)

Drone instances of the drones detailed in the file ```Initial File - hx Interview Model.xlsm``` have already been created in the script.

### Create an instance of the Camera class
    camera_instance = DetachableCamera(Drones, Serial Number, Value)


Detachable camera instances of the detachable cameras detailed in the file ```Initial File - hx Interview Model.xlsm``` have already been created in the script.

### Extension 1 - Input Fleet of Drones

    drone_fleet = {"AAA-111": x, "BBB-222": y, "CCC-333": z}

A user can replace x, y and z with the number of each type of drone, by serial number, that they are looking to get priced.

### Extension 2 - Input Fleet of Cameras

    camera_fleet = {"ZZZ-999": p, "YYY-888": q, "XXX-777": r, "WWW-666": s}

A user can replace p, q, r and s with the number of each type of camera, by serial number, that they are looking to get priced.
