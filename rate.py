rate_settings = {
    "1": 10,
    "2": 20,
    "3": 30,
    "4": 60,
    "5": 80
}
required_rate = ["1", "2", "3", "4", "5"]


def calculate_rating(percent):
    rate_settings_keys = list(rate_settings.keys())
    rate_settings_values = list(rate_settings.values())
    if not all(map(lambda rate: rate in required_rate, rate_settings_keys)) or len(required_rate) != len(rate_settings_keys):
        raise Exception("invalid rate config")
    if any(map(lambda rate: rate < 0 or rate > 100, rate_settings_values)):
        raise Exception("invalid rate value, must be between 0 - 100")
    if rate_settings_values != sorted(rate_settings_values):
        raise Exception("invalid rate value, must be sorted")
    for rate in reversed(rate_settings):
        passing_value = rate_settings[rate]
        if percent >= passing_value:
            return rate
    return 0

print(calculate_rating(50)) 
