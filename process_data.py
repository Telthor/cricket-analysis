import numpy as np
import pandas as pd

def process_batting_data(df):
    # Load the data
    df = df.drop_duplicates()

    # Remove non-numeric Innings Runs Scored
    batted_df = df.dropna(subset="Innings Runs Scored")
    batted_df = batted_df[batted_df["Innings Runs Scored"] != "DNB"]
    batted_df["Innings Runs Scored Stripped"] = batted_df["Innings Runs Scored"].map(
        lambda x: x.replace("*", "")
    )
    batted_df["Innings Runs Scored Stripped"] = pd.to_numeric(
        batted_df["Innings Runs Scored Stripped"], errors="coerce"
    )
    batted_df = batted_df.dropna(subset="Innings Runs Scored Stripped")

    # Calculate batting average
    batting_average = batted_df.groupby("Innings Player").sum().reset_index()
    batting_average["Total Outs"] = (
        batting_average["Innings Batted Flag"] - batting_average["Innings Not Out Flag"]
    )
    batting_average["Batting Average"] = (
        batting_average["Innings Runs Scored Stripped"] / batting_average["Total Outs"]
    )

    return batting_average


def process_bowling_data(df):
    # Load the data
    df = df.drop_duplicates()

    bowled_df = df.loc[df["Innings Bowled Flag"] == 1.0]
    bowled_df["Innings Runs Conceded"] = pd.to_numeric(
        bowled_df["Innings Runs Conceded"], errors="coerce"
    )
    bowled_df["Innings Wickets Taken"] = pd.to_numeric(
        bowled_df["Innings Wickets Taken"], errors="coerce"
    )
    bowled_average = bowled_df.groupby("Innings Player").sum().reset_index()
    bowled_average["Bowling Average"] = (
        bowled_average["Innings Runs Conceded"]
        / bowled_average["Innings Wickets Taken"]
    )

    return bowled_average


def load_and_concat():
    men_19C = pd.read_csv("./data/Men Test Player Innings Stats - 19th Century.csv")
    men_20C = pd.read_csv("./data/Men Test Player Innings Stats - 20th Century.csv")
    men_21C = pd.read_csv("./data/Men Test Player Innings Stats - 21st Century.csv")

    all_men = pd.concat([men_19C, men_20C, men_21C])

    return all_men


def load_and_merge():
    all_men = load_and_concat()
    all_men_batting = process_batting_data(all_men)
    all_men_bowling = process_bowling_data(all_men)
    all_men = pd.merge(left=all_men_batting, right=all_men_bowling, on="Innings Player")
    return all_men


def clean_df(all_men):
    max = all_men.loc[all_men["Bowling Average"] != np.inf]["Bowling Average"].max()
    all_men["Bowling Average"] = all_men["Bowling Average"].replace(np.inf, max)
    all_men["Bowling Average"] = all_men["Bowling Average"].replace(np.nan, max)
    return all_men


def load_merge_clean():
    all_men = load_and_merge()
    all_men_clean = clean_df(all_men)
    return all_men


if __name__ == "__main__":
    all_men = load_merge_clean()
    all_men.to_csv('./data/processed_data.csv')