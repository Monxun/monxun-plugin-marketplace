#!/usr/bin/env python3
"""
Flutter Deploy CLI - Automated Flutter App Deployment Pipeline
A beautiful CLI tool for automating Flutter app deployment to iOS and Android
"""

import sys
import os
from pathlib import Path
from typing import Optional
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich import box
import questionary
from questionary import Style

# Initialize Rich console
console = Console()

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                              ASCII ART & BRANDING                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

LOGO = """
[bold cyan]
    ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗ 
    ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
    █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝
    ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
    ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║
    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
[/bold cyan][bold magenta]
    ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
[/bold magenta]"""

TAGLINE = "[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]"

SUBTITLE = "[bold white]✨ Automated Flutter App Deployment Pipeline ✨[/bold white]"

VERSION = "1.0.0"

# Custom questionary style matching our theme
custom_style = Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:magenta bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:green'),
    ('separator', 'fg:gray'),
    ('instruction', 'fg:gray italic'),
    ('text', 'fg:white'),
    ('disabled', 'fg:gray italic'),
])


class Phase(Enum):
    """Deployment phases"""
    ANALYZE = "analyze"
    APP_STORES = "app_stores"
    FIREBASE = "firebase"
    OAUTH = "oauth"
    CONFIGURE = "configure"
    FASTLANE = "fastlane"
    CREDENTIALS = "credentials"
    GITHUB_ACTIONS = "github_actions"
    RUNNER_SETUP = "runner_setup"


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                              UI COMPONENTS                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

def show_banner():
    """Display the main banner"""
    console.clear()
    console.print(LOGO)
    console.print(Align.center(TAGLINE))
    console.print(Align.center(SUBTITLE))
    console.print(Align.center(f"[dim]v{VERSION}[/dim]"))
    console.print()


def create_phase_table() -> Table:
    """Create a table showing all phases"""
    table = Table(
        title="[bold cyan]📋 Deployment Phases[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold magenta",
        show_lines=True,
    )
    
    table.add_column("Phase", style="bold white", width=8)
    table.add_column("Name", style="cyan", width=20)
    table.add_column("Description", style="dim white", width=45)
    table.add_column("Status", style="white", width=12)
    
    phases = [
        ("1", "🔍 Analyze", "Scan Flutter app for permissions & features", "⏳ Pending"),
        ("2", "🏪 App Stores", "Setup App Store Connect & Play Console", "⏳ Pending"),
        ("3", "🔥 Firebase", "Configure Firebase project & services", "⏳ Pending"),
        ("4", "🔐 OAuth", "Setup authentication providers", "⏳ Pending"),
        ("5", "⚙️  Configure", "Interactive configuration wizard", "⏳ Pending"),
        ("6", "🚀 Fastlane", "Generate Fastlane automation", "⏳ Pending"),
        ("7", "🔑 Credentials", "Setup code signing & secrets", "⏳ Pending"),
        ("8", "🔄 GitHub Actions", "Generate CI/CD workflows", "⏳ Pending"),
        ("9", "🖥️  Runner", "Setup self-hosted Mac Mini runner", "⏳ Pending"),
    ]
    
    for phase in phases:
        table.add_row(*phase)
    
    return table


def show_main_menu() -> str:
    """Display the main menu and get user selection"""
    console.print()
    
    choices = [
        questionary.Choice("🚀  Start Full Deployment Pipeline", value="full"),
        questionary.Choice("📂  Select Flutter Project", value="select_project"),
        questionary.Separator(),
        questionary.Choice("🔍  Phase 1: Analyze Flutter App", value="analyze"),
        questionary.Choice("🏪  Phase 2: Setup App Stores", value="app_stores"),
        questionary.Choice("🔥  Phase 3: Configure Firebase", value="firebase"),
        questionary.Choice("🔐  Phase 4: Setup OAuth Providers", value="oauth"),
        questionary.Choice("⚙️   Phase 5: Configuration Wizard", value="configure"),
        questionary.Choice("🚀  Phase 6: Generate Fastlane", value="fastlane"),
        questionary.Choice("🔑  Phase 7: Setup Credentials", value="credentials"),
        questionary.Choice("🔄  Phase 8: Generate GitHub Actions", value="github_actions"),
        questionary.Choice("🖥️   Phase 9: Setup Mac Mini Runner", value="runner_setup"),
        questionary.Separator(),
        questionary.Choice("📊  View Current Configuration", value="view_config"),
        questionary.Choice("💾  Export Configuration", value="export"),
        questionary.Choice("📥  Import Configuration", value="import"),
        questionary.Separator(),
        questionary.Choice("❓  Help & Documentation", value="help"),
        questionary.Choice("👋  Exit", value="exit"),
    ]
    
    return questionary.select(
        "What would you like to do?",
        choices=choices,
        style=custom_style,
        instruction="(Use ↑↓ arrows, Enter to select)",
    ).ask()


def show_project_selector() -> Optional[str]:
    """Interactive project path selector"""
    console.print()
    console.print(Panel(
        "[bold]Select your Flutter project[/bold]\n\n"
        "Enter the path to your Flutter project directory.\n"
        "This should be the root folder containing [cyan]pubspec.yaml[/cyan]",
        title="[bold cyan]📂 Project Selection[/bold cyan]",
        border_style="cyan",
    ))
    
    # Get current directory as default
    default_path = os.getcwd()
    
    path = questionary.path(
        "Flutter project path:",
        default=default_path,
        only_directories=True,
        style=custom_style,
    ).ask()
    
    if path and validate_flutter_project(path):
        return path
    return None


def validate_flutter_project(path: str) -> bool:
    """Validate that path is a Flutter project"""
    pubspec = Path(path) / "pubspec.yaml"
    if not pubspec.exists():
        console.print(Panel(
            f"[red]Error:[/red] No pubspec.yaml found at:\n[dim]{path}[/dim]\n\n"
            "Please select a valid Flutter project directory.",
            title="[bold red]❌ Invalid Project[/bold red]",
            border_style="red",
        ))
        return False
    
    console.print(Panel(
        f"[green]✓[/green] Valid Flutter project found at:\n[cyan]{path}[/cyan]",
        title="[bold green]✅ Project Validated[/bold green]",
        border_style="green",
    ))
    return True


def show_progress_panel(title: str, steps: list[tuple[str, str]]):
    """Show a progress panel with animated steps"""
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="cyan", complete_style="green"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
        transient=False,
    ) as progress:
        for step_name, step_desc in steps:
            task = progress.add_task(f"{step_name}: {step_desc}", total=100)
            # Simulate work (replace with actual work)
            import time
            for _ in range(100):
                time.sleep(0.01)
                progress.update(task, advance=1)


def show_success_box(title: str, message: str):
    """Display a success message box"""
    console.print(Panel(
        f"[green]{message}[/green]",
        title=f"[bold green]✅ {title}[/bold green]",
        border_style="green",
        box=box.DOUBLE,
    ))


def show_error_box(title: str, message: str):
    """Display an error message box"""
    console.print(Panel(
        f"[red]{message}[/red]",
        title=f"[bold red]❌ {title}[/bold red]",
        border_style="red",
        box=box.DOUBLE,
    ))


def show_info_box(title: str, message: str):
    """Display an info message box"""
    console.print(Panel(
        f"[cyan]{message}[/cyan]",
        title=f"[bold cyan]ℹ️  {title}[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
    ))


def show_tree_view(title: str, items: dict) -> Tree:
    """Create a tree view of nested items"""
    tree = Tree(f"[bold cyan]{title}[/bold cyan]")
    
    def add_items(parent, items):
        for key, value in items.items():
            if isinstance(value, dict):
                branch = parent.add(f"[yellow]{key}[/yellow]")
                add_items(branch, value)
            elif isinstance(value, list):
                branch = parent.add(f"[yellow]{key}[/yellow]")
                for item in value:
                    branch.add(f"[dim]{item}[/dim]")
            else:
                parent.add(f"[green]{key}[/green]: [white]{value}[/white]")
    
    add_items(tree, items)
    return tree


def show_help():
    """Display help information"""
    help_md = """
# Flutter Deploy CLI - Help

## Overview
This tool automates the complete deployment pipeline for Flutter applications,
including iOS and Android builds, CI/CD setup, and app store deployment.

## Phases

### Phase 1: Analyze
Scans your Flutter project to determine:
- Required iOS permissions (Info.plist entries)
- Required Android permissions (AndroidManifest.xml)
- Detected packages and their requirements
- Entitlements needed for iOS

### Phase 2: App Stores
Automates setup of:
- Apple App Store Connect (via Fastlane produce)
- Google Play Console (via Play Developer API)

### Phase 3: Firebase
Configures:
- Firebase project creation
- iOS and Android app registration
- FCM, Analytics, Crashlytics setup

### Phase 4: OAuth Providers
Sets up authentication for:
- Google Sign-In
- Apple Sign-In
- Facebook Login
- Custom providers

### Phase 5: Configuration
Interactive wizard to gather:
- App metadata
- Environment configurations
- Team settings

### Phase 6: Fastlane
Generates:
- iOS Fastfile with lanes for beta/release
- Android Fastfile
- Matchfile for code signing

### Phase 7: Credentials
Sets up:
- Fastlane Match for iOS certificates
- Android keystore
- API keys and secrets

### Phase 8: GitHub Actions
Generates:
- CI workflow for testing
- CD workflow for deployment
- Self-hosted runner configuration

### Phase 9: Runner Setup
Configures your Mac Mini:
- GitHub Actions runner installation
- Xcode and dependencies
- Security and access

## Commands
- `flutter-deploy init` - Initialize new project
- `flutter-deploy analyze` - Run analysis only
- `flutter-deploy generate` - Generate all configs
- `flutter-deploy deploy` - Run full deployment

    """
    console.print(Markdown(help_md))
    
    questionary.press_any_key_to_continue(
        "Press any key to return to menu...",
        style=custom_style,
    ).ask()


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                              MAIN APPLICATION                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class FlutterDeployCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.project_path: Optional[str] = None
        self.config: dict = {}
        self.phase_status: dict[Phase, str] = {p: "pending" for p in Phase}
    
    def run(self):
        """Main application loop"""
        show_banner()
        console.print(Align.center(create_phase_table()))
        
        while True:
            choice = show_main_menu()
            
            if choice is None or choice == "exit":
                self.exit_app()
                break
            elif choice == "full":
                self.run_full_pipeline()
            elif choice == "select_project":
                self.project_path = show_project_selector()
            elif choice == "analyze":
                self.run_phase(Phase.ANALYZE)
            elif choice == "app_stores":
                self.run_phase(Phase.APP_STORES)
            elif choice == "firebase":
                self.run_phase(Phase.FIREBASE)
            elif choice == "oauth":
                self.run_phase(Phase.OAUTH)
            elif choice == "configure":
                self.run_phase(Phase.CONFIGURE)
            elif choice == "fastlane":
                self.run_phase(Phase.FASTLANE)
            elif choice == "credentials":
                self.run_phase(Phase.CREDENTIALS)
            elif choice == "github_actions":
                self.run_phase(Phase.GITHUB_ACTIONS)
            elif choice == "runner_setup":
                self.run_phase(Phase.RUNNER_SETUP)
            elif choice == "view_config":
                self.view_configuration()
            elif choice == "export":
                self.export_configuration()
            elif choice == "import":
                self.import_configuration()
            elif choice == "help":
                show_help()
            
            # Refresh display
            show_banner()
            console.print(Align.center(create_phase_table()))
    
    def run_full_pipeline(self):
        """Run the complete deployment pipeline"""
        if not self.project_path:
            self.project_path = show_project_selector()
            if not self.project_path:
                return
        
        console.print(Panel(
            "[bold]Starting full deployment pipeline...[/bold]\n\n"
            "This will guide you through all phases of deployment.\n"
            "You can cancel at any time with [bold red]Ctrl+C[/bold red]",
            title="[bold cyan]🚀 Full Pipeline[/bold cyan]",
            border_style="cyan",
        ))
        
        if not Confirm.ask("Continue with full pipeline?", console=console):
            return
        
        for phase in Phase:
            self.run_phase(phase)
    
    def run_phase(self, phase: Phase):
        """Run a specific phase"""
        if not self.project_path and phase != Phase.CONFIGURE:
            show_error_box(
                "No Project Selected",
                "Please select a Flutter project first."
            )
            self.project_path = show_project_selector()
            if not self.project_path:
                return
        
        console.print(f"\n[bold cyan]Running Phase: {phase.value}[/bold cyan]\n")
        
        # Import and run the appropriate phase handler
        try:
            if phase == Phase.ANALYZE:
                from flutter_deploy.analyzers.flutter_analyzer import run_analysis
                self.config['analysis'] = run_analysis(self.project_path)
            elif phase == Phase.CONFIGURE:
                from flutter_deploy.utils.config_wizard import run_wizard
                self.config.update(run_wizard(self.config))
            elif phase == Phase.FASTLANE:
                from flutter_deploy.generators.fastlane_generator import generate_fastlane
                generate_fastlane(self.project_path, self.config)
            elif phase == Phase.GITHUB_ACTIONS:
                from flutter_deploy.generators.github_actions_generator import generate_workflows
                generate_workflows(self.project_path, self.config)
            elif phase == Phase.RUNNER_SETUP:
                from flutter_deploy.generators.runner_setup import setup_runner
                setup_runner(self.config)
            # ... other phases
            
            self.phase_status[phase] = "complete"
            show_success_box(f"Phase {phase.value}", "Completed successfully!")
            
        except ImportError as e:
            # Module not yet implemented - show placeholder
            show_info_box(
                f"Phase: {phase.value}",
                f"This phase will be implemented.\nModule: {e}"
            )
        except Exception as e:
            self.phase_status[phase] = "error"
            show_error_box(f"Phase {phase.value} Error", str(e))
    
    def view_configuration(self):
        """Display current configuration"""
        if not self.config:
            show_info_box("Configuration", "No configuration loaded yet.")
            return
        
        tree = show_tree_view("Current Configuration", self.config)
        console.print(tree)
        
        questionary.press_any_key_to_continue(
            "Press any key to continue...",
            style=custom_style,
        ).ask()
    
    def export_configuration(self):
        """Export configuration to file"""
        import json
        
        if not self.config:
            show_error_box("Export Error", "No configuration to export.")
            return
        
        filename = questionary.text(
            "Export filename:",
            default="flutter-deploy-config.json",
            style=custom_style,
        ).ask()
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
            show_success_box("Export", f"Configuration exported to {filename}")
    
    def import_configuration(self):
        """Import configuration from file"""
        import json
        
        filename = questionary.path(
            "Import configuration file:",
            style=custom_style,
        ).ask()
        
        if filename and Path(filename).exists():
            try:
                with open(filename) as f:
                    self.config = json.load(f)
                show_success_box("Import", f"Configuration imported from {filename}")
            except Exception as e:
                show_error_box("Import Error", str(e))
    
    def exit_app(self):
        """Exit the application gracefully"""
        console.print()
        console.print(Panel(
            "[bold]Thanks for using Flutter Deploy CLI![/bold]\n\n"
            "[dim]May your builds be successful and your deploys be smooth.[/dim] 🚀",
            title="[bold magenta]👋 Goodbye![/bold magenta]",
            border_style="magenta",
            box=box.DOUBLE,
        ))


def main():
    """Entry point"""
    try:
        app = FlutterDeployCLI()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
