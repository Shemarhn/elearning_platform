import React, { useEffect, useState } from "react";

function CoursesList() {
  const [courses, setCourses] = useState([]);
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    fetch(`${apiBaseUrl}/courses`)
      .then((res) => res.json())
      .then((data) => setCourses(data))
      .catch((error) => console.error("Error fetching courses:", error));
  }, [apiBaseUrl]);

  return (
    <div>
      <h1>Courses</h1>
      <ul>
        {courses.map((c) => (
          <li key={c.course_id}>{c.course_name}</li>
        ))}
      </ul>
    </div>
  );
}

export default CoursesList;
