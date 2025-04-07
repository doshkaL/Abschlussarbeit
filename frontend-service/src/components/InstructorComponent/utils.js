// Funktion zur Berechnung der Assignment-Daten
export const calculateAssignmentsData = (student) => {
  const totalAssignments = student.exercises.length;

  // Gefilterte abgeschlossene Übungen
  const completedAssignments = student.exercises.filter(
    (exercise) => exercise.grade_result !== null
  ).length;

  // Gesamtpunkte aus `grade_result` extrahieren und summieren
  const totalScore = student.exercises.reduce((sum, exercise) => {
    if (exercise.grade_result) {
      // Extrahiere die "Erzielte Punkte" aus `grade_result`
      const match = exercise.grade_result.match(/Erzielte Punkte: (\d+)\/(\d+)/);
      if (match) {
        const earnedPoints = parseFloat(match[1]); // Erzielte Punkte
        return sum + earnedPoints; // Summiere die Punkte
      }
    }
    return sum; // Falls kein `grade_result`, bleibt die Summe unverändert
  }, 0);

  // Gesamtpunkte der abgeschlossenen Aufgaben ermitteln
  const totalPossibleScore = student.exercises.reduce((sum, exercise) => {
    if (exercise.grade_result) {
      // Extrahiere die möglichen Gesamtpunkte aus `grade_result`
      const match = exercise.grade_result.match(/Erzielte Punkte: (\d+)\/(\d+)/);
      if (match) {
        const possiblePoints = parseFloat(match[2]); // Mögliche Gesamtpunkte
        return sum + possiblePoints;
      }
    }
    return sum;
  }, 0);

  // Durchschnitt berechnen (als Prozentsatz)
  const averageScore =
    completedAssignments > 0 && totalPossibleScore > 0
      ? (totalScore / totalPossibleScore) * 100
      : 0;

  return {
    completedAssignments, // Anzahl der abgeschlossenen Übungen
    totalAssignments, // Gesamtanzahl der Übungen
    totalScore, // Gesamtsumme der erzielten Punkte
    averageScore, // Durchschnittlicher Prozentsatz
  };
};
