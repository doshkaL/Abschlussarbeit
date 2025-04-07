import React from "react";

const CourseList = ({ courses, searchCourse, handleCourseSearch, handleCourseClick, selectedCourse }) => {
  return (
    <section className="bg-white shadow-md rounded-xl p-4 w-full md:w-1/4">
      <h2 className="text-lg font-semibold mb-4 text-grey-600 text-center">Kurse</h2>
      <input
        type="text"
        placeholder="Kurse suchen..."
        value={searchCourse}
        onChange={handleCourseSearch}
        className="mb-4 w-full px-3 py-2 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <ul className="space-y-1">
        {courses.map((course) => (
          <li
            key={course.id}
            className={`p-4 border rounded-xl text-sm cursor-pointer text-center ${
              selectedCourse?.id === course.id
                ? "bg-blue-50 border-blue-400 text-blue-700"
                : "hover:bg-gray-100 hover:shadow-lg"
            }`}
            onClick={() => handleCourseClick(course)}
          >
            <span className="font-medium">{course.name}</span>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default CourseList;
