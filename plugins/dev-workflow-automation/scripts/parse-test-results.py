#!/usr/bin/env python3
"""
Parse test results from various formats (JUnit XML, Surefire, Flutter).
Extracts failure details for Claude Code auto-remediation.
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class TestFailure:
    """Represents a single test failure."""
    test_name: str
    test_class: str
    failure_type: str
    failure_message: str
    stack_trace: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class TestResults:
    """Aggregated test results."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    failures: List[TestFailure]
    source_format: str


def parse_junit_xml(file_path: Path) -> TestResults:
    """Parse JUnit XML format (Maven Surefire, Gradle, etc.)."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Handle both <testsuite> and <testsuites> root elements
    if root.tag == 'testsuites':
        testsuites = root.findall('testsuite')
    else:
        testsuites = [root]

    total = 0
    failed = 0
    skipped = 0
    failures = []

    for testsuite in testsuites:
        total += int(testsuite.get('tests', 0))
        failed += int(testsuite.get('failures', 0)) + int(testsuite.get('errors', 0))
        skipped += int(testsuite.get('skipped', 0))

        for testcase in testsuite.findall('testcase'):
            failure_elem = testcase.find('failure')
            error_elem = testcase.find('error')
            elem = failure_elem if failure_elem is not None else error_elem

            if elem is not None:
                stack_trace = elem.text or ''
                file_path_match = None
                line_num = None

                # Extract file path and line from stack trace
                # Java format: at com.package.Class.method(File.java:123)
                match = re.search(r'at\s+[\w.]+\((\w+\.java):(\d+)\)', stack_trace)
                if match:
                    file_path_match = match.group(1)
                    line_num = int(match.group(2))

                failures.append(TestFailure(
                    test_name=testcase.get('name', 'unknown'),
                    test_class=testcase.get('classname', 'unknown'),
                    failure_type=elem.get('type', 'failure'),
                    failure_message=elem.get('message', ''),
                    stack_trace=stack_trace,
                    file_path=file_path_match,
                    line_number=line_num
                ))

    return TestResults(
        total_tests=total,
        passed=total - failed - skipped,
        failed=failed,
        skipped=skipped,
        failures=failures,
        source_format='junit_xml'
    )


def parse_flutter_json(file_path: Path) -> TestResults:
    """Parse Flutter test JSON output."""
    with open(file_path, 'r') as f:
        # Flutter outputs newline-delimited JSON
        events = []
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    tests = {}
    failures = []

    for event in events:
        event_type = event.get('type')

        if event_type == 'testStart':
            test_id = event.get('test', {}).get('id')
            if test_id:
                tests[test_id] = {
                    'name': event.get('test', {}).get('name', 'unknown'),
                    'suite': event.get('test', {}).get('suiteID', 'unknown'),
                }

        elif event_type == 'error':
            test_id = event.get('testID')
            if test_id and test_id in tests:
                test_info = tests[test_id]
                stack_trace = event.get('stackTrace', '')

                # Extract file path and line from Dart stack trace
                # Format: package:app/path/file.dart:123:45
                file_path_match = None
                line_num = None
                match = re.search(r'([\w_/]+\.dart):(\d+):\d+', stack_trace)
                if match:
                    file_path_match = match.group(1)
                    line_num = int(match.group(2))

                failures.append(TestFailure(
                    test_name=test_info['name'],
                    test_class=str(test_info['suite']),
                    failure_type='error',
                    failure_message=event.get('error', ''),
                    stack_trace=stack_trace,
                    file_path=file_path_match,
                    line_number=line_num
                ))

    total = len(tests)
    failed = len(failures)

    return TestResults(
        total_tests=total,
        passed=total - failed,
        failed=failed,
        skipped=0,
        failures=failures,
        source_format='flutter_json'
    )


def parse_surefire_reports(directory: Path) -> TestResults:
    """Parse all Surefire XML reports in a directory."""
    all_results = TestResults(
        total_tests=0,
        passed=0,
        failed=0,
        skipped=0,
        failures=[],
        source_format='surefire'
    )

    xml_files = list(directory.glob('TEST-*.xml')) + list(directory.glob('*.xml'))

    for xml_file in xml_files:
        try:
            result = parse_junit_xml(xml_file)
            all_results.total_tests += result.total_tests
            all_results.passed += result.passed
            all_results.failed += result.failed
            all_results.skipped += result.skipped
            all_results.failures.extend(result.failures)
        except ET.ParseError as e:
            print(f"Warning: Failed to parse {xml_file}: {e}", file=sys.stderr)
            continue

    return all_results


def find_source_files(failures: List[TestFailure], search_paths: List[Path]) -> None:
    """Try to find full paths for source files mentioned in failures."""
    for failure in failures:
        if failure.file_path and not os.path.isabs(failure.file_path):
            for search_path in search_paths:
                for match in search_path.rglob(failure.file_path):
                    failure.file_path = str(match)
                    break


def format_output(results: TestResults, format_type: str) -> str:
    """Format the results for output."""
    if format_type == 'json':
        output = {
            'summary': {
                'total': results.total_tests,
                'passed': results.passed,
                'failed': results.failed,
                'skipped': results.skipped,
            },
            'failures': [asdict(f) for f in results.failures],
            'source_format': results.source_format
        }
        return json.dumps(output, indent=2)

    elif format_type == 'markdown':
        lines = [
            '## Test Results Summary\n',
            f'| Metric | Value |',
            f'|--------|-------|',
            f'| Total Tests | {results.total_tests} |',
            f'| Passed | {results.passed} |',
            f'| Failed | {results.failed} |',
            f'| Skipped | {results.skipped} |',
            ''
        ]

        if results.failures:
            lines.append('## Failures\n')
            for i, failure in enumerate(results.failures, 1):
                lines.append(f'### {i}. {failure.test_class}.{failure.test_name}\n')
                lines.append(f'**Type**: `{failure.failure_type}`\n')
                lines.append(f'**Message**: {failure.failure_message}\n')
                if failure.file_path:
                    loc = f'{failure.file_path}'
                    if failure.line_number:
                        loc += f':{failure.line_number}'
                    lines.append(f'**Location**: `{loc}`\n')
                lines.append('**Stack Trace**:')
                lines.append('```')
                # Limit stack trace length
                trace_lines = failure.stack_trace.split('\n')[:20]
                lines.extend(trace_lines)
                if len(failure.stack_trace.split('\n')) > 20:
                    lines.append('... (truncated)')
                lines.append('```\n')

        return '\n'.join(lines)

    else:  # brief
        lines = [
            f'Tests: {results.total_tests} total, {results.passed} passed, {results.failed} failed, {results.skipped} skipped'
        ]
        for failure in results.failures:
            lines.append(f'  FAIL: {failure.test_class}.{failure.test_name}')
            if failure.file_path:
                loc = failure.file_path
                if failure.line_number:
                    loc += f':{failure.line_number}'
                lines.append(f'        at {loc}')
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Parse test results for CI/CD remediation')
    parser.add_argument('path', type=str, help='Path to test results file or directory')
    parser.add_argument('--format', choices=['json', 'markdown', 'brief'], default='json',
                        help='Output format')
    parser.add_argument('--type', choices=['auto', 'junit', 'flutter', 'surefire'], default='auto',
                        help='Input format type')
    parser.add_argument('--source-paths', type=str, nargs='*', default=['.'],
                        help='Paths to search for source files')

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Auto-detect format
    input_type = args.type
    if input_type == 'auto':
        if path.is_dir():
            input_type = 'surefire'
        elif path.suffix == '.xml':
            input_type = 'junit'
        elif path.suffix == '.json':
            input_type = 'flutter'
        else:
            print(f"Error: Could not auto-detect format for {path}", file=sys.stderr)
            sys.exit(1)

    # Parse results
    if input_type == 'surefire':
        results = parse_surefire_reports(path)
    elif input_type == 'junit':
        results = parse_junit_xml(path)
    elif input_type == 'flutter':
        results = parse_flutter_json(path)
    else:
        print(f"Error: Unknown format type: {input_type}", file=sys.stderr)
        sys.exit(1)

    # Try to find full source paths
    search_paths = [Path(p) for p in args.source_paths]
    find_source_files(results.failures, search_paths)

    # Output results
    print(format_output(results, args.format))

    # Exit with error code if there are failures
    sys.exit(1 if results.failed > 0 else 0)


if __name__ == '__main__':
    main()
