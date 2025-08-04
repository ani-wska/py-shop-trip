import json
import os
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    fuel_price = config["FUEL_PRICE"]

    customers = [Customer(**cust) for cust in config["customers"]]
    shops = [Shop(**shop) for shop in config["shops"]]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        best_shop = None
        min_cost = float("inf")

        for shop in shops:
            trip_cost = customer.total_trip_cost(shop, fuel_price)
            print(f"{customer.name}'s trip to the {shop.name} "
                  f"costs {trip_cost: .2f}")

            if trip_cost < min_cost:
                min_cost = trip_cost
                best_shop = shop

        if best_shop and min_cost <= customer.money:
            print(f"{customer.name} rides to {best_shop.name}")

            total_purchase_cost = customer.buy_products(best_shop)

            distance = customer.calculate_distance(best_shop.location)
            trip_cost = 2 * (customer.fuel_cost(distance, fuel_price))
            customer.money -= (total_purchase_cost + trip_cost)

            print(f"{customer.name} rides home")
            print(f"{customer.name} now has {customer.money: .2f} dollars")
        else:
            print(f"{customer.name} doesn't have enough money to "
                  f"make a purchase in any shop")
