import { useParams, Link, Outlet } from 'react-router-dom';
import { Tab, Tabs, Paper, Box } from '@mui/material';
import { useState } from 'react';

export default function CoursePage() {
  const { id } = useParams();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <Paper elevation={3} sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} variant="fullWidth">
          <Tab label="Overview" component={Link} to={`/courses/${id}`} />
          <Tab label="Calendar" component={Link} to={`/courses/${id}/calendar`} />
          <Tab label="Assignments" component={Link} to={`/courses/${id}/assignments`} />
          <Tab label="Discussions" component={Link} to={`/courses/${id}/forums`} />
        </Tabs>
      </Paper>

      <Box sx={{ p: 3 }}>
        <Outlet />
      </Box>
    </div>
  );
}