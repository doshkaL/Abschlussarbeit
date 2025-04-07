import React from "react";
import { calculateAssignmentsData } from "../InstructorComponent/utils"; 

const StudentList = ({ students, searchStudent, handleStudentSearch, setSelectedStudent, selectedCourse }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6 w-full md:w-3/4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-blue-600 items-center">
          Studenten in {selectedCourse.name}
        </h2>
      </div>

      <input
        type="text"
        placeholder="Studenten suchen..."
        value={searchStudent}
        onChange={handleStudentSearch}
        className="mb-4 w-full px-3 py-2 border rounded-lg text-sm"
      />

      <table className="min-w-full table-auto">
        <thead>
          <tr className="bg-blue-50 text-blue-600">
            <th className="px-4 py-2 text-left">Student Name</th>
            <th className="px-4 py-2 text-left">Abgeschlossene Aufgaben</th>
            <th className="px-4 py-2 text-left">Score</th>
            <th className="px-4 py-2 text-left">Details</th>
          </tr>
        </thead>
        <tbody>
          {students
            .filter((student) =>
              student.name.toLowerCase().includes(searchStudent)
            )
            .map((student) => {
              const { completedAssignments, totalAssignments, averageScore } = calculateAssignmentsData(student);
              return (
                <tr key={student.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2">{student.name}</td>
                  <td className="px-4 py-2">
                    {completedAssignments} / {totalAssignments}
                  </td>
                  <td className="px-4 py-2">{averageScore.toFixed(2)}</td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => setSelectedStudent(student)}
                      className="text-blue-600 hover:underline"
                    >
                      Details anzeigen
                    </button>
                  </td>
                </tr>
              );
            })}
        </tbody>
      </table>
    </div>
  );
};

export default StudentList;
