#!/usr/bin/env python3
"""Interactive Configuration Wizard"""

import re
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich import box
import questionary
from questionary import Style

console = Console()

custom_style = Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:magenta bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:green'),
])


def validate_bundle_id(value: str) -> bool:
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*(\.[a-zA-Z][a-zA-Z0-9]*)+$', value))


def validate_email(value: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value))


def section_header(title: str, emoji: str = "⚙️"):
    console.print()
    console.print(Panel(f"[bold]{title}[/bold]", title=f"[bold cyan]{emoji}[/bold cyan]",
                       border_style="cyan", box=box.DOUBLE))
    console.print()


def run_wizard(existing_config: dict = None) -> dict:
    """Run the interactive configuration wizard"""
    config = existing_config or {}
    
    console.print(Panel(
        "[bold]Welcome to the Configuration Wizard![/bold]\n\n"
        "This wizard will guide you through setting up your deployment configuration.\n"
        "Press [bold cyan]Ctrl+C[/bold cyan] at any time to cancel.",
        title="[bold cyan]⚙️ Configuration Wizard[/bold cyan]", border_style="cyan"))
    
    # Basic App Information
    section_header("Basic App Information", "📱")
    
    config['app_name'] = questionary.text(
        "App Display Name:",
        default=config.get('app_name', config.get('analysis', {}).get('project_name', '')),
        style=custom_style).ask()
    
    default_bundle = f"com.company.{config.get('app_name', 'app').lower().replace(' ', '')}"
    config['ios_bundle_id'] = questionary.text(
        "iOS Bundle Identifier:",
        default=config.get('ios_bundle_id', default_bundle),
        validate=lambda x: validate_bundle_id(x) or "Invalid format (com.company.app)",
        style=custom_style).ask()
    
    config['android_package_name'] = questionary.text(
        "Android Package Name:",
        default=config.get('android_package_name', config['ios_bundle_id'].lower()),
        style=custom_style).ask()
    
    config['version'] = questionary.text("Initial Version:", default=config.get('version', '1.0.0'), style=custom_style).ask()
    
    # Team & Organization
    section_header("Team & Organization", "👥")
    
    config['organization_name'] = questionary.text("Organization Name:", default=config.get('organization_name', ''), style=custom_style).ask()
    config['team_email'] = questionary.text("Team Email:", default=config.get('team_email', ''),
                                            validate=lambda x: validate_email(x) or "Invalid email", style=custom_style).ask()
    config['apple_team_id'] = questionary.text("Apple Team ID (10 chars):", default=config.get('apple_team_id', ''), style=custom_style).ask()
    
    # Environments
    section_header("Environments", "🌍")
    
    config['environments'] = questionary.checkbox(
        "Which environments do you need?",
        choices=[
            questionary.Choice("Development", value="dev", checked=True),
            questionary.Choice("Staging", value="staging", checked=True),
            questionary.Choice("Production", value="prod", checked=True),
        ], style=custom_style).ask()
    
    config['env_config'] = {}
    for env in config['environments']:
        config['env_config'][env] = {
            'api_url': questionary.text(f"  API URL ({env}):", 
                default=f'https://api.{env}.example.com', style=custom_style).ask()
        }
    
    # Code Signing
    section_header("Code Signing", "🔑")
    
    config['code_signing'] = {}
    config['code_signing']['ios_method'] = questionary.select(
        "iOS signing method:",
        choices=[
            questionary.Choice("Fastlane Match (recommended)", value="match"),
            questionary.Choice("Manual certificates", value="manual"),
            questionary.Choice("Xcode automatic", value="automatic"),
        ], style=custom_style).ask()
    
    if config['code_signing']['ios_method'] == "match":
        config['code_signing']['match'] = {
            'git_url': questionary.text("  Match certificates repo URL:", style=custom_style).ask(),
            'storage_mode': "git",
        }
    
    # CI/CD
    section_header("CI/CD Configuration", "🔄")
    
    config['cicd'] = {}
    config['cicd']['github_repo'] = questionary.text("GitHub repository (owner/repo):", style=custom_style).ask()
    config['cicd']['use_self_hosted'] = questionary.confirm("Use self-hosted Mac Mini runner?", default=True, style=custom_style).ask()
    
    if config['cicd']['use_self_hosted']:
        config['cicd']['runner'] = {
            'labels': questionary.text("  Runner labels (comma-separated):", default="self-hosted,macOS,ARM64", style=custom_style).ask().split(','),
            'xcode_version': questionary.text("  Xcode version:", default="15.0", style=custom_style).ask(),
        }
    
    # Summary
    section_header("Configuration Summary", "📋")
    display_config_summary(config)
    
    if questionary.confirm("Save this configuration?", default=True, style=custom_style).ask():
        console.print(Panel("[green]✓ Configuration saved![/green]", border_style="green"))
    
    return config


def display_config_summary(config: dict):
    """Display configuration summary"""
    tree = Tree("[bold cyan]📋 Configuration Summary[/bold cyan]")
    
    app = tree.add("[yellow]📱 App[/yellow]")
    app.add(f"Name: [white]{config.get('app_name', 'N/A')}[/white]")
    app.add(f"iOS Bundle: [white]{config.get('ios_bundle_id', 'N/A')}[/white]")
    app.add(f"Android Package: [white]{config.get('android_package_name', 'N/A')}[/white]")
    
    team = tree.add("[yellow]👥 Team[/yellow]")
    team.add(f"Organization: [white]{config.get('organization_name', 'N/A')}[/white]")
    team.add(f"Apple Team ID: [white]{config.get('apple_team_id', 'N/A')}[/white]")
    
    envs = tree.add("[yellow]🌍 Environments[/yellow]")
    for env in config.get('environments', []):
        envs.add(f"[cyan]{env}[/cyan]")
    
    cicd = tree.add("[yellow]🔄 CI/CD[/yellow]")
    cicd.add(f"Repository: [white]{config.get('cicd', {}).get('github_repo', 'N/A')}[/white]")
    cicd.add(f"Self-hosted: [white]{config.get('cicd', {}).get('use_self_hosted', False)}[/white]")
    
    console.print(tree)
