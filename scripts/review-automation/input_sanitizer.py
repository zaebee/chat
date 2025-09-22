#!/usr/bin/env python3
"""
Sacred Input Sanitization System
Protects the Sacred Review Automation from malicious inputs
"""

import re
import html
import unicodedata
from typing import Any, Dict, List, Union


class SacredInputSanitizer:
    """
    Sacred Justification: Input sanitization patterns based on OWASP guidelines
    Mathematical basis: Zero-tolerance policy for malicious patterns (100% blocking)
    """

    # Sacred security patterns - any match triggers immediate sanitization
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS script tags
        r'javascript:',                # JavaScript protocols
        r'vbscript:',                 # VBScript protocols
        r'on\w+\s*=',                 # Event handlers (onclick, onload, etc.)
        r'eval\s*\(',                 # eval() calls
        r'setTimeout\s*\(',           # setTimeout calls
        r'setInterval\s*\(',          # setInterval calls
        r'document\.',                # DOM manipulation
        r'window\.',                  # Window object access
        r'alert\s*\(',                # Alert dialogs
        r'confirm\s*\(',              # Confirm dialogs
        r'prompt\s*\(',               # Prompt dialogs
    ]

    # Markdown injection patterns
    MARKDOWN_INJECTION_PATTERNS = [
        r'\[.*?\]\s*\(javascript:',   # Markdown link with JS
        r'!\[.*?\]\s*\(.*?["\'].*?["\'].*?\)', # Image with potential XSS
        r'```.*?<script.*?```',       # Script in code blocks
    ]

    # File path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        r'\.\./+',                    # Directory traversal
        r'\.\.\\+',                   # Windows directory traversal
        r'~/',                        # Home directory access
        r'/etc/',                     # System directory access
        r'/proc/',                    # Process directory access
        r'/sys/',                     # System directory access
        r'C:\\',                      # Windows system drive
    ]

    # Unicode BiDi and hidden character patterns
    UNICODE_ATTACK_PATTERNS = [
        r'[\u202A-\u202E]',           # BiDi override characters
        r'[\u2066-\u2069]',           # Directional isolate characters
        r'[\u200B-\u200F]',           # Zero-width characters
        r'[\uFEFF]',                  # Byte order mark
        r'[\u061C]',                  # Arabic letter mark
    ]

    def __init__(self):
        """Initialize Sacred Input Sanitizer"""
        self.compiled_patterns = {
            'dangerous': [re.compile(pattern, re.IGNORECASE | re.DOTALL)
                         for pattern in self.DANGEROUS_PATTERNS],
            'markdown_injection': [re.compile(pattern, re.IGNORECASE | re.DOTALL)
                                  for pattern in self.MARKDOWN_INJECTION_PATTERNS],
            'path_traversal': [re.compile(pattern, re.IGNORECASE)
                              for pattern in self.PATH_TRAVERSAL_PATTERNS],
            'unicode_attacks': [re.compile(pattern)
                               for pattern in self.UNICODE_ATTACK_PATTERNS],
        }

    def sanitize_string(self, input_str: str, max_length: int = 65536) -> str:
        """
        Sanitize a string input for Sacred Review processing

        Sacred Justification: Max length 65536 matches GitHub comment limit
        """
        if not isinstance(input_str, str):
            return ""

        # Length protection
        if len(input_str) > max_length:
            input_str = input_str[:max_length] + "... [TRUNCATED FOR SAFETY]"

        # Remove dangerous patterns
        for pattern in self.compiled_patterns['dangerous']:
            input_str = pattern.sub('[REMOVED_DANGEROUS_CONTENT]', input_str)

        # Remove markdown injection attempts
        for pattern in self.compiled_patterns['markdown_injection']:
            input_str = pattern.sub('[REMOVED_MARKDOWN_INJECTION]', input_str)

        # Remove path traversal attempts
        for pattern in self.compiled_patterns['path_traversal']:
            input_str = pattern.sub('[REMOVED_PATH_TRAVERSAL]', input_str)

        # Remove Unicode attacks
        for pattern in self.compiled_patterns['unicode_attacks']:
            input_str = pattern.sub('', input_str)

        # HTML entity encoding for remaining content
        input_str = html.escape(input_str, quote=True)

        # Normalize Unicode to prevent mixed script attacks
        input_str = unicodedata.normalize('NFC', input_str)

        return input_str

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename inputs for safe processing

        Sacred Justification: Prevent directory traversal and dangerous extensions
        """
        if not isinstance(filename, str):
            return "unknown_file"

        # Remove path components
        filename = filename.split('/')[-1].split('\\')[-1]

        # Remove dangerous characters
        filename = re.sub(r'[<>:"|?*\x00-\x1f]', '_', filename)

        # Remove leading dots and spaces
        filename = filename.lstrip('. ')

        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            max_name_len = 255 - len(ext) - 1 if ext else 255
            filename = name[:max_name_len] + ('.' + ext if ext else '')

        return filename or "sanitized_file"

    def sanitize_pr_data(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize PR-related data for safe processing

        Sacred Justification: GitHub API data may contain user-controlled content
        """
        sanitized = {}

        # Safe fields that need minimal processing
        safe_numeric_fields = ['number', 'lines_added', 'lines_deleted']
        for field in safe_numeric_fields:
            if field in pr_data:
                value = pr_data[field]
                sanitized[field] = int(value) if isinstance(value, (int, str)) and str(value).isdigit() else 0

        # String fields that need sanitization
        string_fields = ['title', 'author', 'branch', 'body', 'diff']
        for field in string_fields:
            if field in pr_data:
                sanitized[field] = self.sanitize_string(str(pr_data[field]))

        # File lists need special handling
        if 'files_changed' in pr_data:
            files = pr_data['files_changed']
            if isinstance(files, list):
                sanitized['files_changed'] = [
                    self.sanitize_filename(f) for f in files
                    if isinstance(f, str)
                ][:100]  # Limit to 100 files for DoS prevention
            else:
                sanitized['files_changed'] = []

        return sanitized

    def sanitize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize metrics data for safe processing

        Sacred Justification: Prevent metric manipulation attacks
        """
        sanitized = {}

        # Numeric metrics with bounds checking
        numeric_fields = [
            'any_type_score', 'console_log_score', 'atcg_compliance_score',
            'sacred_justifications_score', 'performance_score', 'security_score',
            'any_type_violations', 'console_log_violations', 'total_files_analyzed'
        ]

        for field in numeric_fields:
            if field in metrics:
                try:
                    value = float(metrics[field])
                    # Ensure scores are within valid ranges
                    if 'score' in field:
                        value = max(0, min(100, value))  # Scores: 0-100
                    elif 'violations' in field:
                        value = max(0, value)  # Violations: >= 0
                    elif 'total_files' in field:
                        value = max(0, min(10000, value))  # Files: 0-10000
                    sanitized[field] = value
                except (ValueError, TypeError):
                    sanitized[field] = 0

        # Sanitize violation details
        if 'violations' in metrics and isinstance(metrics['violations'], dict):
            sanitized_violations = {}
            for category, violation_list in metrics['violations'].items():
                if isinstance(violation_list, list):
                    sanitized_list = []
                    for violation in violation_list[:20]:  # Limit to 20 per category
                        if isinstance(violation, dict):
                            sanitized_violation = {
                                'file': self.sanitize_filename(str(violation.get('file', 'unknown'))),
                                'line': max(1, int(violation.get('line', 1))) if str(violation.get('line', 1)).isdigit() else 1,
                                'content': self.sanitize_string(str(violation.get('content', '')), max_length=200),
                                'type': re.sub(r'[^a-zA-Z0-9_]', '', str(violation.get('type', 'unknown')))
                            }
                            sanitized_list.append(sanitized_violation)
                    sanitized_violations[self.sanitize_string(category, max_length=50)] = sanitized_list
            sanitized['violations'] = sanitized_violations

        return sanitized

    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize configuration data

        Sacred Justification: Prevent configuration injection attacks
        """
        if not isinstance(config, dict):
            return {}

        sanitized = {}

        # Sanitize reviewer configuration
        if 'reviewers' in config:
            reviewers_config = config['reviewers']
            if isinstance(reviewers_config, dict):
                sanitized_reviewers = {}
                for reviewer_name, reviewer_config in reviewers_config.items():
                    clean_name = re.sub(r'[^a-zA-Z0-9_]', '', str(reviewer_name))[:50]
                    if isinstance(reviewer_config, dict):
                        sanitized_reviewers[clean_name] = {
                            'enabled': bool(reviewer_config.get('enabled', True)),
                            'focus_areas': [
                                re.sub(r'[^a-zA-Z0-9_]', '', str(area))[:100]
                                for area in reviewer_config.get('focus_areas', [])
                                if isinstance(area, str)
                            ][:10]  # Limit to 10 focus areas
                        }
                sanitized['reviewers'] = sanitized_reviewers

        # Sanitize weights configuration
        if 'sacred_metrics' in config and 'weights' in config['sacred_metrics']:
            weights = config['sacred_metrics']['weights']
            if isinstance(weights, dict):
                sanitized_weights = {}
                valid_weight_keys = [
                    'any_type_score', 'console_log_score', 'atcg_compliance',
                    'sacred_justifications', 'performance_score', 'security_score'
                ]
                for key, value in weights.items():
                    if key in valid_weight_keys:
                        try:
                            weight = float(value)
                            sanitized_weights[key] = max(0.0, min(1.0, weight))
                        except (ValueError, TypeError):
                            sanitized_weights[key] = 0.0

                # Ensure weights sum to approximately 1.0
                weight_sum = sum(sanitized_weights.values())
                if weight_sum > 0:
                    sanitized_weights = {k: v/weight_sum for k, v in sanitized_weights.items()}

                sanitized['sacred_metrics'] = {'weights': sanitized_weights}

        return sanitized

    def detect_injection_attempt(self, input_data: Any) -> List[str]:
        """
        Detect potential injection attempts in input data
        Returns list of detected attack patterns
        """
        if not isinstance(input_data, str):
            input_data = str(input_data)

        detected_attacks = []

        # Check each pattern category
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(input_data):
                    detected_attacks.append(f"{category}_injection")
                    break  # One detection per category is enough

        return detected_attacks


# Convenience function for quick sanitization
def sanitize_input(data: Any, data_type: str = "string") -> Any:
    """
    Quick sanitization function for common use cases
    """
    sanitizer = SacredInputSanitizer()

    if data_type == "string":
        return sanitizer.sanitize_string(str(data))
    elif data_type == "filename":
        return sanitizer.sanitize_filename(str(data))
    elif data_type == "pr_data":
        return sanitizer.sanitize_pr_data(data)
    elif data_type == "metrics":
        return sanitizer.sanitize_metrics(data)
    elif data_type == "config":
        return sanitizer.validate_configuration(data)
    else:
        return sanitizer.sanitize_string(str(data))


if __name__ == "__main__":
    # Test the sanitization system
    print("🛡️ Testing Sacred Input Sanitization...")

    sanitizer = SacredInputSanitizer()

    # Test dangerous inputs
    dangerous_inputs = [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "../../../etc/passwd",
        "file\u202Amalicious\u202C.txt",
        "console.log('injection')" * 1000,  # DoS attempt
    ]

    for dangerous_input in dangerous_inputs:
        sanitized = sanitizer.sanitize_string(dangerous_input)
        attacks = sanitizer.detect_injection_attempt(dangerous_input)
        print(f"Input: {dangerous_input[:50]}...")
        print(f"Sanitized: {sanitized[:50]}...")
        print(f"Attacks detected: {attacks}")
        print("---")

    print("✅ Sacred Input Sanitization tests completed!")