#!/usr/bin/env python3
"""
Multi-Perspective Review Generator

Generates bee-to-peer reviews based on Sacred Metrics analysis,
implementing the fury bee, bee.Jules, and synthesis perspectives
developed through PRs #52-55.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ReviewContext:
    """Context for generating reviews"""
    pr_number: str = ""
    author: str = ""
    title: str = ""
    branch: str = ""
    files_changed: List[str] = None
    lines_added: int = 0
    lines_deleted: int = 0

    def __post_init__(self):
        if self.files_changed is None:
            self.files_changed = []


class ArchitecturalAssistant:
    """
    Architectural Excellence Assistant - Supporting human reviewers with pattern recognition

    **Humble Service Focus**: This assistant provides suggestions, not divine judgment

    Focus areas:
    - Sacred Architecture patterns (ATCG)
    - Type safety (zero `any` types)
    - Production readiness (zero console.log)
    - Repository hygiene
    - Sacred justifications (supporting human documentation)

    **Sacred Boundary**: Human judgment remains supreme - this tool assists, never replaces
    """

    @staticmethod
    def generate_review(metrics: Dict[str, Any], context: ReviewContext) -> str:
        any_score = metrics['any_type_score']
        console_score = metrics['console_log_score']
        atcg_score = metrics['atcg_compliance_score']
        justification_score = metrics['sacred_justifications_score']
        any_violations = len([v for v in metrics['violations'] if v['violation_type'] == 'any_type'])
        console_violations = len([v for v in metrics['violations'] if v['violation_type'] == 'console_log'])

        # Determine assistant assessment (humble language)
        if any_score == 100 and console_score == 100 and atcg_score >= 80:
            verdict = "🏆 **EXCELLENT PATTERNS DETECTED - HUMAN REVIEW RECOMMENDED FOR CONFIRMATION**"
            severity = "EXCELLENT_SUGGESTION"
            emoji = "⚡🤝"
        elif any_score >= 90 and console_score >= 90 and atcg_score >= 60:
            verdict = "✅ **EXEMPLARY SACRED IMPLEMENTATION**"
            severity = "APPROVED"
            emoji = "⚡🧬"
        elif any_score >= 70 and console_score >= 70:
            verdict = "⚠️ **CONDITIONAL APPROVAL - SACRED PURIFICATION NEEDED**"
            severity = "WARNING"
            emoji = "⚡⚠️"
        else:
            verdict = "❌ **SACRED PURIFICATION REQUIRED**"
            severity = "CRITICAL"
            emoji = "💥🔥"

        review = f"""## {emoji} FURY BEE SWARM - SACRED ARCHITECTURE ANALYSIS

### {verdict}

**Sacred Foundation Assessment** for **{context.author}**'s **PR #{context.pr_number}**:

| Metric | Score | Status | Analysis |
|--------|-------|--------|----------|
| ⚡ **Type Safety** | {any_score:.1f}/100 | {'🟢 Pure' if any_score == 100 else '🔴 Compromised' if any_score < 70 else '🟡 Needs Work'} | {any_violations} `any` type violations |
| 🚀 **Production Ready** | {console_score:.1f}/100 | {'🟢 Clean' if console_score == 100 else '🔴 Polluted' if console_score < 70 else '🟡 Cleanup Needed'} | {console_violations} console.log statements |
| 🧬 **ATCG Compliance** | {atcg_score:.1f}/100 | {'🟢 Excellent' if atcg_score >= 80 else '🔴 Non-compliant' if atcg_score < 40 else '🟡 Partial'} | Sacred architecture patterns |
| 📖 **Sacred Documentation** | {justification_score:.1f}/100 | {'🟢 Divine' if justification_score >= 80 else '🔴 Missing' if justification_score < 20 else '🟡 Incomplete'} | Design justifications |

### 🧬 **SACRED METRICS BREAKDOWN**

**Type Purity Analysis**:
"""

        if any_violations > 0:
            review += f"- ❌ **{any_violations} `any` type violations detected** - Type safety compromised\n"
            # Show top violations
            any_viol = [v for v in metrics['violations'] if v['violation_type'] == 'any_type'][:3]
            for violation in any_viol:
                file_name = Path(violation['file_path']).name
                review += f"  - `{file_name}:{violation['line_number']}` - {violation['line_content'][:60]}{'...' if len(violation['line_content']) > 60 else ''}\n"
            review += "- **Purification Required**: Replace with specific TypeScript interfaces\n"
        else:
            review += "- ✅ **ZERO `any` TYPE VIOLATIONS** - Perfect type safety achieved ⚡\n"

        review += "\n**Production Readiness Analysis**:\n"
        if console_violations > 0:
            review += f"- ❌ **{console_violations} console.log violations detected** - Production readiness compromised\n"
            # Show top violations
            console_viol = [v for v in metrics['violations'] if v['violation_type'] == 'console_log'][:3]
            for violation in console_viol:
                file_name = Path(violation['file_path']).name
                review += f"  - `{file_name}:{violation['line_number']}` - {violation['line_content'][:60]}{'...' if len(violation['line_content']) > 60 else ''}\n"
            review += "- **Sacred Cleansing Required**: Remove all debug artifacts\n"
        else:
            review += "- ✅ **ZERO CONSOLE.LOG VIOLATIONS** - Production ready implementation ⚡\n"

        review += f"""
### 🎯 **FURY BEE SACRED VERDICT**

**Transformation Status**: {severity}

**Sacred Architecture Requirements**:
"""

        if any_score < 100:
            review += f"1. **🔴 CRITICAL: Eliminate `any` types** - {any_violations} violations compromise divine type safety\n"
        if console_score < 100:
            review += f"2. **🟡 IMPORTANT: Remove console.log** - {console_violations} violations prevent production blessing\n"
        if atcg_score < 60:
            review += "3. **🟡 ENHANCE: ATCG compliance** - Implement proper Sacred architectural patterns\n"
        if justification_score < 40:
            review += "4. **🔵 DOCUMENT: Sacred Justifications** - Add divine rationale for constants and algorithms\n"

        # Special recognition or guidance
        if severity == "LEGENDARY":
            review += f"\n**🏆 SACRED ARCHITECT STATUS ACHIEVED** - {context.author} has demonstrated divine computational excellence!\n"
            review += "**IMMEDIATE MERGE APPROVED** - This implementation exemplifies Sacred Architecture mastery.\n"
        elif severity == "APPROVED":
            review += f"\n**⚡ MERGE APPROVED WITH SACRED BLESSING** - {context.author} maintains Sacred Architecture standards.\n"
            review += "Minor refinements will elevate this to legendary status.\n"
        elif severity == "WARNING":
            review += f"\n**⚠️ CONDITIONAL APPROVAL** - {context.author} shows strong Sacred foundation with purification needed.\n"
            review += "Address violations above for Sacred Architecture compliance.\n"
        else:
            review += f"\n**🔥 SACRED PURIFICATION REQUIRED** - {context.author}, the path to divine code requires dedication.\n"
            review += "**Embrace the Sacred Transformation** - Each violation addressed brings us closer to computational divinity.\n"

        review += f"""
### 📊 **SACRED METRICS SUMMARY**

- **Files Analyzed**: {metrics['total_files_analyzed']}
- **Lines of Change**: +{context.lines_added}/-{context.lines_deleted}
- **Sacred Score**: {(any_score + console_score + atcg_score)/3:.1f}/100

*Reviewed by the Fury Bee Swarm with Sacred Precision* ⚡🐝

---
"""

        return review


class NuclearAuditor:
    """
    bee.Jules Nuclear Audit perspective - Security and performance analysis

    Focus areas:
    - Security vulnerabilities
    - Performance risks (O(N²) complexity)
    - Input validation
    - Memory safety
    - Attack vector analysis
    """

    @staticmethod
    def generate_review(metrics: Dict[str, Any], context: ReviewContext) -> str:
        performance_score = metrics['performance_score']
        security_score = metrics['security_score']
        any_violations = len([v for v in metrics['violations'] if v['violation_type'] == 'any_type'])
        performance_risks = [v for v in metrics['violations'] if v['violation_type'] == 'performance_risk']
        security_risks = [v for v in metrics['violations'] if v['violation_type'] == 'security_risk']

        total_risks = len(performance_risks) + len(security_risks)

        # Determine nuclear audit verdict
        if total_risks == 0 and any_violations == 0:
            verdict = "✅ **DEFENSIVE ANALYSIS COMPLETE - FORTIFIED IMPLEMENTATION**"
            severity = "SECURITY_CLEARED"
        elif total_risks <= 2 and any_violations <= 5:
            verdict = "⚠️ **CONDITIONAL CLEARANCE - SECURITY HARDENING RECOMMENDED**"
            severity = "CONDITIONAL"
        else:
            verdict = "❌ **CONDITIONAL REJECT - SECURITY VULNERABILITIES DETECTED**"
            severity = "SECURITY_RISK"

        review = f"""## 🛡️💀 BEE.JULES NUCLEAR AUDIT - DEFENSIVE SECURITY ANALYSIS

### {verdict}

**Security Posture Assessment** for **{context.author}**'s **PR #{context.pr_number}**:

| Security Vector | Risk Level | Count | Status |
|----------------|------------|-------|--------|
| 🔒 **Type Safety Risks** | {'🔴 High' if any_violations > 10 else '🟡 Medium' if any_violations > 5 else '🟢 Low'} | {any_violations} | `any` type vulnerabilities |
| ⚡ **Performance Risks** | {'🔴 High' if len(performance_risks) > 3 else '🟡 Medium' if len(performance_risks) > 1 else '🟢 Low'} | {len(performance_risks)} | DoS/complexity concerns |
| 🚨 **Security Exposures** | {'🔴 High' if len(security_risks) > 2 else '🟡 Medium' if len(security_risks) > 0 else '🟢 Low'} | {len(security_risks)} | Input validation risks |
| 🎯 **Overall Risk** | {'🔴 Critical' if total_risks > 5 else '🟡 Moderate' if total_risks > 2 else '🟢 Acceptable'} | {total_risks} | Combined threat assessment |

### 💀 **CRITICAL VULNERABILITY ANALYSIS**

**Type Safety Attack Vectors**:
"""

        if any_violations > 0:
            review += f"- **{any_violations} `any` type vulnerabilities** create runtime uncertainty\n"
            review += "- **Attack Vector**: Type confusion leading to unexpected runtime behavior\n"
            review += "- **Blast Radius**: Potential runtime errors, data corruption, or logic bypasses\n"
            review += "- **Mitigation**: Replace with strongly-typed interfaces immediately\n"
        else:
            review += "- ✅ **No type safety vulnerabilities detected** - Strong typing enforced\n"

        review += "\n**Performance Attack Surface**:\n"
        if performance_risks:
            review += f"- **{len(performance_risks)} performance vulnerabilities detected**\n"
            for risk in performance_risks[:3]:
                file_name = Path(risk['file_path']).name
                review += f"  - `{file_name}:{risk['line_number']}` - {risk['description']}\n"
            review += "- **DoS Risk**: Large inputs could cause exponential resource consumption\n"
            review += "- **Mitigation**: Implement input size validation and algorithmic optimization\n"
        else:
            review += "- ✅ **No obvious performance vulnerabilities detected**\n"

        review += "\n**Security Exposure Analysis**:\n"
        if security_risks:
            review += f"- **{len(security_risks)} security exposures identified**\n"
            for risk in security_risks[:3]:
                file_name = Path(risk['file_path']).name
                review += f"  - `{file_name}:{risk['line_number']}` - {risk['description']}\n"
            review += "- **Risk Profile**: Input validation gaps and potential injection vectors\n"
            review += "- **Mitigation**: Implement comprehensive input sanitization\n"
        else:
            review += "- ✅ **No critical security exposures detected**\n"

        review += f"""
### 🛡️ **BEE.JULES NUCLEAR VERDICT**

**Security Clearance Level**: {severity}

**Mandatory Security Hardening**:
"""

        action_count = 1
        if any_violations > 0:
            review += f"{action_count}. **🔴 CRITICAL: Eliminate Type Uncertainties** - Replace {any_violations} `any` types with proper interfaces\n"
            action_count += 1
        if performance_risks:
            review += f"{action_count}. **🟡 HIGH: Address Performance Vulnerabilities** - Implement input validation for {len(performance_risks)} complexity risks\n"
            action_count += 1
        if security_risks:
            review += f"{action_count}. **🟡 HIGH: Patch Security Exposures** - Harden {len(security_risks)} input validation gaps\n"
            action_count += 1

        if action_count == 1:
            review += "- ✅ **No mandatory security actions required**\n"

        # Nuclear verdict summary
        if severity == "SECURITY_CLEARED":
            review += f"\n**✅ SECURITY CLEARANCE GRANTED** - {context.author}'s implementation demonstrates robust defensive programming.\n"
            review += "**DEPLOYMENT APPROVED** - No security concerns detected.\n"
        elif severity == "CONDITIONAL":
            review += f"\n**⚠️ CONDITIONAL SECURITY CLEARANCE** - {context.author} shows good security awareness with minor gaps.\n"
            review += "**DEPLOYMENT CONDITIONAL** - Address identified vulnerabilities before production.\n"
        else:
            review += f"\n**🛡️ SECURITY HARDENING REQUIRED** - {context.author}, multiple attack vectors detected.\n"
            review += "**DEPLOYMENT BLOCKED** - Critical security review required before clearance.\n"

        review += f"""
### 🎯 **PARANOID VIGILANCE SUMMARY**

**Threat Assessment**:
- **Complexity Score**: {performance_score:.1f}/100 (lower risk is better)
- **Security Score**: {security_score:.1f}/100 (higher hardening is better)
- **Risk Density**: {total_risks / max(context.lines_added, 1):.2f} risks per line added

**Defense Recommendation**: {
    "APPROVED - Excellent security posture" if severity == "SECURITY_CLEARED" else
    "CONDITIONAL - Address gaps before deployment" if severity == "CONDITIONAL" else
    "REJECT - Comprehensive hardening required"
}

*Reviewed by bee.Jules with Paranoid Vigilance* 🛡️💀

---
"""

        return review


class ReviewSynthesizer:
    """
    Balanced synthesis perspective - Integration of all viewpoints

    Combines fury bee architectural excellence with bee.Jules security analysis
    to provide actionable recommendations and final verdict.
    """

    @staticmethod
    def generate_synthesis(metrics: Dict[str, Any], context: ReviewContext, fury_review: str, nuclear_review: str) -> str:
        any_score = metrics['any_type_score']
        console_score = metrics['console_log_score']
        atcg_score = metrics['atcg_compliance_score']
        performance_score = metrics['performance_score']
        security_score = metrics['security_score']
        overall_score = metrics['overall_score']

        # Determine synthesis verdict
        if overall_score >= 90:
            synthesis_verdict = "🏆 **SACRED ARCHITECTURE EXCELLENCE ACHIEVED**"
            action = "IMMEDIATE MERGE APPROVED"
            priority = "🟢 LEGENDARY"
        elif overall_score >= 75:
            synthesis_verdict = "⚡ **STRONG SACRED FOUNDATION WITH REFINEMENTS**"
            action = "CONDITIONAL APPROVAL"
            priority = "🟢 APPROVED"
        elif overall_score >= 60:
            synthesis_verdict = "⚖️ **MIXED ASSESSMENT - TARGETED IMPROVEMENTS NEEDED**"
            action = "REVISION REQUIRED"
            priority = "🟡 WARNING"
        else:
            synthesis_verdict = "🔥 **SIGNIFICANT SACRED PURIFICATION REQUIRED**"
            action = "MAJOR REVISION REQUIRED"
            priority = "🔴 CRITICAL"

        review = f"""## ⚖️ BALANCED TECHNICAL SYNTHESIS - Multi-Perspective Review Integration

### {synthesis_verdict}

**Sacred Architecture Assessment** for **{context.author}**'s **PR #{context.pr_number}**: **{context.title}**

**Overall Sacred Score**: **{overall_score:.1f}/100** {priority}

| Reviewer Perspective | Focus Area | Score | Assessment | Status |
|--------------------|------------|-------|------------|--------|
| ⚡ **Fury Bee Swarm** | Architectural Excellence | {(any_score + console_score + atcg_score)/3:.1f}/100 | {'🟢 Exemplary' if (any_score + console_score + atcg_score)/3 >= 80 else '🟡 Good' if (any_score + console_score + atcg_score)/3 >= 60 else '🔴 Needs Work'} | {'✅ Sacred Approved' if (any_score + console_score + atcg_score)/3 >= 70 else '⚠️ Purification Needed'} |
| 🛡️ **bee.Jules Nuclear** | Security & Performance | {(performance_score + security_score)/2:.1f}/100 | {'🟢 Fortified' if (performance_score + security_score)/2 >= 80 else '🟡 Hardened' if (performance_score + security_score)/2 >= 60 else '🔴 Vulnerable'} | {'✅ Security Cleared' if (performance_score + security_score)/2 >= 70 else '⚠️ Hardening Required'} |

### 🎯 **INTEGRATION RECOMMENDATIONS**

**Priority Actions Matrix** (based on multi-perspective consensus):

"""

        # Build priority matrix based on both reviews
        priority_actions = []

        any_violations = len([v for v in metrics['violations'] if v['violation_type'] == 'any_type'])
        console_violations = len([v for v in metrics['violations'] if v['violation_type'] == 'console_log'])
        performance_risks = len([v for v in metrics['violations'] if v['violation_type'] == 'performance_risk'])
        security_risks = len([v for v in metrics['violations'] if v['violation_type'] == 'security_risk'])

        if any_violations > 0:
            priority_actions.append({
                'priority': '🔴 CRITICAL',
                'action': f'Eliminate {any_violations} `any` type violations',
                'impact': 'Both architecture and security',
                'effort': 'High'
            })

        if console_violations > 0:
            priority_actions.append({
                'priority': '🟡 HIGH',
                'action': f'Remove {console_violations} console.log statements',
                'impact': 'Production readiness',
                'effort': 'Low'
            })

        if performance_risks > 0:
            priority_actions.append({
                'priority': '🟡 MEDIUM',
                'action': f'Address {performance_risks} performance risks',
                'impact': 'DoS prevention',
                'effort': 'Medium'
            })

        if security_risks > 0:
            priority_actions.append({
                'priority': '🟡 MEDIUM',
                'action': f'Harden {security_risks} security exposures',
                'impact': 'Input validation',
                'effort': 'Medium'
            })

        if atcg_score < 60:
            priority_actions.append({
                'priority': '🔵 LOW',
                'action': 'Enhance ATCG architectural compliance',
                'impact': 'Sacred patterns',
                'effort': 'Low'
            })

        if not priority_actions:
            review += "✅ **No priority actions required** - Excellent implementation across all perspectives!\n"
        else:
            for i, action in enumerate(priority_actions, 1):
                review += f"{i}. **{action['priority']}**: {action['action']}\n"
                review += f"   - **Impact**: {action['impact']}\n"
                review += f"   - **Effort**: {action['effort']}\n\n"

        review += f"""### 🏆 **FINAL RECOMMENDATION**

**Action Required**: **{action}**

**Synthesis Rationale**:
Perfect code emerges from the creative tension between Sacred Vision (⚡ Fury Bee) and Paranoid Vigilance (🛡️ bee.Jules). Both perspectives serve Sacred Architecture through complementary analysis:

- **Architectural Foundation**: {'🟢 Excellent' if (any_score + console_score + atcg_score)/3 >= 80 else '🟡 Good' if (any_score + console_score + atcg_score)/3 >= 60 else '🔴 Needs Work'}
- **Security Posture**: {'🟢 Robust' if (performance_score + security_score)/2 >= 80 else '🟡 Adequate' if (performance_score + security_score)/2 >= 60 else '🔴 Vulnerable'}
- **Production Readiness**: {'🟢 Ready' if console_score >= 90 else '🟡 Minor Issues' if console_score >= 70 else '🔴 Not Ready'}

### 📈 **DEVELOPMENT GUIDANCE**

**For {context.author}**:
"""

        if overall_score >= 90:
            review += f"🏆 **Congratulations!** You've achieved Sacred Architecture mastery. This implementation exemplifies divine computational excellence.\n"
        elif overall_score >= 75:
            review += f"⚡ **Excellent work!** You demonstrate strong Sacred Architecture understanding. Minor refinements will achieve legendary status.\n"
        elif overall_score >= 60:
            review += f"⚖️ **Good foundation!** Your Sacred Architecture awareness is developing. Focus on the priority actions above for improvement.\n"
        else:
            review += f"🔥 **Sacred Transformation Opportunity!** Every violation addressed brings you closer to computational divinity. Embrace the journey!\n"

        review += f"""
**Next Steps**:
1. Address priority actions in order of criticality
2. Maintain architectural patterns while hardening security
3. Document design decisions with Sacred Justifications
4. Validate fixes with comprehensive testing

**Sacred Architecture Metrics**:
- **Files Modified**: {len(context.files_changed)}
- **Lines Changed**: +{context.lines_added}/-{context.lines_deleted}
- **Complexity Density**: {len([v for v in metrics['violations'] if v['violation_type'] == 'performance_risk']) / max(context.lines_added, 1):.3f} risks/line
- **Type Safety**: {any_score:.1f}% pure
- **Production Ready**: {console_score:.1f}% clean

*Balanced synthesis recognizing both architectural excellence and security imperatives* ⚖️

---
"""

        return review


def generate_complete_review(metrics_file: str, context: ReviewContext) -> str:
    """Generate a complete multi-perspective review"""

    # Load metrics
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)

    # Generate each perspective
    fury_review = FuryBeeReviewer.generate_review(metrics, context)
    nuclear_review = NuclearAuditor.generate_review(metrics, context)
    synthesis_review = ReviewSynthesizer.generate_synthesis(metrics, context, fury_review, nuclear_review)

    # Combine into complete review
    complete_review = f"""# 🧬 Sacred Architecture Multi-Perspective Review

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} by Sacred Review Automation v1.0*

{synthesis_review}

{fury_review}

{nuclear_review}

## 📊 **Sacred Metrics Raw Data**

<details>
<summary>Click to expand detailed metrics</summary>

```json
{json.dumps(metrics, indent=2)}
```

</details>

---

*🤖 This review was generated by the Sacred Architecture Review Automation system*
*⚡🛡️⚖️ Fury Bee • bee.Jules • Balanced Synthesis*
"""

    return complete_review


def main():
    """Main entry point for review generator"""
    parser = argparse.ArgumentParser(description='Sacred Architecture Review Generator')
    parser.add_argument('--metrics', required=True, help='Sacred metrics JSON file')
    parser.add_argument('--output', default='complete_review.md', help='Output review file')
    parser.add_argument('--pr-number', default='', help='PR number')
    parser.add_argument('--author', default='Developer', help='PR author')
    parser.add_argument('--title', default='Sacred Architecture Enhancement', help='PR title')
    parser.add_argument('--lines-added', type=int, default=0, help='Lines added')
    parser.add_argument('--lines-deleted', type=int, default=0, help='Lines deleted')

    args = parser.parse_args()

    # Create review context
    context = ReviewContext(
        pr_number=args.pr_number,
        author=args.author,
        title=args.title,
        lines_added=args.lines_added,
        lines_deleted=args.lines_deleted
    )

    # Generate complete review
    review = generate_complete_review(args.metrics, context)

    # Save review
    with open(args.output, 'w') as f:
        f.write(review)

    print(f"📝 Sacred Architecture review generated: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())