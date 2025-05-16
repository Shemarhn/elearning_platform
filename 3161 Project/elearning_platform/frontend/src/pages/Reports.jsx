import { useState, useEffect } from 'react';
import API from '../api/apiService';
import { Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

export default function Reports() {
  const [topCourses, setTopCourses] = useState([]);
  const [topStudents, setTopStudents] = useState([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const [coursesRes, studentsRes] = await Promise.all([
          API.get('/reports/top-courses'),
          API.get('/reports/top-students')
        ]);
        setTopCourses(coursesRes.data);
        setTopStudents(studentsRes.data);
      } catch (err) {
        console.error('Failed to load reports', err);
      }
    };
    fetchReports();
  }, []);

  return (
    <div>
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Top 10 Most Enrolled Courses
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Course ID</TableCell>
                <TableCell>Course Name</TableCell>
                <TableCell>Enrollments</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topCourses.map((course) => (
                <TableRow key={course.course_id}>
                  <TableCell>{course.course_id}</TableCell>
                  <TableCell>{course.course_name}</TableCell>
                  <TableCell>{course.enrollments}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Top 10 Students by Average Grade
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Student ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Average Grade</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topStudents.map((student) => (
                <TableRow key={student.user_id}>
                  <TableCell>{student.user_id}</TableCell>
                  <TableCell>{student.full_name}</TableCell>
                  <TableCell>{student.average_grade.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </div>
  );
}