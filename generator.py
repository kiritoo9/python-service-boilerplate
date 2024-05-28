import time
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from generator.model import ModelGenerator

console = Console()

# Show prompt
greetings = """
Wilujeng sumping kang, mangga pilih naon anu anjeun generate:

1. Generate Model dari Database
2. Generate CRUD (nanti bisa milih tablenya)
"""

print("\n")
print(Panel(greetings, title="Nyi Sombro Cli - Generator", subtitle="author: @kiritoo9 - version 1.1", width=60, style="magenta"))

try:
    choosen = int(Prompt.ask("\nSok asupkeun pilihan maneh :moai:"))
    if choosen > 2:
        console.print(f"\nHampura kang, teu aya pilihan nomer {choosen} :smiley:")
    else:

        if choosen == 1:
            choosen_table_type = Prompt.ask(f"\nGenerate semua table apa per-table kang?", choices=["semua","satu_aja"])
            choosen_table = None
            tables = [] # Store all table to handle later

            with console.status("Punten kang diantosan sakedap", spinner="aesthetic"):
                time.sleep(1)
                if choosen_table_type == "satu_aja":
                    table_list = ModelGenerator(True)

                    # Generate table
                    table = Table(highlight=True)
                    table.add_column("Table Name", style="magenta")
                    for v in table_list:
                        tables.append(v.table_name)
                        table.add_row(v.table_name)
                    console.print(table)
                else:
                    ModelGenerator() # Generate all table

            # Handle when only choose one table
            if choosen_table_type == "satu_aja":
                choosen_table = Prompt.ask(f"\nSok mangga kang dipilih mau table yang mana :smiley:")
                if choosen_table not in tables:
                    console.print("\nwkwk funny lu cil :laughing:", style="red")
                    exit()

                with console.status("Diantosan lagi kang sakedap", spinner="aesthetic"):
                    time.sleep(1)
                    ModelGenerator(False, choosen_table)

            # End process
            console.print("\nAlhamdulillah kabéh tabel dina database anjeun geus dihasilkeun, nuhun kang :winking_face::folded_hands:", style="blue")
        elif choosen == 2:
            console.print(f"\n[yellow]Buat generate CRUD masih dikerjain kang hehe :kissing:")

except Exception as e:
    console.print(f"\nwkwkwk hampura kang masih aya error euy :laughing:\nieu kang error nya: [red]{str(e)}")