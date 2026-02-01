#!/usr/bin/env python3
"""Self-Hosted Runner Setup Scripts"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()


def generate_setup_script(config: dict) -> str:
    """Generate Mac Mini setup script"""
    runner_labels = ','.join(config.get('cicd', {}).get('runner', {}).get('labels', ['self-hosted', 'macOS', 'ARM64']))
    
    return f'''#!/bin/bash
# Mac Mini Self-Hosted Runner Setup Script
set -e

echo "🚀 Setting up Mac Mini as GitHub Actions Runner..."

# Install Homebrew
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install dependencies
brew install git gh jq wget cocoapods fastlane rbenv ruby-build || true

# Setup Ruby
if ! rbenv versions | grep -q 3.2; then
    rbenv install 3.2.2
fi
rbenv global 3.2.2
gem install bundler

# Install Java
brew install openjdk@17 || true

# Install Flutter
if [[ ! -d "$HOME/flutter" ]]; then
    git clone https://github.com/flutter/flutter.git -b stable "$HOME/flutter"
fi
export PATH="$PATH:$HOME/flutter/bin"
flutter doctor

# Setup Xcode
sudo xcodebuild -license accept || true

# Download GitHub Actions Runner
RUNNER_DIR="$HOME/actions-runner"
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r '.tag_name' | sed 's/v//')
ARCH=$(uname -m)
[[ "$ARCH" == "arm64" ]] && RUNNER_ARCH="osx-arm64" || RUNNER_ARCH="osx-x64"

curl -o actions-runner.tar.gz -L "https://github.com/actions/runner/releases/download/v$RUNNER_VERSION/actions-runner-$RUNNER_ARCH-$RUNNER_VERSION.tar.gz"
tar xzf actions-runner.tar.gz
rm actions-runner.tar.gz

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to GitHub repo → Settings → Actions → Runners"
echo "2. Click 'New self-hosted runner' and copy the token"
echo "3. Run: ./config.sh --url https://github.com/OWNER/REPO --token YOUR_TOKEN --labels {runner_labels}"
echo "4. Run: sudo ./svc.sh install && sudo ./svc.sh start"
'''


def generate_maintenance_script() -> str:
    """Generate maintenance script"""
    return '''#!/bin/bash
# Runner Maintenance Script

case "$1" in
    health)
        echo "🏥 Health Check"
        echo "macOS: $(sw_vers -productVersion)"
        echo "Xcode: $(xcodebuild -version | head -1)"
        echo "Flutter: $(flutter --version | head -1)"
        echo "Disk: $(df -h / | tail -1)"
        ;;
    cleanup)
        echo "🧹 Cleaning caches..."
        rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null || true
        rm -rf ~/.gradle/caches/build-cache-* 2>/dev/null || true
        flutter clean 2>/dev/null || true
        echo "✅ Cleanup complete"
        ;;
    restart)
        echo "🔄 Restarting runner..."
        cd ~/actions-runner
        sudo ./svc.sh stop
        sudo ./svc.sh start
        ;;
    *)
        echo "Usage: $0 {health|cleanup|restart}"
        ;;
esac
'''


def generate_env_template() -> str:
    """Generate environment template"""
    return '''# Runner Environment Variables
# Place at ~/actions-runner/.env

# iOS
MATCH_PASSWORD=your_match_password
APP_STORE_CONNECT_API_KEY_ID=your_key_id
APP_STORE_CONNECT_API_ISSUER_ID=your_issuer_id

# Android
KEYSTORE_PATH=$HOME/keystores/release.keystore
KEYSTORE_PASSWORD=your_password
KEY_ALIAS=release
KEY_PASSWORD=your_password
PLAY_STORE_JSON_KEY=$HOME/keystores/play-store-key.json
'''


def setup_runner(config: dict):
    """Generate runner setup files"""
    output_dir = Path(config.get('project_path', '.')) / "runner-setup"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel("[bold]Generating Mac Mini runner setup files...[/bold]",
                       title="[bold cyan]🖥️ Runner Setup[/bold cyan]", border_style="cyan"))
    
    with Progress(SpinnerColumn(style="cyan"), TextColumn("[bold cyan]{task.description}[/bold cyan]"),
                  console=console, transient=False) as progress:
        
        task = progress.add_task("Generating setup script...", total=None)
        script = output_dir / "setup-runner.sh"
        script.write_text(generate_setup_script(config))
        script.chmod(0o755)
        progress.update(task, completed=True, description="✓ Setup script generated")
        
        task = progress.add_task("Generating maintenance script...", total=None)
        maint = output_dir / "maintenance.sh"
        maint.write_text(generate_maintenance_script())
        maint.chmod(0o755)
        progress.update(task, completed=True, description="✓ Maintenance script generated")
        
        task = progress.add_task("Generating env template...", total=None)
        (output_dir / "runner.env.template").write_text(generate_env_template())
        progress.update(task, completed=True, description="✓ Env template generated")
    
    console.print(Panel(f"[green]✓ Runner setup files generated in:[/green]\n[cyan]{output_dir}[/cyan]",
                       title="[bold green]✅ Complete[/bold green]", border_style="green"))
    
    table = Table(title="[bold cyan]📋 Mac Mini Requirements[/bold cyan]", box=box.ROUNDED, border_style="cyan")
    table.add_column("Requirement", style="white")
    table.add_column("Recommended", style="cyan")
    table.add_row("macOS", "14.0+ (Sonoma)")
    table.add_row("Xcode", "15.0+")
    table.add_row("RAM", "16GB+")
    table.add_row("Storage", "256GB+ SSD")
    console.print(table)
