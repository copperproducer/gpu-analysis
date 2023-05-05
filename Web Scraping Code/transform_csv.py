import pandas as pd

# Read in the NVDA, SPY, and BOND CSV files
nvda_data = pd.read_csv("NVDA.csv")
spy_data = pd.read_csv("SPY.csv")
bond_data = pd.read_csv("BOND.csv")

# Convert the "Date" column to a timestamp data type
nvda_data["Date"] = pd.to_datetime(nvda_data["Date"])
spy_data["Date"] = pd.to_datetime(spy_data["Date"])
bond_data["Date"] = pd.to_datetime(bond_data["Date"])

# Sort the data by date
nvda_data = nvda_data.sort_values("Date")
spy_data = spy_data.sort_values("Date")
bond_data = bond_data.sort_values("Date")

# Create a date range that covers the full range of dates in all datasets
date_range = pd.date_range(start=min(nvda_data["Date"]), end=max(bond_data["Date"]), freq="D")

# Fill in missing dates with the previous "Open" price
for date in date_range:
    # Check if the date is missing from the NVDA dataset
    if date not in nvda_data["Date"].values:
        # Find the previous date that has data in the NVDA dataset
        previous_date = nvda_data.loc[nvda_data["Date"] < date, "Date"].max()
        # Find the "Open" price for the previous date
        previous_open = nvda_data.loc[nvda_data["Date"] == previous_date, "Open"].values[0]
        # Insert a new row with the missing date and previous "Open" price
        nvda_data = nvda_data.append({"Date": date, "Open": previous_open}, ignore_index=True)

    # Check if the date is missing from the SPY dataset
    if date not in spy_data["Date"].values:
        # Find the previous date that has data in the SPY dataset
        previous_date = spy_data.loc[spy_data["Date"] < date, "Date"].max()
        # Check if there is data for the previous date
        if not pd.isna(previous_date):
            # Find the "Open" price for the previous date
            previous_open = spy_data.loc[spy_data["Date"] == previous_date, "Open"].values[0]
            # Insert a new row with the missing date and previous "Open" price
            spy_data = spy_data.append({"Date": date, "Open": previous_open}, ignore_index=True)

    # Check if the date is missing from the BOND dataset
    if date not in bond_data["Date"].values:
        # Find the previous date that has data in the BOND dataset
        previous_date = bond_data.loc[bond_data["Date"] < date, "Date"].max()
        # Check if there is data for the previous date
        if not pd.isna(previous_date):
            # Find the "Open" price for the previous date
            previous_open = bond_data.loc[bond_data["Date"] == previous_date, "Open"].values[0]
            # Insert a new row with the missing date and previous "Open" price
            bond_data = bond_data.append({"Date": date, "Open": previous_open}, ignore_index=True)

# Save the updated data to new CSV files
nvda_data.to_csv("NVDA_updated.csv", index=False)
spy_data.to_csv("SPY_updated.csv", index=False)
bond_data.to_csv("BOND_updated.csv", index=False)
