#!/usr/bin/env python3
from typing import Dict, List, Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from pydantic import BaseModel
import yaml
import os

app = typer.Typer()
console = Console()

class PromptComponent(BaseModel):
    """Base class for LangGPT prompt components"""
    content: str
    description: Optional[str] = None

class LangGPTPrompt(BaseModel):
    """Main class for LangGPT prompt structure"""
    role: PromptComponent
    profile: Optional[PromptComponent] = None
    rules: Optional[List[PromptComponent]] = None
    workflow: Optional[List[PromptComponent]] = None
    initialization: Optional[PromptComponent] = None
    commands: Optional[Dict[str, PromptComponent]] = None
    format: Optional[PromptComponent] = None

def create_component(component_name: str) -> PromptComponent:
    """Create a prompt component with user input"""
    console.print(f"\n[bold blue]Creating {component_name} component[/bold blue]")
    content = Prompt.ask(f"Enter the {component_name} content")
    description = Prompt.ask("Enter description (optional)", default="")
    return PromptComponent(content=content, description=description)

def create_prompt() -> LangGPTPrompt:
    """Create a complete LangGPT prompt through user interaction"""
    console.print(Panel.fit(
        "[bold green]LangGPT Prompt Generator[/bold green]\n"
        "Let's create a structured prompt following the LangGPT format.",
        title="Welcome"
    ))

    # Create role component
    role = create_component("role")

    # Create profile component
    if Confirm.ask("Would you like to add a profile component?"):
        profile = create_component("profile")
    else:
        profile = None

    # Create rules
    rules = []
    if Confirm.ask("Would you like to add rules?"):
        while True:
            rule = create_component("rule")
            rules.append(rule)
            if not Confirm.ask("Add another rule?"):
                break

    # Create workflow
    workflow = []
    if Confirm.ask("Would you like to add workflow steps?"):
        while True:
            step = create_component("workflow step")
            workflow.append(step)
            if not Confirm.ask("Add another workflow step?"):
                break

    # Create initialization
    initialization = None
    if Confirm.ask("Would you like to add initialization?"):
        initialization = create_component("initialization")

    # Create commands
    commands = {}
    if Confirm.ask("Would you like to add commands?"):
        while True:
            command_name = Prompt.ask("Enter command name")
            command = create_component(f"command: {command_name}")
            commands[command_name] = command
            if not Confirm.ask("Add another command?"):
                break

    # Create format
    format_component = None
    if Confirm.ask("Would you like to add format specifications?"):
        format_component = create_component("format")

    return LangGPTPrompt(
        role=role,
        profile=profile,
        rules=rules if rules else None,
        workflow=workflow if workflow else None,
        initialization=initialization,
        commands=commands if commands else None,
        format=format_component
    )

def save_prompt(prompt: LangGPTPrompt, filename: str):
    """Save the prompt to a YAML file"""
    prompt_dict = prompt.model_dump(exclude_none=True)
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(prompt_dict, f, allow_unicode=True, sort_keys=False)
    console.print(f"\n[green]Prompt saved to {filename}[/green]")

def format_prompt(prompt: LangGPTPrompt) -> str:
    """Format the prompt in markdown format"""
    md = []
    
    # Role
    md.append(f"# Role: {prompt.role.content}")
    if prompt.role.description:
        md.append(f"\n{prompt.role.description}\n")

    # Profile
    if prompt.profile:
        md.append("\n## Profile")
        md.append(prompt.profile.content)
        if prompt.profile.description:
            md.append(f"\n{prompt.profile.description}")

    # Rules
    if prompt.rules:
        md.append("\n## Rules")
        for rule in prompt.rules:
            md.append(f"- {rule.content}")
            if rule.description:
                md.append(f"  - {rule.description}")

    # Workflow
    if prompt.workflow:
        md.append("\n## Workflow")
        for i, step in enumerate(prompt.workflow, 1):
            md.append(f"{i}. {step.content}")
            if step.description:
                md.append(f"   - {step.description}")

    # Initialization
    if prompt.initialization:
        md.append("\n## Initialization")
        md.append(prompt.initialization.content)
        if prompt.initialization.description:
            md.append(f"\n{prompt.initialization.description}")

    # Commands
    if prompt.commands:
        md.append("\n## Commands")
        for name, command in prompt.commands.items():
            md.append(f"\n### {name}")
            md.append(command.content)
            if command.description:
                md.append(f"\n{command.description}")

    # Format
    if prompt.format:
        md.append("\n## Format")
        md.append(prompt.format.content)
        if prompt.format.description:
            md.append(f"\n{prompt.format.description}")

    return "\n".join(md)

@app.command()
def generate(
    output: str = typer.Option("prompt.yaml", help="Output YAML file name"),
    markdown: str = typer.Option("prompt.md", help="Output markdown file name")
):
    """Generate a new LangGPT prompt"""
    prompt = create_prompt()
    
    # Save YAML
    save_prompt(prompt, output)
    
    # Save markdown
    md_content = format_prompt(prompt)
    with open(markdown, 'w', encoding='utf-8') as f:
        f.write(md_content)
    console.print(f"[green]Markdown prompt saved to {markdown}[/green]")

if __name__ == "__main__":
    app() 