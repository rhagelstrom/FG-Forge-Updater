import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from matplotlib import rcParams

# Downloading the font file
urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/lexend/Lexend%5Bwght%5D.ttf?raw=true", "/tmp/lexend.ttf")
if Path("/tmp/lexend.ttf").is_file():
    font_manager.fontManager.addfont("/tmp/lexend.ttf")
    rcParams["font.family"] = "Lexend"


def graph_users(sales: list[dict[str, (str | int | None)]]) -> None:
    sales_df = pd.DataFrame(sales)
    sales_df["created_at"] = pd.to_datetime(sales_df["created_at"])
    sales_df.set_index("created_at", inplace=True)

    sales_count = sales_df.resample("W").size().cumsum()

    plt.style.use("https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/rose-pine-moon.mplstyle")

    plt.figure(figsize=(25, 7))
    sns.lineplot(data=sales_count, linewidth=2.5, color="pink")

    plt.title("Cumulative Users", fontsize=26, pad=20)
    plt.xlabel("Date", fontsize=20, labelpad=20)
    plt.ylabel("Number of Users", fontsize=20, labelpad=20)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    sns.despine(left=True)

    plt.savefig("cumulative_users.png", dpi=300, bbox_inches="tight", transparent=True)
