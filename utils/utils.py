from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

console = Console()


def show_title():
    title = Panel(
        Align.center(
            "[bold cyan]🏡 Smart Property Finder[/bold cyan]\n[white]AI Powered Recommendation System[/white]"
        ),
        border_style="green",
    )
    console.print(title)


def show_section(title):
    console.print(f"\n[bold magenta]━━━ {title} ━━━[/bold magenta]\n")


def print_results(results):
    table = Table(title="🏡 Top Recommended Properties", show_lines=True)

    table.add_column("No", justify="center", style="cyan", no_wrap=True)
    table.add_column("Price", justify="right", style="green")
    table.add_column("Predicted", justify="right", style="yellow")
    table.add_column("Beds", justify="center")
    table.add_column("Baths", justify="center")
    table.add_column("Suburb", justify="center")
    table.add_column("Confidence", justify="center")
    table.add_column("Why", justify="left")

    for i, (_, row) in enumerate(results.iterrows(), 1):
        table.add_row(
            str(i),
            f"{row['price']}",
            f"{row['predicted_price']:.0f}",
            str(row["bedrooms"]),
            str(row["bathrooms"]),
            str(row["suburb"]),
            f"{row['confidence']:.1f}%",
            row["why"],
        )

    console.print(table)