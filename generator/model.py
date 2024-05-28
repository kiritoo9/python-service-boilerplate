import os
from src.configs.database import DB_SESSION
from sqlalchemy import text

# Main
def ModelGenerator(get_table = False, selected_table = None):
    db = DB_SESSION()
    results = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")) # get all tables
    if get_table:
        return results

    # Base model
    base_template = "from sqlalchemy import Column, String, Uuid, Boolean, Date, DateTime, Float"
    base_template += "\nfrom src.configs.database import Base\n\n"
    
    for record in results:

        # Create model files by table_name
        table_name = record.table_name
        if selected_table is None or selected_table == table_name:

            # re-create file
            filepath = f"src/models/{table_name}.py"
            if os.path.exists(filepath) is True:
                os.remove(filepath)

            # Fill more template
            first_letter = table_name[:1].upper()
            template = base_template
            template += f'class {first_letter + table_name[1:]}(Base):\n\t__tablename__ = "{table_name}"\n\n'

            # Describe table
            details = db.execute(text(f"SELECT column_name,column_default,is_nullable,data_type FROM information_schema.columns WHERE table_name = '{table_name}'"))
            primary_key = db.execute(text(f"SELECT c.column_name, c.data_type FROM information_schema.table_constraints tc JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema AND tc.table_name = c.table_name AND ccu.column_name = c.column_name WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name}'"))

            for detail in details:
                column_type = "String"
                column_nullable=True
                column_comment=""

                # Check primary
                column_primary_key=""
                for pk in primary_key:
                    if pk.column_name == detail.column_name:
                        column_primary_key = ", primary_key=True"

                if detail.is_nullable == "NO":
                    column_nullable = False

                if detail.data_type == "uuid":
                    column_type = "Uuid"
                elif detail.data_type == "character varying":
                    column_type = "String"
                elif detail.data_type == "boolean":
                    column_type = "Boolean"
                elif detail.data_type == "date":
                    column_type = "Date"
                elif detail.data_type == "numeric":
                    column_type = "Numeric"
                elif detail.data_type == "integer":
                    column_type = "Integer"
                elif "timestamp" in detail.data_type:
                    column_type = "DateTime"

                template += f'\t{detail.column_name} = Column({column_type}, nullable={column_nullable}, comment="{column_comment}"{column_primary_key})\n'

            # save file
            f = open(filepath, "w")
            f.write(template)
            f.close()

        # End process immediately if selected_table is not None
        if selected_table == table_name:
            break

    return True