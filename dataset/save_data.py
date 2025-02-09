def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data saved in {filename}")
