import math


class Drone:
    """
    Represents a drone with various attributes such as serial number, value, weight, and insurance pricing details.

    Attributes:
        base_rate (dict): Base rate for different types of insurance.
        riebesell_curve_base_limit (int): Base limit for the Riebesell curve calculation.
        riebesell_curve_z (float): Z-value for the Riebesell curve calculation.
        weight_adjustments (list of tuples): Adjustment factors based on drone weight.
    """

    base_rate = {"Hull": 0.06, "Liability": 0.02}
    riebesell_curve_base_limit = 1000000
    riebesell_curve_z = 0.2
    weight_adjustments = {"0 - 5kg": 1, "5 - 10kg": 1.2, "10 - 20kg": 1.6, ">20kg": 2.5}

    def __init__(
        self,
        serial_number: str,
        value: int,
        weight: str,
        has_detachable_camera: bool,
        TPL_limit: int,
        TPL_excess: int,
    ):
        """
        Initialize the Drone instance with specified attributes.

        Args:
            serial_number (str): The serial number of the drone.
            value (int): The monetary value of the drone in GBP.
            weight (str): The weight of the drone.
            has_detachable_camera (bool): Indicates if the drone has a detachable camera.
            TPL_limit (int): Third-party liability limit.
            TPL_excess (int): Third-party liability excess amount.
        """
        if not isinstance(serial_number, str) or not serial_number:
            raise ValueError("Serial number must be a non-empty string.")
        if not isinstance(value, int) or value < 0:
            raise ValueError("Value must be a non-negative integer.")
        if weight not in Drone.weight_adjustments:
            raise ValueError("Weight must be a string inequality.")
        if not isinstance(has_detachable_camera, bool):
            raise ValueError("has_detachable_camera must be a boolean.")
        if not isinstance(TPL_limit, int) or TPL_limit <= 0:
            raise ValueError("TPL_limit must be a positive integer.")
        if not isinstance(TPL_excess, int) or TPL_excess < 0:
            raise ValueError("TPL_excess must be a non-negative integer.")

        self.serial_number = serial_number
        self.value = value
        self.weight = weight
        self.has_detachable_camera = has_detachable_camera
        self.TPL_limit = TPL_limit
        self.TPL_excess = TPL_excess

    def __str__(self):
        """
        Return a string representation of the Drone instance.

        Returns:
            str: A string describing the drone's attributes.
        """
        return f"""Serial Number: {self.serial_number}, 
        Value (GBP): {self.value}, 
        Weight: {self.weight}, 
        Has Detachable Camera?: {self.has_detachable_camera}, 
        TPL Limit: {self.TPL_limit}, 
        TPL Excess: {self.TPL_excess},
        Hull Base Rate: {self.hull_base_rate:.2g},
        Hull Weight Adjustment: {self.hull_weight_adjustment:.2f},
        Hull Final Rate: {self.hull_final_rate:.2g}, 
        Hull Premium: {self.hull_premium:.4g}, 
        TPL Base Rate: {self.TPL_base_rate}, 
        TPL Base Layer Premium: {self.TPL_base_layer_premium:2g}, 
        TPL ILF: {self.TPL_ILF:.2f}, 
        TPL Layer Premium: {self.TPL_layer_premium:.3g}"""

    def hull_calculations(self):
        """
        Calculate hull-related insurance rates and premiums for the drone.

        This method sets the hull base rate, hull weight adjustment, hull final rate, and hull premium based on the drone's value and weight. If the drone's value is zero, these attributes are set to None.
        """
        if self.value == 0:
            self.hull_base_rate = None
            self.hull_weight_adjustment = None
            self.hull_final_rate = None
            self.hull_premium = None
        else:
            self.hull_base_rate = Drone.base_rate["Hull"]
            self.hull_weight_adjustment = Drone.weight_adjustments[self.weight]
            self.hull_final_rate = self.hull_base_rate * self.hull_weight_adjustment
            self.hull_premium = self.value * self.hull_final_rate

    def TPL_calculations(self):
        """
        Calculate third-party liability (TPL) insurance rates and premiums for the drone.

        This method sets the TPL base rate, TPL base layer premium, TPL ILF (incremental load factor), and TPL layer premium based on the drone's value and TPL limits. If the drone's value is zero, these attributes are set to None.
        """
        if self.value == 0:
            self.TPL_base_rate = None
            self.TPL_base_layer_premium = None
            self.TPL_ILF = None
            self.TPL_layer_premium = None
        else:
            self.TPL_base_rate = Drone.base_rate["Liability"]
            self.TPL_base_layer_premium = self.value * self.TPL_base_rate
            self.TPL_ILF = Drone.riebesell(
                self.TPL_limit + self.TPL_excess,
            ) - Drone.riebesell(
                self.TPL_excess,
            )
            self.TPL_layer_premium = self.TPL_base_layer_premium * self.TPL_ILF

    def riebesell(x: int) -> float:
        """
        Calculate the Riebesell curve factor for a given value.

        This static method computes the Riebesell curve factor based on the provided value 'x'.
        The calculation uses the riebesell_curve_base_limit and riebesell_curve_z class attributes.

        Args:
            x (int): The value for which to calculate the Riebesell curve factor.

        Returns:
            float: The calculated Riebesell curve factor.
        """
        return (x / Drone.riebesell_curve_base_limit) ** (
            math.log(1 + Drone.riebesell_curve_z, 2)
        )


class DetachableCamera:
    """
    Represents a detachable camera associated with a list of drones.

    Attributes:
        drones (list[Drone]): A list of Drone instances.
        serial_number (str): The serial number of the detachable camera.
        value (int): The monetary value of the detachable camera in GBP.
    """

    def __init__(self, drones: list[Drone], serial_number: str, value: int):
        """
        Initialize the DetachableCamera instance with specified attributes.

        Args:
            drones (list[Drone]): A list of Drone instances to associate with this camera.
            serial_number (str): The serial number of the detachable camera.
            value (int): The monetary value of the detachable camera in GBP.
        """
        self.drones = drones
        self.serial_number = serial_number
        self.value = value

    def __str__(self):
        """
        Return a string representation of the DetachableCamera instance.

        Returns:
            str: A string describing the camera's attributes.
        """
        return f"""Serial Number: {self.serial_number}, 
        Value (GBP): {self.value},
        Rate: {self.rate:.2g},
        Premium: {self.premium:.3g}"""

    def calculations(self):
        """
        Calculate insurance rates and premiums for the detachable camera.

        This method sets the rate and premium for the camera based on its value and associated drones. If the camera's value is zero, these attributes are set to None.
        """
        if self.value == 0:
            self.rate = None
            self.premium = None
        else:
            self.rate = DetachableCamera.conditional_max(self.drones)
            self.premium = self.value * self.rate

    def conditional_max(drones: list[Drone]) -> float:
        """
        Determine the maximum rate based on a list of drones.

        This static method calculates the maximum rate for insurance based on the attributes of the drones in the provided list.

        Args:
            drones (list[Drone]): A list of Drone instances.

        Returns:
            float: The maximum rate determined from the drones' attributes.
        """
        filtered_drones = []
        filtered_drones = [
            drone
            for drone in drones
            if drone.has_detachable_camera == True and drone.value > 0
        ]
        return max(
            filtered_drones, key=lambda drone: drone.hull_final_rate
        ).hull_final_rate


def print_premiums(rows):
    """
    Print a formatted table of insurance premiums.

    This function takes a list of rows, each representing premium information, and prints it in a formatted table.

    Args:
        rows (list of tuples): Each tuple contains the description, net premium, and gross premium.
    """
    headers = ["", "Net", "Gross"]

    max_desc_length = max(len(row[0]) for row in rows)

    print(
        f"{headers[0].ljust(max_desc_length)} | {headers[1].rjust(10)} | {headers[2].rjust(10)}"
    )
    print("-" * (max_desc_length + 3 + 20))

    for description, net, gross in rows:
        print(f"{description.ljust(max_desc_length)} | {net:10.0f} | {gross:10.0f}")


def front_load_list(input_list: list[int], n: int) -> list[int]:
    """
    Generates a new list by front-loading values from the original list up to a specified limit.

    Args:
        input_list (list[int]): The original list of integers.
        n (int): The limit for front-loading values.

    Returns:
        list[int]: The new list front-loaded up to the specified limit.
    """
    new_list = [0] * len(input_list)

    total_added = 0
    for i in range(len(input_list)):
        while new_list[i] < input_list[i] and total_added < n:
            new_list[i] += 1
            total_added += 1

    return new_list


def drone_fleet_premium(
    drones: list[Drone], fleet: dict, n: int
) -> tuple[float, float, float]:
    """
    Calculate the total net premium for a fleet of drones.

    This function calculates the hull and TPL net premiums for a fleet of drones, as well as the total net premium.

    Args:
        drones (list[Drone]): A list of Drone instances.
        fleet (dict): A dictionary with drone serial numbers as keys and quantity as values.
        n (int): The number of drones in the fleet.

    Returns:
        tuple[float, float, float]: A tuple containing the hull net premium, TPL net premium, and total net premium.
    """
    combined = sorted(
        zip(drones, fleet.values()),
        key=lambda pair: pair[0].hull_premium + pair[0].TPL_layer_premium,
        reverse=True,
    )
    sorted_drones, sorted_other_list = zip(*combined)

    front_loaded_list = front_load_list(sorted_other_list, n)

    hull_net_premium = sum(
        [
            sorted_drones.hull_premium * front_loaded_list
            for sorted_drones, front_loaded_list in zip(
                sorted_drones, front_loaded_list
            )
        ]
    )

    TPL_net_premium = sum(
        [
            sorted_drones.TPL_layer_premium * front_loaded_list
            for sorted_drones, front_loaded_list in zip(
                sorted_drones, front_loaded_list
            )
        ]
    )

    total_net_premium = (
        hull_net_premium + TPL_net_premium + (n - sum(fleet.values())) * 150
    )

    return (hull_net_premium, TPL_net_premium, total_net_premium)


def camera_fleet_premium(
    cameras: list[DetachableCamera], fleet: dict, n: int, m: int
) -> int:
    """
    Calculate the total net premium for a fleet of detachable cameras.

    This function calculates the hull net premium for a fleet of detachable cameras.

    Args:
        cameras (list[DetachableCamera]): A list of DetachableCamera instances.
        fleet (dict): A dictionary with camera serial numbers as keys and quantity as values.
        n (int): The number of items in the drone fleet.
        m (int): The number of items in the camera fleet.

    Returns:
        int: The hull net premium for the camera fleet.
    """
    combined = sorted(
        zip(cameras, fleet.values()),
        key=lambda pair: pair[0].premium,
        reverse=True,
    )
    sorted_cameras, sorted_other_list = zip(*combined)

    front_loaded_list = front_load_list(sorted_other_list, m)

    hull_net_premium = (
        sum(
            [
                sorted_cameras.premium * front_loaded_list
                for sorted_cameras, front_loaded_list in zip(
                    sorted_cameras, front_loaded_list
                )
            ]
        )
        + (m - n) * 50
    )

    return hull_net_premium


def print_extension_premiums(
    drone_premiums: tuple[float, float, float], camera_premiums: int, brokerage: float
):
    """
    Print a formatted table of extended insurance premiums.

    This function takes premium data for drones and cameras, along with a brokerage rate, and prints it in a formatted table.

    Args:
        drone_premiums (tuple[float, float, float]): A tuple containing the drone hull, TPL, and total premiums.
        camera_premiums (int): The camera hull premium.
        brokerage (float): The brokerage rate to apply.
    """
    data = [
        ("Drone - Hull", drone_premiums[0], drone_premiums[0] / (1 - brokerage)),
        ("Drone - TPL", drone_premiums[1], drone_premiums[1] / (1 - brokerage)),
        ("Camera - Hull", camera_premiums, camera_premiums / (1 - brokerage)),
        (
            "Total",
            drone_premiums[2] + camera_premiums,
            (drone_premiums[2] + camera_premiums) / (1 - brokerage),
        ),
    ]

    print_premiums(data)


if __name__ == "__main__":

    details = {
        "Insured": "Drones R Us",
        "Underwriter": "Michael",
        "Broker": "Aon",
        "Brokerage": 0.3,
    }

    drones = [
        Drone("AAA-111", 10000, "0 - 5kg", True, 1000000, 0),
        Drone("BBB-222", 12000, "10 - 20kg", False, 4000000, 1000000),
        Drone("CCC-333", 15000, "5 - 10kg", True, 5000000, 5000000),
    ]

    for drone in drones:
        drone.hull_calculations()
        drone.TPL_calculations()

    detachable_cameras = [
        DetachableCamera(drones, "ZZZ-999", 5000),
        DetachableCamera(drones, "YYY-888", 2500),
        DetachableCamera(drones, "XXX-777", 1500),
        DetachableCamera(drones, "WWW-666", 2000),
    ]

    for camera in detachable_cameras:
        camera.calculations()

    drone_hull_net = sum(drone.hull_premium for drone in drones)
    drone_TPL_net = sum(drone.TPL_layer_premium for drone in drones)
    camera_hull_net = sum(camera.premium for camera in detachable_cameras)

    drone_hull_gross = drone_hull_net / (1 - details["Brokerage"])
    drone_TPL_gross = drone_TPL_net / (1 - details["Brokerage"])
    camera_hull_gross = camera_hull_net / (1 - details["Brokerage"])

    total_net = drone_hull_net + drone_TPL_net + camera_hull_net
    total_gross = drone_hull_gross + drone_TPL_gross + camera_hull_gross

    premium_data = [
        ("Drone - Hull", drone_hull_net, drone_hull_gross),
        ("Drone - TPL", drone_TPL_net, drone_TPL_gross),
        ("Camera - Hull", camera_hull_net, camera_hull_gross),
        ("Total", total_net, total_gross),
    ]

    for drone in drones:
        print(drone, "\n")

    for camera in detachable_cameras:
        print(camera, "\n")

    print_premiums(premium_data)

    # Extensions

    drone_fleet = {"AAA-111": 1, "BBB-222": 1, "CCC-333": 1}

    camera_fleet = {"ZZZ-999": 1, "YYY-888": 1, "XXX-777": 1, "WWW-666": 1}

    drone_premiums = drone_fleet_premium(drones, drone_fleet, 3)

    camera_premiums = camera_fleet_premium(
        detachable_cameras,
        camera_fleet,
        sum(drone_fleet.values()),
        sum(camera_fleet.values()),
    )

    print_extension_premiums(drone_premiums, camera_premiums, details["Brokerage"])
