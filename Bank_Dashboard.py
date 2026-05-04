import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

parser = argparse.ArgumentParser(description="Render the bank marketing dashboard")
parser.add_argument("--output", "-o",
                    default=None,
                    help="Output image path for the rendered dashboard")
args = parser.parse_args()

# Load data 
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "bank-full.csv")
df = pd.read_csv(csv_path, sep=";")
df["subscribed"] = (df["y"] == "yes").astype(int)

# Pre-compute metrics 
total         = len(df)
converted     = int(df["subscribed"].sum())
conv_rate     = converted / total * 100
avg_dur_yes   = df[df["subscribed"] == 1]["duration"].mean()
avg_dur_no    = df[df["subscribed"] == 0]["duration"].mean()

def conv_by(col, order=None):
    g = df.groupby(col).agg(total=("subscribed","count"), conv=("subscribed","sum")).reset_index()
    g["rate"] = g["conv"] / g["total"] * 100
    if order:
        g[col] = pd.Categorical(g[col], categories=order, ordered=True)
        g = g.sort_values(col)
    else:
        g = g.sort_values("rate", ascending=False)
    return g

# Contact channel
channel_df = conv_by("contact")

# Monthly
month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
month_df = conv_by("month", month_order)

# Campaign count 
df["camp_bucket"] = df["campaign"].clip(upper=10).astype(str)
df.loc[df["campaign"] >= 10, "camp_bucket"] = "10+"
camp_order = [str(i) for i in range(1, 10)] + ["10+"]
camp_df = conv_by("camp_bucket", camp_order)

# Job
job_df = conv_by("job")

# Education
edu_order = ["primary","secondary","tertiary","unknown"]
edu_df = conv_by("education", edu_order)

# Housing loan
housing_df = conv_by("housing")

# Previous outcome
pout_df = conv_by("poutcome")
pout_df = pout_df.sort_values("rate", ascending=False)

# Palette 
BG       = "#1a1a1a"
CARD_BG  = "#242424"
BORDER   = "#333333"
TEXT_PRI = "#f0f0f0"
TEXT_SEC = "#999999"
BLUE     = "#378ADD"
TEAL     = "#1D9E75"
AMBER    = "#BA7517"
RED      = "#E24B4A"
GRAY     = "#666666"
GREEN    = "#639922"

def bar_color(rate):
    if rate >= 20:   return TEAL
    if rate >= 12:   return BLUE
    if rate >= 8:    return AMBER
    return RED

# Figure setup
fig = plt.figure(figsize=(24, 14), facecolor=BG)
fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.04, hspace=0.55, wspace=0.3)

# Title
fig.text(0.5, 0.965, "Bank Marketing Campaign — Funnel & Conversion Dashboard",
         ha="center", va="center", fontsize=16, fontweight="bold",
         color=TEXT_PRI, fontfamily="monospace")


# Grid layout 
outer = gridspec.GridSpec(3, 1, figure=fig, height_ratios=[0.8, 3.5, 3.5],
                          hspace=0.45, left=0.02, right=0.98, top=0.93, bottom=0.04)

# KPI row 
kpi_gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=outer[0], wspace=0.04)

kpi_data = [
    ("Total contacts",      f"{total:,}",          "campaign records",             BLUE),
    ("Conversions",         f"{converted:,}",       "subscribed to term deposit",   TEAL),
    ("Overall conv. rate",  f"{conv_rate:.1f}%",    "industry benchmark ~10–15%",   AMBER),
    ("Avg call (converted)",f"{avg_dur_yes:.0f}s",  f"vs {avg_dur_no:.0f}s non-converted", GREEN),
]

for i, (label, value, sub, color) in enumerate(kpi_data):
    ax = fig.add_subplot(kpi_gs[i])
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
        spine.set_linewidth(0.8)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.05, 0.78, label, transform=ax.transAxes, fontsize=9,
            color=TEXT_SEC, va="top")
    ax.text(0.05, 0.48, value, transform=ax.transAxes, fontsize=22,
            fontweight="bold", color=color, va="center")
    ax.text(0.05, 0.12, sub, transform=ax.transAxes, fontsize=8,
            color=TEXT_SEC, va="bottom")

mid_gs = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[1], wspace=0.3)

def style_ax(ax, title, ylabel="Conversion rate (%)"):
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER); spine.set_linewidth(0.6)
    ax.tick_params(colors=TEXT_SEC, labelsize=8.5)
    ax.yaxis.label.set_color(TEXT_SEC)
    ax.xaxis.label.set_color(TEXT_SEC)
    ax.set_title(title, color=TEXT_PRI, fontsize=10, pad=8, loc="left")
    ax.set_ylabel(ylabel, fontsize=8, color=TEXT_SEC)
    ax.set_facecolor(CARD_BG)
    ax.grid(axis="y", color=BORDER, linewidth=0.4, alpha=0.7)
    ax.set_axisbelow(True)
    fig.patch.set_facecolor(BG)

# Contact channel 
ax1 = fig.add_subplot(mid_gs[0])
style_ax(ax1, "Conversion rate by contact channel")
labels = channel_df["contact"].tolist()
rates  = channel_df["rate"].tolist()
colors = [bar_color(r) for r in rates]
bars = ax1.bar(labels, rates, color=colors, width=0.5, zorder=3, edgecolor="none")
for bar, rate in zip(bars, rates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{rate:.1f}%", ha="center", va="bottom", fontsize=9, color=TEXT_PRI)
ax1.set_ylim(0, max(rates) * 1.3)
ax1.tick_params(axis="x", colors=TEXT_PRI, labelsize=9)

#  Monthly 
ax2 = fig.add_subplot(mid_gs[1])
style_ax(ax2, "Conversion rate by month")
m_rates = month_df["rate"].tolist()
m_labels = [m.capitalize() for m in month_df["month"].tolist()]
m_colors = [bar_color(r) for r in m_rates]
bars2 = ax2.bar(m_labels, m_rates, color=m_colors, width=0.65, zorder=3, edgecolor="none")
for bar, rate in zip(bars2, m_rates):
    if rate > 15:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{rate:.0f}%", ha="center", va="bottom", fontsize=7.5, color=TEXT_PRI)
ax2.set_ylim(0, max(m_rates) * 1.2)
ax2.tick_params(axis="x", colors=TEXT_PRI, labelsize=8, rotation=35)

# Campaign contacts 
ax3 = fig.add_subplot(mid_gs[2])
style_ax(ax3, "Conversion by # contacts this campaign")
c_rates  = camp_df["rate"].tolist()
c_labels = camp_df["camp_bucket"].tolist()
c_colors = [bar_color(r) for r in c_rates]
bars3 = ax3.bar(c_labels, c_rates, color=c_colors, width=0.65, zorder=3, edgecolor="none")
for bar, rate in zip(bars3, c_rates):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f"{rate:.1f}%", ha="center", va="bottom", fontsize=8, color=TEXT_PRI)
ax3.set_ylim(0, max(c_rates) * 1.3)
ax3.set_xlabel("Number of contacts", fontsize=8, color=TEXT_SEC)
ax3.tick_params(axis="x", colors=TEXT_PRI, labelsize=9)


bot_gs = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[2], wspace=0.3)

# Job type 
ax4 = fig.add_subplot(bot_gs[0])
ax4.set_facecolor(CARD_BG)
for spine in ax4.spines.values():
    spine.set_edgecolor(BORDER); spine.set_linewidth(0.6)
ax4.set_title("Conversion by job type", color=TEXT_PRI, fontsize=10, pad=8, loc="left")
ax4.grid(axis="x", color=BORDER, linewidth=0.4, alpha=0.7)
ax4.set_axisbelow(True)

job_labels = job_df["job"].tolist()
job_rates  = job_df["rate"].tolist()
job_colors = [bar_color(r) for r in job_rates]
y_pos = range(len(job_labels)-1, -1, -1)
hbars = ax4.barh(list(y_pos), job_rates, color=job_colors, height=0.6, edgecolor="none")
ax4.set_yticks(list(y_pos))
ax4.set_yticklabels(job_labels, fontsize=9, color=TEXT_PRI)
ax4.set_xlabel("Conversion rate (%)", fontsize=8, color=TEXT_SEC)
ax4.tick_params(colors=TEXT_SEC, labelsize=8.5)
for bar, rate in zip(hbars, job_rates):
    ax4.text(rate + 0.3, bar.get_y() + bar.get_height()/2,
             f"{rate:.1f}%", va="center", fontsize=8.5, color=TEXT_PRI)
ax4.set_xlim(0, max(job_rates) * 1.25)

# Education + Housing 
inner_right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=bot_gs[1], hspace=0.55)

ax5 = fig.add_subplot(inner_right[0])
style_ax(ax5, "Conversion by education level")
e_labels = [e.capitalize() for e in edu_df["education"].tolist()]
e_rates  = edu_df["rate"].tolist()
e_colors = [bar_color(r) for r in e_rates]
b5 = ax5.bar(e_labels, e_rates, color=e_colors, width=0.5, zorder=3, edgecolor="none")
for bar, rate in zip(b5, e_rates):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f"{rate:.1f}%", ha="center", va="bottom", fontsize=9, color=TEXT_PRI)
ax5.set_ylim(0, max(e_rates) * 1.3)
ax5.tick_params(axis="x", colors=TEXT_PRI, labelsize=9)

ax6 = fig.add_subplot(inner_right[1])
style_ax(ax6, "Housing loan impact on conversion")
h_labels = ["No loan", "Has loan"]
h_rates  = [housing_df[housing_df["housing"]=="no"]["rate"].values[0],
            housing_df[housing_df["housing"]=="yes"]["rate"].values[0]]
h_colors = [TEAL, RED]
b6 = ax6.bar(h_labels, h_rates, color=h_colors, width=0.4, zorder=3, edgecolor="none")
for bar, rate in zip(b6, h_rates):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{rate:.1f}%", ha="center", va="bottom", fontsize=11, fontweight="bold",
             color=TEXT_PRI)
ax6.set_ylim(0, max(h_rates) * 1.35)
ax6.tick_params(axis="x", colors=TEXT_PRI, labelsize=10)

# 
ax7 = fig.add_subplot(bot_gs[2])
ax7.set_facecolor(CARD_BG)
for spine in ax7.spines.values():
    spine.set_edgecolor(BORDER); spine.set_linewidth(0.6)
ax7.set_xticks([]); ax7.set_yticks([])
ax7.set_title("Key drop-off risks & insights", color=TEXT_PRI, fontsize=10, pad=8, loc="left")

risks = [
    (RED,   "May = 30% of contacts",
             "13.7K calls made but only 6.7% convert — worst month"),
    (AMBER, "Unknown contact method",
             "28.8% of contacts, only 4.1% convert — fix data quality"),
    (AMBER, "3+ contacts in campaign",
             "Conversion drops sharply after 2 calls — stop re-dialling"),
    (TEAL,  "Prior success = 64.7% conv.",
             "Re-target previously converted customers first"),
    (BLUE,  "Longer calls = higher conv.",
             f"Converted avg {avg_dur_yes:.0f}s vs {avg_dur_no:.0f}s non-converted"),
]

y_start = 0.92
for color, headline, detail in risks:
    # colored left bar
    ax7.add_patch(FancyBboxPatch((0.01, y_start - 0.135), 0.025, 0.115,
                                  boxstyle="round,pad=0.005",
                                  facecolor=color, edgecolor="none",
                                  transform=ax7.transAxes, zorder=3))
    ax7.text(0.065, y_start - 0.01, headline,
             transform=ax7.transAxes, fontsize=9, fontweight="bold",
             color=TEXT_PRI, va="top")
    ax7.text(0.065, y_start - 0.055, detail,
             transform=ax7.transAxes, fontsize=7.8,
             color=TEXT_SEC, va="top", wrap=True)
    y_start -= 0.185

ax7.set_xlim(0, 1); ax7.set_ylim(0, 1)

# Save 
if args.output:
    out_path = os.path.expanduser(args.output)
    out_path = os.path.abspath(out_path)
else:
    out_dir = os.path.join(script_dir, "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "bank_marketing_dashboard.png")

out_dir = os.path.dirname(out_path) or script_dir
os.makedirs(out_dir, exist_ok=True)
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {out_path}")
plt.show()