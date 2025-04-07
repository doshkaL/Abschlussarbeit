import React from "react";

const parseGradeResult = (gradeResult) => {
  if (!gradeResult) return { totalPoints: "N/A", grade: "N/A", testResults: [] };

  const lines = gradeResult.split("\n").map((line) => line.trim()).filter(Boolean);
  const totalPoints = lines[0]?.replace("Erzielte Punkte: ", "") || "N/A";
  const grade = lines[1]?.replace("Note: ", "") || "N/A";

  const testResults = lines
    .slice(3)
    .map((line) => {
      const match = line.match(/(test_\w+): (.+), Punkte: (\d+\/\d+)/);
      return match ? { test_name: match[1], status: match[2], points: match[3] } : null;
    })
    .filter(Boolean);

  return { totalPoints, grade, testResults };
};

const parseLinterFeedback = (feedback) => {
  if (!feedback) return { linterErrors: [], codeRating: "N/A" };

  const lines = feedback.split("\n").map((line) => line.trim()).filter(Boolean);
  const linterErrors = lines
    .slice(1)
    .map((line) => {
      const match = line.match(/(.+?):(\d+):(\d+): (\w+): (.+)/);
      return match ? { file: match[1], line: match[2], column: match[3], type: match[4], message: match[5] } : null;
    })
    .filter(Boolean);

  const codeRatingLine = lines.find((line) => line.includes("Your code has been rated"));
  const codeRating = codeRatingLine || "N/A";

  return { linterErrors, codeRating };
};

const FeedbackCard = ({ exercise, onReturn }) => {
  if (!exercise) {
    return (
      <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
        <div className="max-w-2xl mx-auto bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-semibold text-red-600 mb-4">Keine Übung ausgewählt.</h2>
          <button
            onClick={onReturn}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Zurück zu den Unterrichtsdetails
          </button>
        </div>
      </div>
    );
  }

  const { totalPoints, grade, testResults } = parseGradeResult(exercise.grade_result);
  const { linterErrors, codeRating } = parseLinterFeedback(exercise.feedback);

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
      <div className="w-full h-full bg-white p-8 overflow-auto">
        {/* Überschrift */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-semibold text-blue-600">Übung: {exercise.name}</h2>
          <button
            onClick={onReturn}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Zurück
          </button>
        </div>

        {/* Punkte und Note (untereinander) */}
        <div className="bg-gray-50 p-6 rounded-lg shadow mb-6 text-center">
          <div className="mb-4">
            <p className="text-gray-600 text-lg font-medium">Erzielte Punkte:</p>
            <p className="text-4xl font-bold text-green-600">{totalPoints}</p>
          </div>
          <div>
            <p className="text-gray-600 text-lg font-medium">Note:</p>
            <p className="text-4xl font-bold text-blue-600">{grade}</p>
          </div>
        </div>

        {/* Testergebnisse */}
        <h3 className="text-lg font-semibold text-gray-700 mt-4">Testergebnisse:</h3>
        {testResults.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300 mt-2">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border border-gray-300 px-4 py-2 text-left">Test</th>
                  <th className="border border-gray-300 px-4 py-2 text-left">Status</th>
                  <th className="border border-gray-300 px-4 py-2 text-left">Punkte</th>
                </tr>
              </thead>
              <tbody>
                {testResults.map((test, index) => (
                  <tr key={index} className={`${index % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-blue-100`}>
                    <td className="border border-gray-300 px-4 py-2">{test.test_name}</td>
                    <td className="border border-gray-300 px-4 py-2">
                      {test.status === "Bestanden" ? (
                        <span className="text-green-600 font-semibold"> {test.status}</span>
                      ) : (
                        <span className="text-red-600 font-semibold"> {test.status}</span>
                      )}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">{test.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-600">Keine Testergebnisse verfügbar.</p>
        )}

        {/* Linter-Fehlermeldungen */}
        {linterErrors.length > 0 ? (
          <>
            <h3 className="text-lg font-semibold text-gray-700 mt-6">Linter-Fehlermeldungen:</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse border border-gray-300 mt-2">
                <thead className="bg-gray-200">
                  <tr>
                    <th className="border border-gray-300 px-4 py-2 text-left">Datei</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Zeile</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Typ</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Beschreibung</th>
                  </tr>
                </thead>
                <tbody>
                  {linterErrors.map((error, index) => (
                    <tr key={index} className={`${index % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-blue-100`}>
                      <td className="border border-gray-300 px-4 py-2">{error.file}</td>
                      <td className="border border-gray-300 px-4 py-2">{error.line}</td>
                      <td className="border border-gray-300 px-4 py-2">{error.type}</td>
                      <td className="border border-gray-300 px-4 py-2">{error.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ):(
          <p className="text-green-600 font-semibold text-center mt-4">
             Es gibt keine Fehler, du hast gut gemacht! 🎉
          </p>
        )}

        {/* Code-Bewertung */}
        <p className="text-gray-700 mt-4">
          <strong>Code-Bewertung:</strong> {codeRating}
        </p>
      </div>
    </div>
  );
};

export default FeedbackCard;
