import React from "react";

const StudentDetails = ({ student, onFeedbackClick }) => {
  // Helferfunktion: Extrahiert nur die Note aus dem `grade_result`
  const extractGrade = (gradeResult) => {
    const match = gradeResult?.match(/Note: (\d+\.\d+)/); // Suche nach "Note: X.X"
    return match ? match[1] : "Noch nicht bewertet"; // Gib nur die Zahl zurück
  };

  // Übungen nach Note sortieren
  const sortedExercises = [...student.exercises].sort((a, b) => {
    const getGrade = (gradeResult) => {
      const match = gradeResult?.match(/Note: (\d+\.\d+)/);
      return match ? parseFloat(match[1]) : Infinity; // Falls keine Note vorhanden, setze Infinity
    };

    return getGrade(a.grade_result) - getGrade(b.grade_result); // Sortierung aufsteigend
  });

  return (
    <div className="mt-6 bg-white shadow rounded-lg p-4">
      <h3 className="text-xl font-semibold text-blue-600 mb-4">
        Details für {student.name}
      </h3>
      <table className="table-auto w-full text-sm text-left border-collapse">
        <thead>
          <tr className="bg-blue-50 text-blue-600">
            <th className="py-2 px-4 border">Übungsname</th>
            <th className="py-2 px-4 border">Note</th>
            <th className="py-2 px-4 border">Aktionen</th>
          </tr>
        </thead>
        <tbody>
          {sortedExercises.map((exercise, index) => (
            <tr
              key={index}
              className={`${index % 2 === 0 ? "bg-gray-50" : "bg-white"}`}
            >
              <td className="py-2 px-4 border">{exercise.name}</td>
              <td className="py-2 px-4 border">
                {extractGrade(exercise.grade_result)}
              </td>
              <td className="py-2 px-4 border">
                <button
                  className="text-blue-600 underline hover:text-blue-800"
                  onClick={() => onFeedbackClick(exercise)}
                >
                  Detailliertes Feedback
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentDetails;
