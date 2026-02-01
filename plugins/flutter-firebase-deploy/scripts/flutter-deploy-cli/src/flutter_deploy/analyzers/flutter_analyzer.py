#!/usr/bin/env python3
"""
Flutter Project Analyzer
Scans Flutter projects to detect permissions, features, and requirements
"""

import re
from pathlib import Path
from dataclasses import dataclass, field

import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

# Permission mappings
IOS_PERMISSION_MAP = {
    "camera": {"key": "NSCameraUsageDescription", "description": "This app needs camera access to"},
    "image_picker": {"key": "NSPhotoLibraryUsageDescription", "description": "This app needs photo library access to", "related_keys": ["NSCameraUsageDescription", "NSMicrophoneUsageDescription"]},
    "photo_manager": {"key": "NSPhotoLibraryUsageDescription", "description": "This app needs photo library access to"},
    "video_player": {"key": "NSAppTransportSecurity", "description": "Allow arbitrary loads for video streaming"},
    "geolocator": {"key": "NSLocationWhenInUseUsageDescription", "description": "This app needs location access to", "related_keys": ["NSLocationAlwaysAndWhenInUseUsageDescription"]},
    "location": {"key": "NSLocationWhenInUseUsageDescription", "description": "This app needs location access to"},
    "google_maps_flutter": {"key": "NSLocationWhenInUseUsageDescription", "description": "This app needs location for maps to"},
    "audio_session": {"key": "NSMicrophoneUsageDescription", "description": "This app needs microphone access to", "background_modes": ["audio"]},
    "just_audio": {"background_modes": ["audio"]},
    "record": {"key": "NSMicrophoneUsageDescription", "description": "This app needs microphone access to"},
    "contacts_service": {"key": "NSContactsUsageDescription", "description": "This app needs contacts access to"},
    "flutter_contacts": {"key": "NSContactsUsageDescription", "description": "This app needs contacts access to"},
    "device_calendar": {"key": "NSCalendarsUsageDescription", "description": "This app needs calendar access to"},
    "flutter_blue": {"key": "NSBluetoothAlwaysUsageDescription", "description": "This app needs Bluetooth access to", "related_keys": ["NSBluetoothPeripheralUsageDescription"]},
    "flutter_reactive_ble": {"key": "NSBluetoothAlwaysUsageDescription", "description": "This app needs Bluetooth access to"},
    "health": {"key": "NSHealthShareUsageDescription", "description": "This app needs HealthKit access to", "related_keys": ["NSHealthUpdateUsageDescription"], "entitlements": ["com.apple.developer.healthkit"]},
    "pedometer": {"key": "NSMotionUsageDescription", "description": "This app needs motion data access to"},
    "local_auth": {"key": "NSFaceIDUsageDescription", "description": "This app uses Face ID for"},
    "firebase_messaging": {"entitlements": ["aps-environment"], "background_modes": ["remote-notification"]},
    "flutter_local_notifications": {"background_modes": ["remote-notification"]},
    "onesignal_flutter": {"entitlements": ["aps-environment"], "background_modes": ["remote-notification"]},
    "in_app_purchase": {"entitlements": ["com.apple.developer.in-app-payments"]},
    "purchases_flutter": {"entitlements": ["com.apple.developer.in-app-payments"]},
    "workmanager": {"background_modes": ["fetch", "processing"]},
    "background_fetch": {"background_modes": ["fetch"]},
    "sign_in_with_apple": {"entitlements": ["com.apple.developer.applesignin"]},
    "google_sign_in": {"url_schemes": ["REVERSED_CLIENT_ID"]},
}

ANDROID_PERMISSION_MAP = {
    "camera": ["android.permission.CAMERA"],
    "image_picker": ["android.permission.CAMERA", "android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_EXTERNAL_STORAGE"],
    "geolocator": ["android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION"],
    "location": ["android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION"],
    "contacts_service": ["android.permission.READ_CONTACTS", "android.permission.WRITE_CONTACTS"],
    "flutter_blue": ["android.permission.BLUETOOTH", "android.permission.BLUETOOTH_ADMIN", "android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_CONNECT"],
    "record": ["android.permission.RECORD_AUDIO"],
    "local_auth": ["android.permission.USE_BIOMETRIC"],
    "flutter_local_notifications": ["android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.VIBRATE"],
}


@dataclass
class AnalysisResult:
    """Results from Flutter project analysis"""
    project_name: str = ""
    project_path: str = ""
    dependencies: list = field(default_factory=list)
    dev_dependencies: list = field(default_factory=list)
    ios_permissions: dict = field(default_factory=dict)
    ios_entitlements: list = field(default_factory=list)
    ios_background_modes: list = field(default_factory=list)
    ios_url_schemes: list = field(default_factory=list)
    android_permissions: list = field(default_factory=list)
    android_features: list = field(default_factory=list)
    uses_firebase: bool = False
    firebase_services: list = field(default_factory=list)
    auth_providers: list = field(default_factory=list)
    features: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def parse_pubspec(project_path: str) -> dict:
    """Parse pubspec.yaml file"""
    pubspec_path = Path(project_path) / "pubspec.yaml"
    if not pubspec_path.exists():
        raise FileNotFoundError(f"pubspec.yaml not found at {project_path}")
    with open(pubspec_path) as f:
        return yaml.safe_load(f)


def analyze_dependencies(pubspec: dict) -> tuple:
    """Extract dependencies from pubspec"""
    deps = list(pubspec.get("dependencies", {}).keys())
    dev_deps = list(pubspec.get("dev_dependencies", {}).keys())
    deps = [d for d in deps if d not in ["flutter"]]
    dev_deps = [d for d in dev_deps if d not in ["flutter_test", "flutter_lints"]]
    return deps, dev_deps


def analyze_ios_requirements(dependencies: list) -> tuple:
    """Determine iOS permissions and entitlements"""
    permissions = {}
    entitlements = set()
    background_modes = set()
    url_schemes = []
    
    for dep in dependencies:
        if dep in IOS_PERMISSION_MAP:
            config = IOS_PERMISSION_MAP[dep]
            if "key" in config:
                permissions[config["key"]] = f"{config.get('description', 'Required for')} provide functionality."
            for related in config.get("related_keys", []):
                if related not in permissions:
                    permissions[related] = "Required for app functionality."
            entitlements.update(config.get("entitlements", []))
            background_modes.update(config.get("background_modes", []))
            url_schemes.extend(config.get("url_schemes", []))
    
    return permissions, list(entitlements), list(background_modes), url_schemes


def analyze_android_requirements(dependencies: list) -> tuple:
    """Determine Android permissions"""
    permissions = set()
    features = set()
    
    for dep in dependencies:
        if dep in ANDROID_PERMISSION_MAP:
            permissions.update(ANDROID_PERMISSION_MAP[dep])
    
    if "android.permission.CAMERA" in permissions:
        features.add("android.hardware.camera")
    if "android.permission.ACCESS_FINE_LOCATION" in permissions:
        features.add("android.hardware.location.gps")
    if "android.permission.BLUETOOTH" in permissions:
        features.add("android.hardware.bluetooth")
    
    return list(permissions), list(features)


def detect_firebase_usage(dependencies: list) -> tuple:
    """Detect Firebase services"""
    firebase_packages = ["firebase_core", "firebase_auth", "firebase_analytics", "firebase_crashlytics", 
                        "cloud_firestore", "firebase_storage", "firebase_messaging", "firebase_remote_config",
                        "firebase_dynamic_links", "firebase_database", "firebase_performance"]
    services = [pkg for pkg in dependencies if pkg in firebase_packages]
    return len(services) > 0, services


def detect_auth_providers(dependencies: list) -> list:
    """Detect authentication providers"""
    auth_mapping = {
        "google_sign_in": "Google", "sign_in_with_apple": "Apple", "flutter_facebook_auth": "Facebook",
        "twitter_login": "Twitter", "github_sign_in": "GitHub", "firebase_auth": "Firebase Auth",
    }
    return [auth_mapping[dep] for dep in dependencies if dep in auth_mapping]


def detect_features(dependencies: list) -> list:
    """Detect high-level features"""
    feature_mapping = {
        "in_app_purchase": "In-App Purchases", "purchases_flutter": "In-App Purchases (RevenueCat)",
        "google_maps": "Google Maps", "video_player": "Video Playback", "camera": "Camera",
        "image_picker": "Image Picker", "local_auth": "Biometric Authentication",
        "firebase_messaging": "Push Notifications", "geolocator": "Location Services",
    }
    features = []
    for dep in dependencies:
        for pattern, feature in feature_mapping.items():
            if pattern in dep and feature not in features:
                features.append(feature)
    return features


def run_analysis(project_path: str) -> dict:
    """Run complete analysis on Flutter project"""
    result = AnalysisResult()
    result.project_path = project_path
    
    with Progress(SpinnerColumn(style="cyan"), TextColumn("[bold cyan]{task.description}[/bold cyan]"), 
                  console=console, transient=True) as progress:
        
        task = progress.add_task("Parsing pubspec.yaml...", total=None)
        pubspec = parse_pubspec(project_path)
        result.project_name = pubspec.get("name", "unknown")
        progress.update(task, completed=True)
        
        task = progress.add_task("Analyzing dependencies...", total=None)
        result.dependencies, result.dev_dependencies = analyze_dependencies(pubspec)
        progress.update(task, completed=True)
        
        task = progress.add_task("Detecting iOS requirements...", total=None)
        result.ios_permissions, result.ios_entitlements, result.ios_background_modes, result.ios_url_schemes = analyze_ios_requirements(result.dependencies)
        progress.update(task, completed=True)
        
        task = progress.add_task("Detecting Android requirements...", total=None)
        result.android_permissions, result.android_features = analyze_android_requirements(result.dependencies)
        progress.update(task, completed=True)
        
        task = progress.add_task("Detecting Firebase usage...", total=None)
        result.uses_firebase, result.firebase_services = detect_firebase_usage(result.dependencies)
        progress.update(task, completed=True)
        
        task = progress.add_task("Detecting auth providers...", total=None)
        result.auth_providers = detect_auth_providers(result.dependencies)
        progress.update(task, completed=True)
        
        task = progress.add_task("Detecting features...", total=None)
        result.features = detect_features(result.dependencies)
        progress.update(task, completed=True)
    
    display_analysis_results(result)
    
    return {
        "project_name": result.project_name,
        "project_path": result.project_path,
        "dependencies": result.dependencies,
        "ios": {"permissions": result.ios_permissions, "entitlements": result.ios_entitlements, 
                "background_modes": result.ios_background_modes, "url_schemes": result.ios_url_schemes},
        "android": {"permissions": result.android_permissions, "features": result.android_features},
        "firebase": {"enabled": result.uses_firebase, "services": result.firebase_services},
        "auth_providers": result.auth_providers,
        "features": result.features,
        "warnings": result.warnings,
    }


def display_analysis_results(result: AnalysisResult):
    """Display analysis results"""
    console.print()
    console.print(Panel(
        f"[bold white]Name:[/bold white] [cyan]{result.project_name}[/cyan]\n"
        f"[bold white]Path:[/bold white] [dim]{result.project_path}[/dim]\n"
        f"[bold white]Dependencies:[/bold white] [green]{len(result.dependencies)}[/green] packages",
        title="[bold cyan]📦 Project Information[/bold cyan]", border_style="cyan"))
    
    if result.ios_permissions or result.ios_entitlements or result.ios_background_modes:
        ios_table = Table(title="[bold cyan]🍎 iOS Requirements[/bold cyan]", box=box.ROUNDED, border_style="cyan", show_lines=True)
        ios_table.add_column("Type", style="bold yellow", width=12)
        ios_table.add_column("Key/Value", style="white", width=32)
        ios_table.add_column("Description", style="dim", width=24)
        for key, desc in result.ios_permissions.items():
            ios_table.add_row("Permission", key, desc[:50] + "..." if len(desc) > 50 else desc)
        for ent in result.ios_entitlements:
            ios_table.add_row("Entitlement", ent, "Enable in Xcode capabilities")
        for mode in result.ios_background_modes:
            ios_table.add_row("Background", mode, "Add to Info.plist UIBackgroundModes")
        console.print(ios_table)
    
    if result.android_permissions:
        android_table = Table(title="[bold green]🤖 Android Requirements[/bold green]", box=box.ROUNDED, border_style="green")
        android_table.add_column("Permission", style="white")
        for perm in result.android_permissions:
            android_table.add_row(perm)
        console.print(android_table)
    
    if result.uses_firebase:
        console.print(Panel("\n".join([f"• [cyan]{svc}[/cyan]" for svc in result.firebase_services]),
                          title="[bold orange1]🔥 Firebase Services[/bold orange1]", border_style="orange1"))
    
    if result.auth_providers:
        console.print(Panel("\n".join([f"• [magenta]{p}[/magenta]" for p in result.auth_providers]),
                          title="[bold magenta]🔐 Auth Providers[/bold magenta]", border_style="magenta"))
    
    if result.features:
        console.print(Panel(" • ".join([f"[green]{f}[/green]" for f in result.features]),
                          title="[bold green]✨ Detected Features[/bold green]", border_style="green"))
