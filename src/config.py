"""Static options used by the input forms for each vehicle type."""

from datetime import date


def current_year() -> int:
    """Evaluated per call so long-running deployments roll over at New Year."""
    return date.today().year


MIN_YEAR = 1995

VEHICLE_TYPES = ("car", "scooter", "bike")

CONDITIONS = ("Excellent", "Good", "Fair", "Poor")
OWNER_OPTIONS = ("1st Owner", "2nd Owner", "3rd Owner", "4th Owner or more")
INSURANCE_OPTIONS = ("Comprehensive", "Third Party", "Expired / None")

BRANDS = {
    "car": (
        "Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Honda", "Toyota",
        "Kia", "Renault", "Volkswagen", "Skoda", "MG", "Ford", "Nissan",
        "Chevrolet", "Datsun", "Fiat", "Jeep", "BMW", "Mercedes-Benz", "Audi",
        "Volvo", "Jaguar", "Lexus", "Land Rover", "Other",
    ),
    "scooter": (
        "Honda", "TVS", "Suzuki", "Hero", "Yamaha", "Ather", "Ola Electric",
        "Bajaj", "Vespa", "Aprilia", "Other",
    ),
    "bike": (
        "Hero", "Honda", "Bajaj", "TVS", "Royal Enfield", "Yamaha", "Suzuki",
        "KTM", "Kawasaki", "Harley-Davidson", "Triumph", "Jawa", "Other",
    ),
}

FUEL_TYPES = {
    "car": ("Petrol", "Diesel", "CNG", "LPG", "Electric", "Hybrid"),
    "scooter": ("Petrol", "Electric"),
    "bike": ("Petrol", "Electric"),
}

CAR_TRANSMISSIONS = ("Manual", "Automatic", "AMT", "CVT", "DCT")
CAR_BODY_TYPES = ("Hatchback", "Sedan", "SUV", "Compact SUV", "MUV", "Coupe", "Convertible", "Pickup")
BIKE_TYPES = ("Commuter", "Sports", "Cruiser", "Adventure / Touring", "Naked / Street", "Off-road")
BRAKE_TYPES = ("Drum", "Disc (Front)", "Disc (Both)", "ABS")

# Typical yearly usage (km) used to flag unusually high mileage.
TYPICAL_KM_PER_YEAR = {"car": 12_000, "scooter": 7_000, "bike": 9_000}
