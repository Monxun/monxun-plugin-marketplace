<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugins-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHoiLz48L3N2Zz4=" alt="Claude Code Plugins"/>
</p>

<h1 align="center">Claude Code Plugins</h1>

<p align="center">
  <strong>A collection of production-ready plugins for Claude Code</strong>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-plugin-factory">Plugin Factory</a> •
  <a href="#-heuristics-framework">Heuristics Framework</a> •
  <a href="#-akashic-knowledge">Akashic Knowledge</a> •
  <a href="#-flutter-firebase-deploy">Flutter Firebase Deploy</a> •
  <a href="#-unity-vr-dev">Unity VR Dev</a> •
  <a href="#-architecture">Architecture</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Claude_Code-1.0.33+-orange?style=flat-square" alt="Claude Code"/>
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square" alt="Python"/>
</p>

---

## Overview

This repository contains a **marketplace of production-ready Claude Code plugins** distributed via `monxun-marketplace`. Each plugin leverages multi-agent orchestration, research-driven methodologies, and progressive disclosure patterns.

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              MONXUN MARKETPLACE                                        │
├───────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  🏭  PLUGIN FACTORY           🧠  HEURISTICS FRAMEWORK                                │
│  "Build plugins that          "Discover, validate, and                                │
│   build plugins"               document heuristics"                                   │
│  10 Agents • 6 Skills         6 Agents • 4 Skills                                     │
│  8 Commands • 5 Gates         4 Commands • 3 Hooks                                    │
│                                                                                        │
│  📚  AKASHIC KNOWLEDGE        📱  FLUTTER FIREBASE DEPLOY                             │
│  "Ultimate research and       "Complete Flutter deployment                            │
│   knowledge base"              automation"                                            │
│  7 Agents • 4 Skills          13 Agents • 10 Skills                                   │
│  6 Commands • 4 Hooks         13 Commands • 2 Hooks                                   │
│  Docker: Qdrant, Neo4j,       iOS/Android • Fastlane                                  │
│  Elasticsearch, Redis         TestFlight • Play Store                                 │
│                                                                                        │
│  🥽  UNITY VR DEV              "AI-powered Meta Quest VR development"                  │
│  6 Agents • 6 Skills          MCP • IL2CPP • Voice • Quest Build • Debug               │
│  7 Commands • 3 Hooks         Unity 2022.3+ • Meta XR SDK v74+                         │
│                                                                                        │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Installation from Marketplace

```bash
# Install Plugin Factory
claude plugin install plugin-factory@monxun-marketplace

# Install Heuristics Framework
claude plugin install heuristics-framework@monxun-marketplace

# Install Akashic Knowledge
claude plugin install akashic-knowledge@monxun-marketplace

# Install Flutter Firebase Deploy
claude plugin install flutter-firebase-deploy@monxun-marketplace

# Install Unity VR Dev
claude plugin install unity-vr-dev@monxun-marketplace
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/claude-code-plugins.git
cd claude-code-plugins

# Load Plugin Factory locally
claude --plugin-dir ./plugins/plugin-factory

# Load Heuristics Framework locally
claude --plugin-dir ./plugins/heuristics-framework

# Load Akashic Knowledge (requires Docker)
cd plugins/akashic-knowledge/docker && docker-compose up -d && cd ../../..
claude --plugin-dir ./plugins/akashic-knowledge

# Load Flutter Firebase Deploy
claude --plugin-dir ./plugins/flutter-firebase-deploy

# Load Unity VR Dev
claude --plugin-dir ./plugins/unity-vr-dev
```

### Create Your First Plugin

```bash
# In Claude Code session
/plugin-factory:create-plugin my-awesome-plugin
```

### Discover Heuristics from Code

```bash
# In Claude Code session
/heuristics-framework:discover ./src --domain software-engineering
```

Both plugins use multi-agent orchestration to guide you through their respective workflows automatically.

---

## 🏭 Plugin Factory

### Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `create-plugin` | Generate complete plugin | `/plugin-factory:create-plugin my-plugin` |
| `create-skill` | Create progressive disclosure skill | `/plugin-factory:create-skill data-parser ./my-plugin` |
| `create-agent` | Create specialized subagent | `/plugin-factory:create-agent reviewer ./my-plugin` |
| `create-hook` | Create event hooks | `/plugin-factory:create-hook PreToolUse ./my-plugin` |
| `create-mcp` | Create MCP server config | `/plugin-factory:create-mcp api-client ./my-plugin` |
| `validate-plugin` | Run comprehensive validation | `/plugin-factory:validate-plugin ./my-plugin` |
| `create-marketplace` | Package for distribution | `/plugin-factory:create-marketplace ./my-plugin` |
| `research-patterns` | Research latest patterns | `/plugin-factory:research-patterns hooks --deep` |

### Agents

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         AGENT ORCHESTRATION                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                          ┌──────────────┐                                │
│                          │ ORCHESTRATOR │                                │
│                          │    (opus)    │                                │
│                          └──────┬───────┘                                │
│                                 │                                        │
│         ┌───────────────────────┼───────────────────────┐                │
│         │                       │                       │                │
│         ▼                       ▼                       ▼                │
│  ┌─────────────┐         ┌───────────┐          ┌──────────┐            │
│  │ CLARIFICATION│         │ RESEARCHER │          │  PLANNER  │            │
│  │   (haiku)   │         │  (sonnet)  │          │ (sonnet)  │            │
│  └─────────────┘         └───────────┘          └──────────┘            │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        BUILDERS                                  │    │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │    │
│  │  │   SKILL   │  │   HOOK    │  │   AGENT   │  │    MCP    │    │    │
│  │  │  BUILDER  │  │  BUILDER  │  │  BUILDER  │  │  BUILDER  │    │    │
│  │  │ (sonnet)  │  │ (sonnet)  │  │ (sonnet)  │  │ (sonnet)  │    │    │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                 │                                        │
│                                 ▼                                        │
│                    ┌───────────────────────┐                            │
│                    │      VALIDATOR        │                            │
│                    │       (haiku)         │                            │
│                    └───────────┬───────────┘                            │
│                                │                                        │
│                                ▼                                        │
│                    ┌───────────────────────┐                            │
│                    │     DOCUMENTER        │                            │
│                    │      (sonnet)         │                            │
│                    └───────────────────────┘                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Skills

| Skill | Description | Auto-Triggers |
|:------|:------------|:--------------|
| **plugin-patterns** | Core plugin architecture | "create plugin", "plugin structure" |
| **skill-authoring** | Progressive disclosure patterns | "create skill", "SKILL.md" |
| **hook-engineering** | Event hook system (12 types) | "create hook", "PreToolUse" |
| **agent-design** | Subagent orchestration | "create agent", "subagent" |
| **mcp-integration** | MCP server patterns | "MCP", "external tools" |
| **heuristics-engine** | Quality validation | "validate", "quality gates" |

---

## 🧠 Heuristics Framework

LLM-based framework for automated heuristic discovery, validation, and documentation using cutting-edge research methodologies.

### Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `discover` | Full discovery pipeline | `/heuristics-framework:discover ./src --domain software-engineering` |
| `extract` | Extract patterns only | `/heuristics-framework:extract ./docs --min-confidence 0.7` |
| `validate` | Validate heuristics (POPPER) | `/heuristics-framework:validate ./heuristics/` |
| `build-kg` | Build knowledge graph | `/heuristics-framework:build-kg ./patterns.json --format neo4j` |

### Agents

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    HEURISTICS PIPELINE ORCHESTRATION                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                          ┌──────────────┐                                │
│                          │ ORCHESTRATOR │                                │
│                          │    (opus)    │                                │
│                          └──────┬───────┘                                │
│                                 │                                        │
│              ┌──────────────────┼──────────────────┐                     │
│              │                  │                  │                     │
│              ▼                  ▼                  ▼                     │
│       ┌───────────┐      ┌───────────┐      ┌───────────┐               │
│       │ EXTRACTOR │      │SYNTHESIZER│      │ VALIDATOR │               │
│       │ (sonnet)  │      │  (opus)   │      │  (opus)   │               │
│       │           │      │           │      │           │               │
│       │  Pattern  │      │  AutoHD   │      │  POPPER   │               │
│       │ Parsing   │      │ Heuristic │      │ Falsify   │               │
│       └─────┬─────┘      └─────┬─────┘      └─────┬─────┘               │
│             │                  │                  │                     │
│             └──────────────────┼──────────────────┘                     │
│                                │                                        │
│              ┌─────────────────┼─────────────────┐                      │
│              │                                   │                      │
│              ▼                                   ▼                      │
│       ┌───────────┐                       ┌───────────┐                 │
│       │DOCUMENTER │                       │KG-BUILDER │                 │
│       │ (sonnet)  │                       │ (sonnet)  │                 │
│       │           │                       │           │                 │
│       │ JSON-LD   │                       │ Knowledge │                 │
│       │ Markdown  │                       │  Graph    │                 │
│       └───────────┘                       └───────────┘                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Skills

| Skill | Description | Auto-Triggers |
|:------|:------------|:--------------|
| **autohd-discovery** | Automated heuristic function generation | "discover heuristics", "AutoHD", "heuristic functions" |
| **popper-validation** | Sequential falsification framework | "validate hypothesis", "POPPER", "falsification" |
| **kg-construction** | Knowledge graph building pipeline | "knowledge graph", "entity extraction", "relationships" |
| **deterministic-inference** | Reproducible LLM inference (SGLang) | "deterministic", "reproducible", "batch-invariant" |

### Research Foundation

The Heuristics Framework is built on cutting-edge research:

| Research | Description | Source |
|:---------|:------------|:-------|
| **AutoHD** | Complex LLM Planning via Automated Heuristics Discovery | Texas A&M, Feb 2025 |
| **POPPER** | Agentic AI Framework for Hypothesis Validation | Stanford/Harvard, Feb 2025 |
| **KG Construction** | LLM-empowered Knowledge Graph Construction Survey | Oct 2025 |
| **Deterministic Inference** | SGLang batch-invariant kernels | Sep 2025 |

### Output Formats

#### JSON-LD Schema

```json
{
  "@type": "heuristic:Heuristic",
  "@id": "heuristic:early-return-001",
  "name": "Early Return Pattern",
  "heuristic:confidence": 0.87,
  "popper:validation": {
    "method": "POPPER",
    "typeIError": 0.08
  }
}
```

#### Quality Metrics

| Metric | Target |
|:-------|:-------|
| Heuristic confidence | >0.85 |
| Type-I error rate | <0.10 |
| Statistical power | >0.80 |
| KG entity precision | >0.85 |

---

## 📚 Akashic Knowledge

The ultimate research and knowledge base plugin combining multi-agent orchestration, agentic RAG, containerized databases, and automated heuristics discovery.

### Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `create-kb` | Create knowledge base | `/akashic:create-kb my-research project` |
| `ingest` | Ingest documents | `/akashic:ingest my-research ./docs` |
| `query` | Hybrid search query | `/akashic:query my-research "architecture patterns"` |
| `discover` | Discover heuristics | `/akashic:discover my-research --domain code-quality` |
| `export` | Export research docs | `/akashic:export my-research ./output.md` |
| `sync` | Check infrastructure | `/akashic:sync --status` |

### Agents

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     AKASHIC KNOWLEDGE PIPELINE                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                          ┌──────────────┐                                │
│                          │ ORCHESTRATOR │                                │
│                          └──────┬───────┘                                │
│                                 │                                        │
│         ┌───────────────────────┼───────────────────────┐                │
│         │                       │                       │                │
│         ▼                       ▼                       ▼                │
│  ┌───────────┐          ┌───────────┐           ┌───────────┐           │
│  │ RESEARCHER │          │ EXTRACTOR │           │  INDEXER  │           │
│  │  Web/Docs  │          │  Entities │           │  Qdrant   │           │
│  └─────┬─────┘          │  Relations │           │  Neo4j    │           │
│        │                 └─────┬─────┘           │    ES     │           │
│        │                       │                 └─────┬─────┘           │
│        └───────────────────────┼───────────────────────┘                 │
│                                ▼                                         │
│                ┌───────────────────────────────┐                        │
│                │         SYNTHESIZER           │                        │
│                │    (AutoHD Heuristics)        │                        │
│                └───────────────┬───────────────┘                        │
│                                ▼                                         │
│                ┌───────────────────────────────┐                        │
│                │          VALIDATOR            │                        │
│                │      (POPPER Framework)       │                        │
│                └───────────────┬───────────────┘                        │
│                                ▼                                         │
│                ┌───────────────────────────────┐                        │
│                │          RETRIEVER            │                        │
│                │       (Hybrid RAG)            │                        │
│                └───────────────────────────────┘                        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Skills

| Skill | Description | Auto-Triggers |
|:------|:------------|:--------------|
| **knowledge-discovery** | Research pattern extraction | "discover patterns", "knowledge extraction" |
| **rag-retrieval** | Hybrid semantic + keyword search | "search knowledge", "query", "RAG" |
| **heuristics-synthesis** | AutoHD heuristic generation | "generate heuristics", "decision functions" |
| **graph-reasoning** | Multi-hop knowledge graph queries | "graph traversal", "relationships" |

### Infrastructure (Docker)

| Service | Port | Purpose |
|:--------|:-----|:--------|
| Qdrant | 6333/6334 | Vector database (semantic search) |
| Neo4j | 7474/7687 | Graph database (knowledge graph) |
| Elasticsearch | 9200 | Keyword search (BM25) |
| Redis | 6379 | Caching and session state |

```bash
# Start infrastructure
cd plugins/akashic-knowledge/docker
docker-compose up -d

# Verify containers
docker-compose ps
```

### RAG Architecture

```
Query → Decomposition → ┌─────────────┬─────────────┐
                        │  Semantic   │   Keyword   │
                        │  (Qdrant)   │    (ES)     │
                        │  80% weight │  20% weight │
                        └──────┬──────┴──────┬──────┘
                               │   RRF Fusion   │
                               └───────┬───────┘
                                       ▼
                            ColBERT Reranking
                                       ▼
                            Graph Augmentation
                                       ▼
                              Top-K Results
```

---

## 📱 Flutter Firebase Deploy

Complete Flutter + Firebase deployment automation for iOS and Android, including Fastlane, TestFlight, Play Store, GitHub Actions CI/CD, and code signing management.

### Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `analyze-project` | Analyze Flutter project | `/flutter-firebase-deploy:analyze-project` |
| `configure-firebase` | Set up Firebase | `/flutter-firebase-deploy:configure-firebase my-project` |
| `setup-ios` | Configure iOS/Xcode | `/flutter-firebase-deploy:setup-ios --capabilities push` |
| `setup-android` | Configure Android/Gradle | `/flutter-firebase-deploy:setup-android --create-keystore` |
| `configure-fastlane` | Set up Fastlane | `/flutter-firebase-deploy:configure-fastlane --match-repo URL` |
| `deploy-testflight` | Deploy to TestFlight | `/flutter-firebase-deploy:deploy-testflight` |
| `deploy-playstore` | Deploy to Play Store | `/flutter-firebase-deploy:deploy-playstore --track beta` |
| `configure-oauth` | Set up auth providers | `/flutter-firebase-deploy:configure-oauth --providers google,apple` |
| `run-simulator-tests` | Run on simulator/emulator | `/flutter-firebase-deploy:run-simulator-tests --platform ios` |
| `configure-github-actions` | Set up CI/CD | `/flutter-firebase-deploy:configure-github-actions` |
| `setup-self-hosted-runner` | Configure Mac Mini runner | `/flutter-firebase-deploy:setup-self-hosted-runner` |
| `validate-config` | Validate all configs | `/flutter-firebase-deploy:validate-config --fix` |
| `troubleshoot` | Diagnose issues | `/flutter-firebase-deploy:troubleshoot "error message"` |

### Agents

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  FLUTTER FIREBASE DEPLOY ORCHESTRATION                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                          ┌──────────────┐                                │
│                          │ ORCHESTRATOR │                                │
│                          └──────┬───────┘                                │
│                                 │                                        │
│    ┌────────────────────────────┼────────────────────────────┐           │
│    │                            │                            │           │
│    ▼                            ▼                            ▼           │
│ ┌─────────────┐          ┌─────────────┐            ┌─────────────┐     │
│ │   FLUTTER   │          │   FIREBASE  │            │     iOS     │     │
│ │  ANALYZER   │          │ CONFIGURATOR│            │ SPECIALIST  │     │
│ └─────────────┘          └─────────────┘            └─────────────┘     │
│                                                                          │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│ │   ANDROID   │  │  FASTLANE   │  │   GITHUB    │  │   SIGNING   │     │
│ │ SPECIALIST  │  │ SPECIALIST  │  │   ACTIONS   │  │ SPECIALIST  │     │
│ └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                          │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│ │    OAUTH    │  │  SIMULATOR  │  │  VALIDATOR  │  │TROUBLESHOOTER│     │
│ │CONFIGURATOR │  │   TESTER    │  │             │  │             │     │
│ └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                          │
│                          ┌─────────────┐                                │
│                          │  RESEARCHER │                                │
│                          └─────────────┘                                │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Skills

| Skill | Description | Auto-Triggers |
|:------|:------------|:--------------|
| **flutter-analysis** | Project detection | "analyze flutter", "detect firebase" |
| **firebase-config** | FlutterFire setup | "configure firebase", "firebase init" |
| **ios-setup** | Xcode configuration | "ios setup", "xcode config", "capabilities" |
| **android-setup** | Gradle configuration | "android setup", "gradle", "signing config" |
| **fastlane-automation** | Build automation | "fastlane", "matchfile", "lanes" |
| **github-actions-cicd** | CI/CD workflows | "github actions", "ci cd", "workflow" |
| **signing-management** | Code signing | "certificates", "provisioning", "keystore" |
| **oauth-integration** | Auth providers | "google sign in", "apple sign in", "oauth" |
| **simulator-testing** | Device testing | "simulator", "emulator", "run tests" |
| **troubleshooting** | Issue resolution | "fix error", "troubleshoot", "debug" |

### Deployment Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐             │
│  │ ANALYZE  │──▶│ CONFIGURE│──▶│  BUILD   │──▶│  DEPLOY  │             │
│  │ PROJECT  │   │ FIREBASE │   │ FASTLANE │   │  STORES  │             │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘             │
│       │              │              │              │                    │
│       ▼              ▼              ▼              ▼                    │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐             │
│  │ Flutter  │   │ google-  │   │  Match   │   │TestFlight│             │
│  │ pubspec  │   │ services │   │ Certs    │   │  + Play  │             │
│  │ Platform │   │ Info.plist│   │ Fastfile │   │  Store   │             │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘             │
│                                                                          │
│  ════════════════════════════════════════════════════════════════════   │
│                                                                          │
│                        GITHUB ACTIONS CI/CD                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Push → Test → Build iOS → Build Android → Deploy to Stores    │    │
│  │                                                                  │    │
│  │  Supports: GitHub-hosted runners + Self-hosted Mac Mini         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🥽 Unity VR Dev

AI-powered Unity VR development for Meta Quest. Build automation, debug orchestration, voice integration, and testing through Claude Code MCP.

### Commands

| Command | Description | Example |
|:--------|:------------|:--------|
| `build-quest` | Build IL2CPP APK for Meta Quest | `/unity-vr-dev:build-quest` |
| `deploy-quest` | Deploy APK to Quest via ADB | `/unity-vr-dev:deploy-quest` |
| `mcp-connect` | Connect to Unity MCP server | `/unity-vr-dev:mcp-connect` |
| `debug-session` | Start debug session (LogCat, GPU, mirror) | `/unity-vr-dev:debug-session` |
| `voice-setup` | Configure voice pipeline | `/unity-vr-dev:voice-setup` |
| `test-suite` | Run Unity test suite | `/unity-vr-dev:test-suite` |
| `adr-create` | Create Architecture Decision Record | `/unity-vr-dev:adr-create` |

### Agents

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     UNITY VR DEV ORCHESTRATION                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                          ┌──────────────┐                                │
│                          │ ORCHESTRATOR │                                │
│                          │    (opus)    │                                │
│                          └──────┬───────┘                                │
│                                 │                                        │
│         ┌───────────────────────┼───────────────────────┐                │
│         │              │        │        │               │                │
│         ▼              ▼        ▼        ▼               ▼                │
│  ┌───────────┐  ┌───────────┐  ┌──────┐  ┌───────┐  ┌───────────┐      │
│  │   BUILD   │  │   DEBUG   │  │VOICE │  │ TEST  │  │ KNOWLEDGE │      │
│  │   AGENT   │  │   AGENT   │  │AGENT │  │ AGENT │  │   AGENT   │      │
│  │ (sonnet)  │  │ (sonnet)  │  │(son) │  │(son)  │  │  (sonnet) │      │
│  └───────────┘  └───────────┘  └──────┘  └───────┘  └───────────┘      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Skills

| Skill | Description | Auto-Triggers |
|:------|:------------|:--------------|
| **unity-mcp-integration** | Unity MCP server communication | "MCP", "unity editor", "scene manipulation" |
| **quest-build-automation** | IL2CPP build pipeline | "build quest", "IL2CPP", "APK" |
| **debug-orchestration** | LogCat, GPU profiling, mirroring | "debug", "logcat", "GPU profiler" |
| **voice-pipeline** | Porcupine + Deepgram voice | "voice", "wake word", "speech" |
| **adr-management** | Architecture Decision Records | "ADR", "decision record" |
| **wsl2-networking** | WSL2 network configuration | "WSL2", "mirrored mode", "port forward" |

### Quest Constraints

| Constraint | Details |
|:-----------|:--------|
| **No gRPC** | IL2CPP ARM64 linking errors — use HTTP/WebSocket only |
| **IL2CPP + ARM64** | Required for Quest Store submission |
| **11.1ms frame budget** | 90 FPS target for performance tests |
| **Unity 2022.3 LTS — Unity 6** | Meta XR SDK v74+ |

---

## 🏗 Architecture

### Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          ◀── ONLY file here (critical!)
│
├── commands/                ◀── User-invoked entry points
│   ├── main-command.md
│   └── helper-command.md
│
├── agents/                  ◀── Specialized subagents
│   ├── orchestrator.md
│   └── specialist.md
│
├── skills/                  ◀── Auto-triggered capabilities
│   └── my-skill/
│       ├── SKILL.md         ◀── < 500 lines
│       └── references/      ◀── Detailed docs
│           ├── patterns.md
│           └── examples.md
│
├── hooks/                   ◀── Lifecycle event handlers
│   ├── hooks.json
│   └── scripts/
│       └── validate.py
│
├── templates/               ◀── Generation templates
├── schemas/                 ◀── JSON validation
└── docs/                    ◀── Documentation
```

### Quality Gates

```
┌─────────────────────────────────────────────────────────────────────┐
│                        QUALITY PIPELINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │STRUCTURE │──▶│  SCHEMA  │──▶│COMPONENTS│──▶│ QUALITY  │        │
│  │   25%    │   │   25%    │   │   25%    │   │   25%    │        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│       │              │              │              │                │
│       ▼              ▼              ▼              ▼                │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │• Manifest│   │• JSON    │   │• Command │   │• Skills  │        │
│  │  exists  │   │  valid   │   │  front-  │   │  < 500   │        │
│  │• Only in │   │• YAML    │   │  matter  │   │  lines   │        │
│  │  .claude │   │  valid   │   │• Agent   │   │• Refs    │        │
│  │  -plugin │   │• kebab   │   │  front-  │   │  exist   │        │
│  │• Paths   │   │  -case   │   │  matter  │   │• Scripts │        │
│  │  valid   │   │• semver  │   │• Triggers│   │  used    │        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│                                                                     │
│  ════════════════════════════════════════════════════════════════  │
│                                                                     │
│    SCORE: 95/100    GRADE: A    STATUS: ✅ PASS                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Hook Exit Codes

| Exit Code | Meaning | Claude Behavior |
|:---------:|:--------|:----------------|
| `0` | Success | Continue, parse JSON output |
| `2` | Block | **Stop operation**, show stderr |
| Other | Error | Non-blocking, continue with warning |

---

## 📚 Documentation

### Repository Structure

```
claude-code-plugins/
│
├── monxun-marketplace/              # Plugin marketplace registry
│   └── .claude-plugin/
│       └── marketplace.json         # Lists all 8 plugins
│
├── plugins/                         # All plugins
│   │
│   ├── plugin-factory/              # Meta-plugin for building plugins
│   │   ├── .claude-plugin/plugin.json
│   │   ├── agents/                  # 10 specialized subagents
│   │   ├── skills/                  # 6 progressive disclosure skills
│   │   ├── commands/                # 8 user-invoked commands
│   │   ├── hooks/                   # Validation hooks
│   │   ├── schemas/                 # JSON validation schemas
│   │   └── templates/               # Generation templates
│   │
│   ├── heuristics-framework/        # Heuristic discovery framework
│   │   ├── .claude-plugin/plugin.json
│   │   ├── agents/                  # 6 pipeline agents
│   │   ├── skills/                  # 4 research-based skills
│   │   ├── commands/                # 4 discovery commands
│   │   └── hooks/                   # Validation hooks
│   │
│   ├── akashic-knowledge/           # Research & knowledge base plugin
│   │   ├── .claude-plugin/plugin.json
│   │   ├── agents/                  # 7 RAG/research agents
│   │   ├── skills/                  # 4 knowledge skills
│   │   ├── commands/                # 6 KB commands
│   │   ├── hooks/                   # Automation hooks
│   │   ├── docker/                  # Qdrant, Neo4j, ES, Redis
│   │   │   └── docker-compose.yml
│   │   ├── mcp/                     # MCP server configs
│   │   ├── schemas/                 # KB validation schemas
│   │   └── templates/               # Document templates
│   │
│   ├── flutter-firebase-deploy/     # Flutter deployment automation
│   │   ├── .claude-plugin/plugin.json
│   │   ├── agents/                  # 13 deployment agents
│   │   ├── skills/                  # 10 platform skills
│   │   ├── commands/                # 13 deployment commands
│   │   ├── hooks/                   # Validation hooks
│   │   └── docs/
│   │
│   └── unity-vr-dev/               # AI-powered Meta Quest VR development
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json                # Unity MCP server config
│       ├── agents/                  # 6 VR development agents
│       ├── skills/                  # 6 progressive disclosure skills
│       ├── commands/                # 7 VR commands
│       ├── hooks/                   # ADB check, build validation hooks
│       ├── schemas/                 # Build config, MCP response schemas
│       └── templates/               # ADR template, build config
│
├── docs/                            # Documentation
│   ├── claude-code/                 # Claude Code reference docs
│   ├── heuristics-documentation-framework/  # Research methodology
│   └── flutter-finalizer/           # Flutter plugin task specs
│
├── CLAUDE.md                        # Claude Code guidance
├── README.md                        # This file
└── LICENSE                          # MIT License
```

### Key Documentation

#### Plugin Factory

| Document | Description |
|:---------|:------------|
| [QUICKSTART](plugins/plugin-factory/docs/QUICKSTART.md) | Get started in 5 minutes |
| [ARCHITECTURE](plugins/plugin-factory/docs/ARCHITECTURE.md) | Design decisions & workflows |
| [HEURISTICS](plugins/plugin-factory/docs/HEURISTICS.md) | Quality patterns & anti-patterns |

#### Heuristics Framework

| Document | Description |
|:---------|:------------|
| [README](plugins/heuristics-framework/docs/README.md) | Framework overview & usage |
| [AutoHD Research](docs/heuristics-documentation-framework/autohd-discovery.md) | Automated heuristic discovery methodology |
| [POPPER Research](docs/heuristics-documentation-framework/popper-validation.md) | Hypothesis validation framework |

#### Akashic Knowledge

| Document | Description |
|:---------|:------------|
| [README](plugins/akashic-knowledge/docs/README.md) | Plugin overview & quick start |
| [ARCHITECTURE](plugins/akashic-knowledge/docs/ARCHITECTURE.md) | RAG pipeline & agent orchestration |
| [QUICKSTART](plugins/akashic-knowledge/docs/QUICKSTART.md) | 5-minute getting started guide |

#### Flutter Firebase Deploy

| Document | Description |
|:---------|:------------|
| [README](plugins/flutter-firebase-deploy/docs/README.md) | Deployment automation overview |

#### Unity VR Dev

| Document | Description |
|:---------|:------------|
| [Plugin Manifest](plugins/unity-vr-dev/.claude-plugin/plugin.json) | Plugin configuration and metadata |
| [MCP Config](plugins/unity-vr-dev/.mcp.json) | Unity MCP server connection |
| [Marketplace Guide](monxun-marketplace/unity-vr-dev-plugin.md) | Complete plugin reference |

---

## 🎯 Key Patterns

### Progressive Disclosure

Keep main skill files concise, with detailed documentation in references:

```
skills/my-skill/
├── SKILL.md              # < 500 lines, core patterns only
└── references/
    ├── overview.md       # Detailed explanation
    ├── patterns.md       # Advanced patterns
    └── examples.md       # Code examples
```

### Tool Scoping

Grant minimum necessary tool access to agents:

| Agent Type | Tools | Purpose |
|:-----------|:------|:--------|
| **Research** | Read, Grep, Glob | Information gathering |
| **Research+** | Read, Grep, Glob, WebSearch | External research |
| **Validation** | Read, Bash | Testing (no writes) |
| **Builder** | Read, Write, Edit, Bash | Construction |

### Description Optimization

Include trigger keywords for auto-discovery:

```yaml
# ✅ Good
description: |
  Plugin validation and quality metrics.
  Use when: validation, quality gates, "validate plugin".
  Supports: structure validation, schema validation.

# ❌ Bad
description: Handles plugin stuff.
```

---

## 🔧 Development

### Testing Plugins Locally

```bash
# Load Plugin Factory
claude --plugin-dir ./plugins/plugin-factory

# Load Heuristics Framework
claude --plugin-dir ./plugins/heuristics-framework

# Load Akashic Knowledge (start Docker first)
cd plugins/akashic-knowledge/docker && docker-compose up -d && cd ../../..
claude --plugin-dir ./plugins/akashic-knowledge

# Load Flutter Firebase Deploy
claude --plugin-dir ./plugins/flutter-firebase-deploy

# Load Unity VR Dev
claude --plugin-dir ./plugins/unity-vr-dev

# Load multiple plugins
claude --plugin-dir ./plugins/plugin-factory \
       --plugin-dir ./plugins/akashic-knowledge
```

### Validation Scripts

#### Plugin Factory

```bash
# Run manifest validation
python3 plugins/plugin-factory/hooks/scripts/validate-manifest.py

# Run skill validation
python3 plugins/plugin-factory/hooks/scripts/validate-skill.py

# Full quality gate check
python3 plugins/plugin-factory/hooks/scripts/quality-gate.py
```

#### Heuristics Framework

```bash
# Check corpus path exists
python3 plugins/heuristics-framework/hooks/scripts/check-corpus-exists.py

# Validate JSON-LD output schema
python3 plugins/heuristics-framework/hooks/scripts/validate-jsonld.py

# Validate heuristic function syntax
python3 plugins/heuristics-framework/hooks/scripts/validate-heuristic-syntax.py
```

#### Akashic Knowledge

```bash
# Start infrastructure
cd plugins/akashic-knowledge/docker && docker-compose up -d

# Check container health
docker-compose ps
```

#### Flutter Firebase Deploy

```bash
# Validate Flutter project structure
python3 plugins/flutter-firebase-deploy/hooks/scripts/validate-flutter-project.py

# Check signing configuration
python3 plugins/flutter-firebase-deploy/hooks/scripts/check-signing-config.py
```

### JSON Schemas

Validate your components against schemas in `plugins/plugin-factory/schemas/`:

- `plugin-manifest.schema.json` — Plugin manifest
- `skill-frontmatter.schema.json` — Skill YAML frontmatter
- `agent-frontmatter.schema.json` — Agent YAML frontmatter
- `hooks.schema.json` — Hooks configuration
- `mcp-config.schema.json` — MCP server config

---

## 📋 Requirements

| Requirement | Version | Plugins |
|:------------|:--------|:--------|
| Claude Code | 1.0.33+ | All |
| Python | 3.8+ | All |
| Docker | 20.10+ | Akashic Knowledge |
| Flutter SDK | 3.x | Flutter Firebase Deploy |
| Xcode | 15+ | Flutter Firebase Deploy (iOS) |
| Ruby/Bundler | 2.7+/2.x | Flutter Firebase Deploy (Fastlane) |
| Unity | 2022.3 LTS — Unity 6 | Unity VR Dev |
| Meta XR SDK | v74+ | Unity VR Dev |
| ADB | Latest | Unity VR Dev (Quest deployment) |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with Claude Code, Plugin Factory, and Heuristics Framework</sub>
</p>
