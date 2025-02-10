import pandas as pd
from haversine import haversine

from src.utils.time import robust_hour_of_iso_date


def driver_distance_to_pickup(df: pd.DataFrame) -> pd.DataFrame:
    df["driver_distance"] = df.apply(
        lambda r: haversine(
            (r["driver_latitude"], r["driver_longitude"]),
            (r["pickup_latitude"], r["pickup_longitude"]),
        ),
        axis=1,
    )
    return df


def hour_of_day(df: pd.DataFrame) -> pd.DataFrame:
    df["event_hour"] = df["event_timestamp"].apply(robust_hour_of_iso_date)
    return df


def driver_historical_completed_bookings(df: pd.DataFrame) -> pd.DataFrame:
    
    '''raise NotImplementedError(
        f"Show us your feature engineering skills! Suppose that drivers with a good track record are more likely to accept bookings. "
        f"Implement a feature that describes the number of historical bookings that each driver has completed."
    )'''
    
#    print("Original Columns:", df.columns.tolist())
    
    # Check if 'booking_status' exists now
#    if "booking_status_y" not in df.columns:
#        raise KeyError("The column 'booking_status' is missing from the DataFrame!")

    # Ensure driver_id is numeric
    df["driver_id"] = pd.to_numeric(df["driver_id"], errors="coerce")

    # Filter for completed trips
    completed_trips = df[df["is_completed"] == 1]
    completed_trips = completed_trips.loc[:, ['driver_id', 'is_completed', 'order_id']]

    # Count the number of completed trips per driver
    completed_trip_counts = (
        completed_trips.groupby("driver_id")["order_id"].count().reset_index()
    )
    completed_trip_counts.rename(
        columns={"order_id": "historical_completed_trips"}, inplace=True
    )

    # Merge the count back into the original dataframe
    df = df.merge(completed_trip_counts, on="driver_id", how="left")

    # Fill NaN values with 0 for drivers with no completed trips
    df["historical_completed_trips"] = df["historical_completed_trips"].fillna(0).astype(int)
    
    return df

