import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import API from '../api/apiService';
import { Card, CardContent, Typography, Grid, Button } from '@mui/material';

export default function Dashboard() {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const endpoint = user?.role === 'student' 
          ? `/courses?student_id=${user.user_id}`
          : user?.role === 'lecturer'
          ? `/courses?lecturer_id=${user.user_id}`
          : '/courses';
        
        const res = await API.get(endpoint);
        setCourses(res.data);
      } catch (err) {
        console.error('Failed to load courses', err);
      }
    };
    fetchCourses();
  }, [user]);

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Welcome, {user?.name || 'User'}!
        </h1>
        
        <div className="mb-8">
          <Typography variant="h5" gutterBottom>
            Your Courses
          </Typography>
          <Grid container spacing={3}>
            {courses.map((course) => (
              <Grid item xs={12} sm={6} md={4} key={course.course_id}>
                <Card className="h-full">
                  <CardContent>
                    <Typography variant="h6">{course.course_name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {course.description}
                    </Typography>
                  </CardContent>
                  <div className="p-2 flex space-x-2">
                    <Button
                      component={Link}
                      to={`/courses/${course.course_id}`}
                      size="small"
                      variant="outlined"
                    >
                      View
                    </Button>
                    <Button
                      component={Link}
                      to={`/courses/${course.course_id}/assignments`}
                      size="small"
                      variant="outlined"
                    >
                      Assignments
                    </Button>
                  </div>
                </Card>
              </Grid>
            ))}
          </Grid>
        </div>

        <div className="space-x-4">
          <Button
            component={Link}
            to="/reports"
            variant="contained"
            color="primary"
          >
            View Reports
          </Button>
          {user?.role === 'lecturer' && (
            <Button
              component={Link}
              to="/courses/new"
              variant="outlined"
              color="primary"
            >
              Create Course
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}