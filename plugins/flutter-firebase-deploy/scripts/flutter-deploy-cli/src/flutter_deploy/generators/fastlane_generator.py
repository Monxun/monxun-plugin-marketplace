#!/usr/bin/env python3
"""Fastlane Configuration Generator"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from questionary import Style

console = Console()
custom_style = Style([('qmark', 'fg:cyan bold'), ('question', 'fg:white bold'), ('answer', 'fg:magenta bold'), ('pointer', 'fg:cyan bold')])


def generate_ios_fastfile(config: dict) -> str:
    """Generate iOS Fastfile content"""
    app_identifier = config.get('ios_bundle_id', 'com.example.app')
    team_id = config.get('apple_team_id', 'YOUR_TEAM_ID')
    use_match = config.get('code_signing', {}).get('ios_method') == 'match'
    environments = config.get('environments', ['dev', 'staging', 'prod'])
    
    match_config = ""
    if use_match:
        match_config = f'''
  desc "Sync development certificates"
  lane :sync_dev_certs do
    match(type: "development", app_identifier: "{app_identifier}", readonly: is_ci)
  end

  desc "Sync distribution certificates"
  lane :sync_dist_certs do
    match(type: "appstore", app_identifier: "{app_identifier}", readonly: is_ci)
  end
'''
    
    env_lanes = ""
    for env in environments:
        env_lanes += f'''
  desc "Build {env} version"
  lane :build_{env} do
    setup_ci if is_ci
    {"sync_dist_certs" if use_match else "# Manual signing configured"}
    increment_build_number(build_number: ENV["BUILD_NUMBER"] || Time.now.strftime("%Y%m%d%H%M"))
    build_ios_app(scheme: "Runner", configuration: "Release", export_method: "app-store",
      output_directory: "./build/ios/{env}", output_name: "app-{env}.ipa", clean: true)
  end
'''
    
    return f'''# Flutter Deploy - iOS Fastfile
default_platform(:ios)

APP_IDENTIFIER = "{app_identifier}"
TEAM_ID = "{team_id}"

before_all do |lane|
  Dir.chdir("..") if File.basename(Dir.pwd) == "fastlane"
end

platform :ios do
{match_config}
{env_lanes}
  desc "Upload to TestFlight"
  lane :beta do |options|
    env = options[:env] || "staging"
    build_path = "./build/ios/#{{env}}/app-#{{env}}.ipa"
    send("build_#{{env}}") unless File.exist?(build_path)
    upload_to_testflight(ipa: build_path, skip_waiting_for_build_processing: true)
  end

  desc "Deploy to App Store"
  lane :release do
    build_prod
    upload_to_app_store(ipa: "./build/ios/prod/app-prod.ipa", skip_screenshots: true, submit_for_review: false)
  end
end
'''


def generate_android_fastfile(config: dict) -> str:
    """Generate Android Fastfile content"""
    package_name = config.get('android_package_name', 'com.example.app')
    environments = config.get('environments', ['dev', 'staging', 'prod'])
    
    env_lanes = ""
    for env in environments:
        track = "internal" if env == "dev" else ("alpha" if env == "staging" else "production")
        env_lanes += f'''
  desc "Build {env} version"
  lane :build_{env} do
    gradle(task: "clean")
    gradle(task: "bundle", build_type: "Release", properties: {{
      "android.injected.signing.store.file" => ENV["KEYSTORE_PATH"],
      "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
      "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
      "android.injected.signing.key.password" => ENV["KEY_PASSWORD"],
    }})
  end

  desc "Deploy {env} to Play Store"
  lane :deploy_{env} do
    build_{env}
    upload_to_play_store(track: "{track}", aab: "./app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true, skip_upload_images: true, json_key: ENV["PLAY_STORE_JSON_KEY"])
  end
'''
    
    return f'''# Flutter Deploy - Android Fastfile
default_platform(:android)

PACKAGE_NAME = "{package_name}"

before_all do |lane|
  Dir.chdir("..") if File.basename(Dir.pwd) == "fastlane"
end

platform :android do
{env_lanes}
  desc "Deploy to Production"
  lane :release do
    deploy_prod
  end
end
'''


def generate_ios_appfile(config: dict) -> str:
    return f'''app_identifier("{config.get('ios_bundle_id', 'com.example.app')}")
apple_id("{config.get('team_email', 'team@example.com')}")
team_id("{config.get('apple_team_id', 'YOUR_TEAM_ID')}")
'''


def generate_android_appfile(config: dict) -> str:
    return f'''package_name("{config.get('android_package_name', 'com.example.app')}")
json_key_file(ENV["PLAY_STORE_JSON_KEY"] || "play-store-key.json")
'''


def generate_matchfile(config: dict) -> str:
    match_config = config.get('code_signing', {}).get('match', {})
    return f'''git_url("{match_config.get('git_url', 'git@github.com:your-org/certificates.git')}")
storage_mode("{match_config.get('storage_mode', 'git')}")
type("appstore")
app_identifier(["{config.get('ios_bundle_id', 'com.example.app')}"])
username("{config.get('team_email', 'team@example.com')}")
team_id("{config.get('apple_team_id', 'YOUR_TEAM_ID')}")
'''


def generate_gemfile() -> str:
    return '''source "https://rubygems.org"
gem "fastlane", "~> 2.219"
gem "cocoapods", "~> 1.14"
'''


def generate_pluginfile() -> str:
    return '''gem 'fastlane-plugin-firebase_app_distribution'
gem 'fastlane-plugin-versioning'
'''


def generate_fastlane(project_path: str, config: dict):
    """Generate all Fastlane configurations"""
    ios_dir = Path(project_path) / "ios" / "fastlane"
    android_dir = Path(project_path) / "android" / "fastlane"
    
    console.print(Panel("[bold]Generating Fastlane configurations...[/bold]",
                       title="[bold cyan]🚀 Fastlane Generator[/bold cyan]", border_style="cyan"))
    
    with Progress(SpinnerColumn(style="cyan"), TextColumn("[bold cyan]{task.description}[/bold cyan]"),
                  console=console, transient=False) as progress:
        
        task = progress.add_task("Creating directories...", total=None)
        ios_dir.mkdir(parents=True, exist_ok=True)
        android_dir.mkdir(parents=True, exist_ok=True)
        progress.update(task, completed=True, description="✓ Directories created")
        
        task = progress.add_task("Generating iOS Fastfile...", total=None)
        (ios_dir / "Fastfile").write_text(generate_ios_fastfile(config))
        progress.update(task, completed=True, description="✓ iOS Fastfile generated")
        
        task = progress.add_task("Generating iOS Appfile...", total=None)
        (ios_dir / "Appfile").write_text(generate_ios_appfile(config))
        progress.update(task, completed=True, description="✓ iOS Appfile generated")
        
        if config.get('code_signing', {}).get('ios_method') == 'match':
            task = progress.add_task("Generating Matchfile...", total=None)
            (ios_dir / "Matchfile").write_text(generate_matchfile(config))
            progress.update(task, completed=True, description="✓ Matchfile generated")
        
        task = progress.add_task("Generating Android Fastfile...", total=None)
        (android_dir / "Fastfile").write_text(generate_android_fastfile(config))
        progress.update(task, completed=True, description="✓ Android Fastfile generated")
        
        task = progress.add_task("Generating Android Appfile...", total=None)
        (android_dir / "Appfile").write_text(generate_android_appfile(config))
        progress.update(task, completed=True, description="✓ Android Appfile generated")
        
        task = progress.add_task("Generating Gemfiles...", total=None)
        (ios_dir.parent / "Gemfile").write_text(generate_gemfile())
        (android_dir.parent / "Gemfile").write_text(generate_gemfile())
        progress.update(task, completed=True, description="✓ Gemfiles generated")
        
        task = progress.add_task("Generating Pluginfiles...", total=None)
        (ios_dir / "Pluginfile").write_text(generate_pluginfile())
        (android_dir / "Pluginfile").write_text(generate_pluginfile())
        progress.update(task, completed=True, description="✓ Pluginfiles generated")
    
    console.print(Panel(f"[green]✓ All Fastlane configurations generated![/green]\n\n"
                       f"[bold]iOS:[/bold] {ios_dir}\n[bold]Android:[/bold] {android_dir}",
                       title="[bold green]✅ Complete[/bold green]", border_style="green"))
