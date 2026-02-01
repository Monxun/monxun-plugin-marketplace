#!/usr/bin/env python3
"""
Parse security scan results from various tools (Trivy, OWASP, etc.).
Extracts vulnerability details for Claude Code auto-remediation.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET


@dataclass
class Vulnerability:
    """Represents a single vulnerability."""
    cve_id: str
    severity: str
    package_name: str
    installed_version: str
    fixed_version: Optional[str]
    title: str
    description: str
    cvss_score: Optional[float] = None
    references: List[str] = None

    def __post_init__(self):
        if self.references is None:
            self.references = []


@dataclass
class SecurityResults:
    """Aggregated security scan results."""
    total_vulnerabilities: int
    critical: int
    high: int
    medium: int
    low: int
    vulnerabilities: List[Vulnerability]
    source_tool: str


def parse_trivy_json(file_path: Path) -> SecurityResults:
    """Parse Trivy JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    vulnerabilities = []
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    # Handle different Trivy output formats
    results = data.get('Results', [data]) if 'Results' in data else [data]

    for result in results:
        vulns = result.get('Vulnerabilities', [])
        for vuln in vulns:
            severity = vuln.get('Severity', 'UNKNOWN').upper()
            if severity in severity_counts:
                severity_counts[severity] += 1

            vulnerabilities.append(Vulnerability(
                cve_id=vuln.get('VulnerabilityID', 'UNKNOWN'),
                severity=severity,
                package_name=vuln.get('PkgName', 'unknown'),
                installed_version=vuln.get('InstalledVersion', 'unknown'),
                fixed_version=vuln.get('FixedVersion'),
                title=vuln.get('Title', ''),
                description=vuln.get('Description', ''),
                cvss_score=vuln.get('CVSS', {}).get('nvd', {}).get('V3Score'),
                references=vuln.get('References', [])[:5]  # Limit references
            ))

    return SecurityResults(
        total_vulnerabilities=len(vulnerabilities),
        critical=severity_counts['CRITICAL'],
        high=severity_counts['HIGH'],
        medium=severity_counts['MEDIUM'],
        low=severity_counts['LOW'],
        vulnerabilities=vulnerabilities,
        source_tool='trivy'
    )


def parse_owasp_json(file_path: Path) -> SecurityResults:
    """Parse OWASP Dependency-Check JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    vulnerabilities = []
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    dependencies = data.get('dependencies', [])
    for dep in dependencies:
        for vuln in dep.get('vulnerabilities', []):
            # Map CVSS score to severity
            cvss = vuln.get('cvssv3', {}).get('baseScore') or vuln.get('cvssv2', {}).get('score', 0)
            if cvss >= 9.0:
                severity = 'CRITICAL'
            elif cvss >= 7.0:
                severity = 'HIGH'
            elif cvss >= 4.0:
                severity = 'MEDIUM'
            else:
                severity = 'LOW'

            severity_counts[severity] += 1

            vulnerabilities.append(Vulnerability(
                cve_id=vuln.get('name', 'UNKNOWN'),
                severity=severity,
                package_name=dep.get('fileName', 'unknown'),
                installed_version=dep.get('version', 'unknown'),
                fixed_version=None,  # OWASP DC doesn't provide this directly
                title=vuln.get('name', ''),
                description=vuln.get('description', ''),
                cvss_score=cvss,
                references=vuln.get('references', [])[:5]
            ))

    return SecurityResults(
        total_vulnerabilities=len(vulnerabilities),
        critical=severity_counts['CRITICAL'],
        high=severity_counts['HIGH'],
        medium=severity_counts['MEDIUM'],
        low=severity_counts['LOW'],
        vulnerabilities=vulnerabilities,
        source_tool='owasp-dependency-check'
    )


def parse_owasp_xml(file_path: Path) -> SecurityResults:
    """Parse OWASP Dependency-Check XML output."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Handle namespace
    ns = {'dc': 'https://jeremylong.github.io/DependencyCheck/dependency-check.2.5.xsd'}

    vulnerabilities = []
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    for dep in root.findall('.//dc:dependency', ns):
        pkg_name = dep.find('dc:fileName', ns)
        pkg_name = pkg_name.text if pkg_name is not None else 'unknown'

        for vuln in dep.findall('.//dc:vulnerability', ns):
            name = vuln.find('dc:name', ns)
            name = name.text if name is not None else 'UNKNOWN'

            severity_elem = vuln.find('dc:severity', ns)
            severity = severity_elem.text.upper() if severity_elem is not None else 'UNKNOWN'
            if severity in severity_counts:
                severity_counts[severity] += 1

            desc = vuln.find('dc:description', ns)
            desc = desc.text if desc is not None else ''

            vulnerabilities.append(Vulnerability(
                cve_id=name,
                severity=severity,
                package_name=pkg_name,
                installed_version='unknown',
                fixed_version=None,
                title=name,
                description=desc[:500] if desc else '',  # Truncate
                cvss_score=None,
                references=[]
            ))

    return SecurityResults(
        total_vulnerabilities=len(vulnerabilities),
        critical=severity_counts['CRITICAL'],
        high=severity_counts['HIGH'],
        medium=severity_counts['MEDIUM'],
        low=severity_counts['LOW'],
        vulnerabilities=vulnerabilities,
        source_tool='owasp-dependency-check'
    )


def parse_snyk_json(file_path: Path) -> SecurityResults:
    """Parse Snyk JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    vulnerabilities = []
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    vulns = data.get('vulnerabilities', [])
    for vuln in vulns:
        severity = vuln.get('severity', 'unknown').upper()
        if severity in severity_counts:
            severity_counts[severity] += 1

        identifiers = vuln.get('identifiers', {})
        cve = identifiers.get('CVE', ['UNKNOWN'])[0] if identifiers.get('CVE') else vuln.get('id', 'UNKNOWN')

        vulnerabilities.append(Vulnerability(
            cve_id=cve,
            severity=severity,
            package_name=vuln.get('packageName', 'unknown'),
            installed_version=vuln.get('version', 'unknown'),
            fixed_version=vuln.get('fixedIn', [None])[0] if vuln.get('fixedIn') else None,
            title=vuln.get('title', ''),
            description=vuln.get('description', '')[:500],
            cvss_score=vuln.get('cvssScore'),
            references=vuln.get('references', [])[:5]
        ))

    return SecurityResults(
        total_vulnerabilities=len(vulnerabilities),
        critical=severity_counts['CRITICAL'],
        high=severity_counts['HIGH'],
        medium=severity_counts['MEDIUM'],
        low=severity_counts['LOW'],
        vulnerabilities=vulnerabilities,
        source_tool='snyk'
    )


def format_output(results: SecurityResults, format_type: str, min_severity: str = 'LOW') -> str:
    """Format the results for output."""
    severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    min_level = severity_order.get(min_severity.upper(), 1)

    # Filter by minimum severity
    filtered_vulns = [
        v for v in results.vulnerabilities
        if severity_order.get(v.severity, 0) >= min_level
    ]

    if format_type == 'json':
        output = {
            'summary': {
                'total': results.total_vulnerabilities,
                'critical': results.critical,
                'high': results.high,
                'medium': results.medium,
                'low': results.low,
            },
            'vulnerabilities': [asdict(v) for v in filtered_vulns],
            'source_tool': results.source_tool
        }
        return json.dumps(output, indent=2)

    elif format_type == 'markdown':
        lines = [
            '## Security Scan Summary\n',
            '| Severity | Count |',
            '|----------|-------|',
            f'| Critical | {results.critical} |',
            f'| High | {results.high} |',
            f'| Medium | {results.medium} |',
            f'| Low | {results.low} |',
            f'| **Total** | **{results.total_vulnerabilities}** |',
            ''
        ]

        if filtered_vulns:
            lines.append('## Vulnerabilities\n')

            # Group by severity
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                sev_vulns = [v for v in filtered_vulns if v.severity == severity]
                if sev_vulns:
                    emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}
                    lines.append(f'### {emoji.get(severity, "")} {severity}\n')

                    for vuln in sev_vulns[:10]:  # Limit per severity
                        lines.append(f'#### {vuln.cve_id}\n')
                        lines.append(f'- **Package**: `{vuln.package_name}@{vuln.installed_version}`')
                        if vuln.fixed_version:
                            lines.append(f'- **Fixed In**: `{vuln.fixed_version}`')
                        if vuln.title:
                            lines.append(f'- **Title**: {vuln.title}')
                        if vuln.cvss_score:
                            lines.append(f'- **CVSS Score**: {vuln.cvss_score}')
                        lines.append('')

                    if len(sev_vulns) > 10:
                        lines.append(f'*...and {len(sev_vulns) - 10} more {severity} vulnerabilities*\n')

        return '\n'.join(lines)

    else:  # brief
        lines = [
            f'Security: {results.total_vulnerabilities} vulnerabilities '
            f'({results.critical} critical, {results.high} high, {results.medium} medium, {results.low} low)'
        ]

        # Show critical and high only in brief mode
        for vuln in filtered_vulns:
            if vuln.severity in ['CRITICAL', 'HIGH']:
                fix_info = f' -> fix: {vuln.fixed_version}' if vuln.fixed_version else ''
                lines.append(f'  [{vuln.severity}] {vuln.cve_id}: {vuln.package_name}@{vuln.installed_version}{fix_info}')

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse security scan results for CI/CD remediation')
    parser.add_argument('path', type=str, help='Path to security scan results file')
    parser.add_argument('--format', choices=['json', 'markdown', 'brief'], default='json',
                        help='Output format')
    parser.add_argument('--type', choices=['auto', 'trivy', 'owasp-json', 'owasp-xml', 'snyk'], default='auto',
                        help='Input format type')
    parser.add_argument('--min-severity', choices=['critical', 'high', 'medium', 'low'], default='low',
                        help='Minimum severity to include')

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Auto-detect format
    input_type = args.type
    if input_type == 'auto':
        with open(path, 'r') as f:
            content = f.read(1000)  # Read first 1000 chars

        if path.suffix == '.xml':
            input_type = 'owasp-xml'
        elif '"Results"' in content or '"ArtifactName"' in content:
            input_type = 'trivy'
        elif '"vulnerabilities"' in content and '"packageName"' in content:
            input_type = 'snyk'
        elif '"dependencies"' in content:
            input_type = 'owasp-json'
        else:
            print(f"Error: Could not auto-detect format for {path}", file=sys.stderr)
            sys.exit(1)

    # Parse results
    if input_type == 'trivy':
        results = parse_trivy_json(path)
    elif input_type == 'owasp-json':
        results = parse_owasp_json(path)
    elif input_type == 'owasp-xml':
        results = parse_owasp_xml(path)
    elif input_type == 'snyk':
        results = parse_snyk_json(path)
    else:
        print(f"Error: Unknown format type: {input_type}", file=sys.stderr)
        sys.exit(1)

    # Output results
    print(format_output(results, args.format, args.min_severity))

    # Exit with error code based on severity
    if results.critical > 0:
        sys.exit(2)  # Critical vulnerabilities
    elif results.high > 0:
        sys.exit(1)  # High vulnerabilities
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
