"""
Measure coverage for Part 2 tests (LLM-generated tests).
This script measures coverage for the two selected variants:
- HumanEval_6 (parse_nested_parens) - Llama_cot
- HumanEval_7 (filter_by_substring) - Llama_cot
"""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
import re
from pathlib import Path


def measure_part2_coverage():
    """Measure coverage for Part 2 test files."""
    
    base_dir = Path(__file__).parent.parent
    tests_dir = base_dir / "tests"
    solutions_dir = base_dir / "solutions"
    reports_dir = base_dir / "coverage_reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Define the two variants we're testing
    variants = [
        {
            'problem_num': '6',
            'variant_id': 'Llama_cot',
            'entry_point': 'parse_nested_parens',
            'module_name': 'problem_6_Llama_cot'
        },
        {
            'problem_num': '7',
            'variant_id': 'Llama_cot',
            'entry_point': 'filter_by_substring',
            'module_name': 'problem_7_Llama_cot'
        }
    ]
    
    print("Measuring coverage for Part 2 (LLM-generated tests)...")
    print(f"{'='*70}")
    
    coverage_results = {}
    
    for variant in variants:
        problem_num = variant['problem_num']
        variant_id = variant['variant_id']
        entry_point = variant['entry_point']
        module_name = variant['module_name']
        
        test_file = tests_dir / f"test_problem_{problem_num}_{variant_id}.py"
        
        if not test_file.exists():
            print(f"⚠️  Test file not found: {test_file}")
            continue
        
        result_key = f"problem_{problem_num}_{variant_id}"
        print(f"\n📊 Testing problem_{problem_num} ({entry_point}) [{variant_id}]...")
        
        # Run pytest with coverage
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_file),
            f"--cov=solutions.{module_name}",
            "--cov-branch",  # Enable branch coverage
            "--cov-report=term",
            "--cov-report=xml",
            f"--cov-report=html:{reports_dir}/{module_name}",
            "-v"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(base_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse coverage from stdout
            output = result.stdout + result.stderr
            line_cov = 0.0
            branch_cov = 0.0
            tests_passed = 0
            tests_failed = 0
            tests_total = 0
            
            # Parse test results
            passed_match = re.search(r'(\d+)\s+passed', output)
            failed_match = re.search(r'(\d+)\s+failed', output)
            error_match = re.search(r'(\d+)\s+error', output)
            
            if passed_match:
                tests_passed = int(passed_match.group(1))
            if failed_match:
                tests_failed = int(failed_match.group(1))
            if error_match:
                tests_failed += int(error_match.group(1))
            tests_total = tests_passed + tests_failed
            
            # Parse coverage percentages
            lines = output.split('\n')
            for i, line in enumerate(lines):
                # Look for lines with the module name and percentage
                if module_name in line or f"solutions/{module_name}" in line:
                    parts = line.split()
                    percentages = []
                    for part in parts:
                        if "%" in part:
                            try:
                                pct = float(part.replace('%', ''))
                                percentages.append(pct)
                            except:
                                pass
                    if len(percentages) >= 1:
                        line_cov = percentages[0]
                    if len(percentages) >= 2:
                        branch_cov = percentages[1]
                
                # Also check for TOTAL line
                if "TOTAL" in line and ("Cover" in lines[i-1] if i > 0 else False):
                    parts = line.split()
                    percentages = []
                    for part in parts:
                        if "%" in part:
                            try:
                                pct = float(part.replace('%', ''))
                                percentages.append(pct)
                            except:
                                pass
                    if len(percentages) >= 1 and line_cov == 0.0:
                        line_cov = percentages[0]
                    if len(percentages) >= 2 and branch_cov == 0.0:
                        branch_cov = percentages[1]
            
            # Try parsing XML if available
            xml_file = base_dir / "coverage.xml"
            if xml_file.exists() and (line_cov == 0.0 or branch_cov == 0.0):
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    if line_cov == 0.0:
                        line_rate = float(root.get('line-rate', 0)) * 100
                        line_cov = line_rate
                    if branch_cov == 0.0:
                        branch_rate = float(root.get('branch-rate', 0)) * 100
                        branch_cov = branch_rate
                    
                    # Try to get from packages
                    packages = root.findall('.//package')
                    for package in packages:
                        classes = package.findall('.//class')
                        for cls in classes:
                            if line_cov == 0.0:
                                line_rate = float(cls.get('line-rate', 0)) * 100
                                line_cov = line_rate
                            if branch_cov == 0.0:
                                branch_rate = float(cls.get('branch-rate', 0)) * 100
                                branch_cov = branch_rate
                            if line_cov > 0 and branch_cov > 0:
                                break
                except Exception as e:
                    pass
                
                # Clean up XML file
                xml_file.unlink()
            
            coverage_results[result_key] = {
                'problem_num': problem_num,
                'variant_id': variant_id,
                'entry_point': entry_point,
                'line_coverage': round(line_cov, 2),
                'branch_coverage': round(branch_cov, 2),
                'tests_passed': tests_passed,
                'tests_failed': tests_failed,
                'tests_total': tests_total,
                'passed': result.returncode == 0
            }
            
            if line_cov > 0:
                print(f"   Line coverage: {line_cov:.2f}%")
                if branch_cov > 0:
                    print(f"   Branch coverage: {branch_cov:.2f}%")
            else:
                print(f"   ⚠️  Could not extract coverage metrics")
            
            if tests_total > 0:
                print(f"   Tests: {tests_passed}/{tests_total} passed", end="")
                if tests_failed > 0:
                    print(f" ({tests_failed} failed)")
                else:
                    print()
            elif result.returncode == 0:
                print(f"   ✅ Tests passed")
            else:
                print(f"   ⚠️  Tests failed or had issues")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}")
        
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  Timeout while measuring coverage")
            coverage_results[result_key] = {
                'problem_num': problem_num,
                'variant_id': variant_id,
                'entry_point': entry_point,
                'line_coverage': 0.0,
                'branch_coverage': 0.0,
                'tests_passed': 0,
                'tests_failed': 0,
                'tests_total': 0,
                'passed': False,
                'error': 'Timeout'
            }
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            coverage_results[result_key] = {
                'problem_num': problem_num,
                'variant_id': variant_id,
                'entry_point': entry_point,
                'line_coverage': 0.0,
                'branch_coverage': 0.0,
                'tests_passed': 0,
                'tests_failed': 0,
                'tests_total': 0,
                'passed': False,
                'error': str(e)
            }
    
    # Generate summary table
    print(f"\n{'='*70}")
    print("PART 2 COVERAGE SUMMARY (LLM-Generated Tests)")
    print(f"{'='*70}")
    print(f"{'Problem':<20} {'Entry Point':<25} {'Line %':>9} {'Branch %':>10} {'Tests':>12} {'Status':<8}")
    print(f"{'-'*70}")
    
    for key in sorted(coverage_results.keys()):
        result = coverage_results[key]
        problem_id = f"problem_{result['problem_num']}"
        entry = result['entry_point']
        line_cov = result['line_coverage']
        branch_cov = result['branch_coverage']
        tests_passed = result['tests_passed']
        tests_total = result['tests_total']
        passed = result.get('passed', False)
        
        tests_str = f"{tests_passed}/{tests_total}" if tests_total > 0 else "N/A"
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{problem_id:<20} {entry:<25} {line_cov:>8.2f}%  {branch_cov:>8.2f}%  {tests_str:>12}  {status}")
    
    # Save results
    results_path = base_dir / "part2_coverage_results.json"
    with open(results_path, 'w') as f:
        json.dump(coverage_results, f, indent=2)
    
    print(f"{'='*70}")
    print(f"\n✅ Coverage results saved to: {results_path}")
    print(f"   HTML reports available in: {reports_dir}")
    
    return coverage_results


if __name__ == '__main__':
    measure_part2_coverage()



