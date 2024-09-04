from api.profiles_api.models import UserRank, Profile
from api.water_management.models import WaterMeter, Property


def update_rankings():
    # Get all profiles
    profiles = Profile.objects.select_related('user')
    # Dictionaries to hold total consumption by town and company
    town_consumption = {}
    company_consumption = {}

    # Calculate total consumption for each user
    for profile in profiles:
        user = profile.user
        properties = Property.objects.filter(user=user)
        if not properties:
            continue

        user_total_consumption = 0

        for property in properties:
            water_meters = WaterMeter.objects.filter(client_number=property.client_number)

            for water_meter in water_meters:
                average_consumption = water_meter.calculate_average_monthly_consumption()
                if isinstance(average_consumption, str):
                    break

                user_total_consumption += average_consumption['average_monthly_consumption']

        if user_total_consumption == 0:
            continue

        # Aggregate total consumption by town and company
        town = profile.city
        water_company = property.client_number.water_company

        if town not in town_consumption:
            town_consumption[town] = []
        town_consumption[town].append((user, user_total_consumption))

        if water_company not in company_consumption:
            company_consumption[water_company] = []
        company_consumption[water_company].append((user, user_total_consumption))

    # Rank users by town
    for town, users in town_consumption.items():
        users_sorted = sorted(users, key=lambda x: x[1], reverse=True)
        for idx, (user, _) in enumerate(users_sorted):
            UserRank.objects.update_or_create(
                user=user,
                defaults={'town_rank': idx + 1}
            )

    # Rank users by water company
    for water_company, users in company_consumption.items():
        users_sorted = sorted(users, key=lambda x: x[1], reverse=True)
        for idx, (user, _) in enumerate(users_sorted):
            UserRank.objects.update_or_create(
                user=user,
                defaults={'company_rank': idx + 1}
            )
