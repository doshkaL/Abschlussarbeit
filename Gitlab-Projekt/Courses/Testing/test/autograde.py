import subprocess
import re
import os
import sys

def extract_test_results(pytest_output):
    results = []
    for line in pytest_output.splitlines():
        # Match test names and results (e.g., "test/unitest.py::test_fibonacci_0 PASSED")
        match = re.search(r"::(?P<test_name>[^\s:]+)\s+(?P<result>PASSED|FAILED)", line)
        if match:
            test_name = match.group("test_name")  # Extract the test function name
            result = match.group("result").lower()  # Convert to lowercase
            results.append({
                "test_name": test_name,
                "result": result
            })
    return results

def extract_weights(test_dir):
    weights = {}
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract methods with Gewichtung in their docstring
                        test_cases = re.findall(
                            r"def\s+(\w+)\(.*?\):\s*\"\"\"[^\"]*Punkt:\s*(\d+)",
                            content,
                            re.DOTALL
                        )
                        for method_name, weight in test_cases:
                            weights[method_name] = int(weight)
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {filepath}: {e}")
    return weights

def calculate_grade(test_results, weights):
    total_weight = sum(weights.values())
    obtained_score = sum(weights.get(test['test_name'], 0) for test in test_results if test['result'] == 'passed')

    if total_weight == 0:
        return "Keine Tests vorhanden", 0, 0

    percentage = (obtained_score / total_weight) * 100
    if percentage >= 90:
        grade = "Note: 1.0"
    elif percentage >= 80:
        grade = "Note: 2.0"
    elif percentage >= 70:
        grade = "Note: 3.0"
    elif percentage >= 60:
        grade = "Note: 3.5"    
    elif percentage == 50:
        grade = "Note: 4.0"
    else:
        grade = "Note: 5.0"

    return grade, obtained_score, total_weight

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = current_dir

    # Überprüfe, ob das Verzeichnis existiert und nicht leer ist
    if not os.path.exists(test_dir) or not os.listdir(test_dir):
        print(f"Fehler: Testverzeichnis {test_dir} existiert nicht oder ist leer.")
        sys.exit(1)

    try:
        # Setze die Umgebungsvariablen
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{os.getcwd()}:{os.path.join(os.getcwd(), 'src')}"

        # Führe pytest auf den Testdateien aus
        print("Running pytest on:", os.path.join(test_dir, "testing.py"))
        result = subprocess.run(
            ["pytest", os.path.join(test_dir, "testing.py"), "-v"],  # Use -v for verbose output
            capture_output=True,
            text=True,
            env=env
        )

        # Print the pytest output and errors
        print("=== pytest Output ===")
        print(result.stdout)

        if result.stderr:
            print("=== pytest Errors ===")
            print(result.stderr)

        # Extrahiere Testergebnisse und Gewichtungen
        test_results = extract_test_results(result.stdout)
        weights = extract_weights(test_dir)

        # Berechne die Note
        grade, obtained_score, total_weight = calculate_grade(test_results, weights)

        # Ergebnisse ausgeben
        print(f"\nErzielte Punkte: {obtained_score}/{total_weight}")
        print(f"{grade}")
        print("\nDetaillierte Ergebnisse:")
        for test in test_results:
            status = "Bestanden" if test['result'] == 'passed' else "Nicht bestanden"
            points = weights.get(test['test_name'], 0) if test['result'] == 'passed' else 0
            print(f"{test['test_name']}: {status}, Punkte: {points}/{weights.get(test['test_name'], 0)}")
    except Exception as e:
        print(f"Fehler bei der Testausführung: {e}")
