# 🚀 Flutter Deploy CLI

```
    ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗ 
    ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
    █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝
    ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
    ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║
    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
    ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
```

**A beautiful CLI tool for fully automated Flutter app deployment to iOS and Android**

## ✨ Features

- 🔍 **Smart Analysis** - Automatically detects permissions, features, and requirements
- 🏪 **App Store Setup** - Automates App Store Connect and Google Play Console
- 🔥 **Firebase Integration** - Sets up Firebase with per-environment projects
- 🔐 **OAuth Providers** - Configures Google, Apple, Facebook auth
- 🚀 **Fastlane Generation** - Creates complete Fastlane configurations
- 🔄 **GitHub Actions** - Generates CI/CD workflows with self-hosted runner support
- 🖥️ **Mac Mini Runner** - Scripts to set up your build machine
- 🎨 **Beautiful UI** - Stunning terminal interface

## 📦 Installation

```bash
pip install -e .
```

## 🚀 Quick Start

```bash
flutter-deploy
# or
fd
```

## 📋 Deployment Phases

1. **Analyze** - Scans project for permissions and features
2. **App Stores** - Sets up App Store Connect and Play Console
3. **Firebase** - Configures Firebase project and services
4. **OAuth** - Sets up authentication providers
5. **Configure** - Interactive configuration wizard
6. **Fastlane** - Generates Fastlane files
7. **Credentials** - Sets up code signing
8. **GitHub Actions** - Generates CI/CD workflows
9. **Runner Setup** - Configures self-hosted Mac Mini

## 🖥️ Self-Hosted Runner Requirements

| Requirement | Recommended |
|-------------|-------------|
| macOS | 14.0+ (Sonoma) |
| Xcode | 15.0+ |
| RAM | 16GB+ |
| Storage | 256GB+ SSD |

## 📄 License

MIT License
