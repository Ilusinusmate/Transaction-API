import click
from sqlmodel import SQLModel
from server.db import engine
import uvicorn

from server.api import app

# INITIALIZE TABLES
from authuser.models import Users
from transactions.models import Transactions, Operations
from accounts.models import Accounts

@click.group()
def cli():
    pass


@click.command("init_db")
def init_db():
    """Initialize the database models."""
    
    SQLModel.metadata.create_all(engine)
    click.echo("Database models initialized successfully.")


@click.command("runserver")
def runserver():
    """Run the server."""
    uvicorn.run(
        app=app,
        port=8000,
    )


cli.add_command(init_db)
cli.add_command(runserver)

if __name__ == "__main__":
    cli()
