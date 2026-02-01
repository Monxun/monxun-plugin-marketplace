#!/usr/bin/env python3
"""GitHub Actions Workflow Generator"""

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def generate_ci_workflow(config: dict) -> str:
    """Generate CI workflow"""
    use_self_hosted = config.get('cicd', {}).get('use_self_hosted', False)
    runner_labels = config.get('cicd', {}).get('runner', {}).get('labels', ['self-hosted', 'macOS', 'ARM64'])
    runner = ', '.join(runner_labels) if use_self_hosted else 'macos-latest'
    
    return f'''name: CI - Test & Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{{{ github.workflow }}}}-${{{{ github.event.pull_request.number || github.ref }}}}
  cancel-in-progress: true

env:
  FLUTTER_VERSION: '3.19.0'

jobs:
  analyze:
    name: 🔍 Analyze
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
          cache: true
      - run: flutter pub get
      - run: flutter analyze --fatal-infos
      - run: dart format --set-exit-if-changed .

  test:
    name: 🧪 Test
    runs-on: ubuntu-latest
    needs: analyze
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
          cache: true
      - run: flutter pub get
      - run: flutter test --coverage

  build-ios:
    name: 🍎 Build iOS
    runs-on: [{runner}]
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
          cache: true
      - run: flutter pub get
      - run: flutter build ios --release --no-codesign

  build-android:
    name: 🤖 Build Android
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
          cache: true
      - run: flutter pub get
      - run: flutter build apk --release
      - run: flutter build appbundle --release
'''


def generate_cd_workflow(config: dict) -> str:
    """Generate CD workflow"""
    use_self_hosted = config.get('cicd', {}).get('use_self_hosted', False)
    runner_labels = config.get('cicd', {}).get('runner', {}).get('labels', ['self-hosted', 'macOS', 'ARM64'])
    runner = ', '.join(runner_labels) if use_self_hosted else 'macos-latest'
    
    return f'''name: CD - Deploy

on:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]
      platform:
        description: 'Platform to deploy'
        required: true
        default: 'both'
        type: choice
        options: [ios, android, both]

env:
  FLUTTER_VERSION: '3.19.0'

jobs:
  setup:
    name: 🔧 Setup
    runs-on: ubuntu-latest
    outputs:
      environment: ${{{{ steps.config.outputs.environment }}}}
      version: ${{{{ steps.config.outputs.version }}}}
    steps:
      - uses: actions/checkout@v4
      - id: config
        run: |
          if [[ "${{{{ github.event_name }}}}" == "workflow_dispatch" ]]; then
            echo "environment=${{{{ github.event.inputs.environment }}}}" >> $GITHUB_OUTPUT
          elif [[ "${{{{ github.ref }}}}" == refs/tags/v* ]]; then
            echo "environment=production" >> $GITHUB_OUTPUT
          else
            echo "environment=staging" >> $GITHUB_OUTPUT
          fi

  deploy-ios:
    name: 🍎 Deploy iOS
    runs-on: [{runner}]
    needs: setup
    environment: ${{{{ needs.setup.outputs.environment }}}}
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: ios
      - run: flutter pub get
      - working-directory: ios
        env:
          MATCH_PASSWORD: ${{{{ secrets.MATCH_PASSWORD }}}}
          APP_STORE_CONNECT_API_KEY_ID: ${{{{ secrets.APP_STORE_CONNECT_API_KEY_ID }}}}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{{{ secrets.APP_STORE_CONNECT_API_ISSUER_ID }}}}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{{{ secrets.APP_STORE_CONNECT_API_KEY_CONTENT }}}}
        run: bundle exec fastlane beta env:${{{{ needs.setup.outputs.environment }}}}

  deploy-android:
    name: 🤖 Deploy Android
    runs-on: ubuntu-latest
    needs: setup
    environment: ${{{{ needs.setup.outputs.environment }}}}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: android
      - run: flutter pub get
      - run: echo "${{{{ secrets.ANDROID_KEYSTORE_BASE64 }}}}" | base64 --decode > android/app/release.keystore
      - working-directory: android
        env:
          KEYSTORE_PATH: ${{{{ github.workspace }}}}/android/app/release.keystore
          KEYSTORE_PASSWORD: ${{{{ secrets.ANDROID_KEYSTORE_PASSWORD }}}}
          KEY_ALIAS: ${{{{ secrets.ANDROID_KEY_ALIAS }}}}
          KEY_PASSWORD: ${{{{ secrets.ANDROID_KEY_PASSWORD }}}}
          PLAY_STORE_JSON_KEY: ${{{{ secrets.PLAY_STORE_JSON_KEY }}}}
        run: |
          echo '${{{{ secrets.PLAY_STORE_JSON_KEY }}}}' > play-store-key.json
          bundle exec fastlane deploy_${{{{ needs.setup.outputs.environment }}}}
'''


def generate_release_workflow(config: dict) -> str:
    """Generate release workflow"""
    use_self_hosted = config.get('cicd', {}).get('use_self_hosted', False)
    runner_labels = config.get('cicd', {}).get('runner', {}).get('labels', ['self-hosted', 'macOS', 'ARM64'])
    runner = ', '.join(runner_labels) if use_self_hosted else 'macos-latest'
    
    return f'''name: Release - Production

on:
  release:
    types: [published]

env:
  FLUTTER_VERSION: '3.19.0'

jobs:
  release-ios:
    name: 🍎 Release iOS
    runs-on: [{runner}]
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: ios
      - run: flutter pub get
      - working-directory: ios
        env:
          MATCH_PASSWORD: ${{{{ secrets.MATCH_PASSWORD }}}}
          APP_STORE_CONNECT_API_KEY_ID: ${{{{ secrets.APP_STORE_CONNECT_API_KEY_ID }}}}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{{{ secrets.APP_STORE_CONNECT_API_ISSUER_ID }}}}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{{{ secrets.APP_STORE_CONNECT_API_KEY_CONTENT }}}}
        run: bundle exec fastlane release

  release-android:
    name: 🤖 Release Android
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{{{ env.FLUTTER_VERSION }}}}
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: android
      - run: flutter pub get
      - run: echo "${{{{ secrets.ANDROID_KEYSTORE_BASE64 }}}}" | base64 --decode > android/app/release.keystore
      - working-directory: android
        env:
          KEYSTORE_PATH: ${{{{ github.workspace }}}}/android/app/release.keystore
          KEYSTORE_PASSWORD: ${{{{ secrets.ANDROID_KEYSTORE_PASSWORD }}}}
          KEY_ALIAS: ${{{{ secrets.ANDROID_KEY_ALIAS }}}}
          KEY_PASSWORD: ${{{{ secrets.ANDROID_KEY_PASSWORD }}}}
          PLAY_STORE_JSON_KEY: ${{{{ secrets.PLAY_STORE_JSON_KEY }}}}
        run: |
          echo '${{{{ secrets.PLAY_STORE_JSON_KEY }}}}' > play-store-key.json
          bundle exec fastlane release
'''


def generate_runner_health_workflow() -> str:
    """Generate runner health check workflow"""
    return '''name: Runner - Health Check

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  health-check:
    name: 🏥 Health Check
    runs-on: [self-hosted, macOS, ARM64]
    steps:
      - name: System Info
        run: |
          echo "macOS: $(sw_vers -productVersion)"
          echo "Xcode: $(xcodebuild -version | head -1)"
          echo "Flutter: $(flutter --version | head -1)"
          echo "Disk: $(df -h / | tail -1)"
'''


def generate_dependabot_config() -> str:
    """Generate Dependabot configuration"""
    return '''version: 2
updates:
  - package-ecosystem: "pub"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "bundler"
    directory: "/ios"
    schedule:
      interval: "weekly"
  - package-ecosystem: "bundler"
    directory: "/android"
    schedule:
      interval: "weekly"
'''


def generate_workflows(project_path: str, config: dict):
    """Generate all GitHub Actions workflows"""
    workflows_dir = Path(project_path) / ".github" / "workflows"
    github_dir = Path(project_path) / ".github"
    
    console.print(Panel("[bold]Generating GitHub Actions workflows...[/bold]",
                       title="[bold cyan]🔄 GitHub Actions Generator[/bold cyan]", border_style="cyan"))
    
    with Progress(SpinnerColumn(style="cyan"), TextColumn("[bold cyan]{task.description}[/bold cyan]"),
                  console=console, transient=False) as progress:
        
        task = progress.add_task("Creating directories...", total=None)
        workflows_dir.mkdir(parents=True, exist_ok=True)
        progress.update(task, completed=True, description="✓ Directories created")
        
        task = progress.add_task("Generating CI workflow...", total=None)
        (workflows_dir / "ci.yml").write_text(generate_ci_workflow(config))
        progress.update(task, completed=True, description="✓ CI workflow generated")
        
        task = progress.add_task("Generating CD workflow...", total=None)
        (workflows_dir / "cd.yml").write_text(generate_cd_workflow(config))
        progress.update(task, completed=True, description="✓ CD workflow generated")
        
        task = progress.add_task("Generating release workflow...", total=None)
        (workflows_dir / "release.yml").write_text(generate_release_workflow(config))
        progress.update(task, completed=True, description="✓ Release workflow generated")
        
        if config.get('cicd', {}).get('use_self_hosted', False):
            task = progress.add_task("Generating runner workflow...", total=None)
            (workflows_dir / "runner-health.yml").write_text(generate_runner_health_workflow())
            progress.update(task, completed=True, description="✓ Runner workflow generated")
        
        task = progress.add_task("Generating Dependabot config...", total=None)
        (github_dir / "dependabot.yml").write_text(generate_dependabot_config())
        progress.update(task, completed=True, description="✓ Dependabot config generated")
    
    console.print(Panel(f"[green]✓ All GitHub Actions workflows generated![/green]",
                       title="[bold green]✅ Complete[/bold green]", border_style="green"))
