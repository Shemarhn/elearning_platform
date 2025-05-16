import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api/apiService';
import { Button, TextField, Typography, List, ListItem, Paper, Box } from '@mui/material';

export default function Assignments() {
  const { courseId } = useParams();
  const [assignments, setAssignments] = useState([]);
  const [submissionContent, setSubmissionContent] = useState('');

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const res = await API.get(`/assignments?course_id=${courseId}`);
        setAssignments(res.data);
      } catch (err) {
        console.error('Failed to load assignments', err);
      }
    };
    fetchAssignments();
  }, [courseId]);

  const handleSubmit = async (assignmentId) => {
    try {
      await API.post(`/assignments/${assignmentId}/submit`, { content: submissionContent });
      alert('Assignment submitted successfully!');
      setSubmissionContent('');
    } catch (err) {
      alert('Submission failed: ' + err.response?.data?.error);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Course Assignments
      </Typography>
      <List>
        {assignments.map((assignment) => (
          <ListItem key={assignment.assignment_id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <Typography variant="h6">{assignment.title}</Typography>
            <Typography variant="body2" color="text.secondary">
              Due: {new Date(assignment.due_date).toLocaleString()}
            </Typography>
            <Typography>{assignment.description}</Typography>
            <Box sx={{ mt: 2, width: '100%' }}>
              <TextField
                multiline
                fullWidth
                rows={4}
                label="Your submission"
                value={submissionContent}
                onChange={(e) => setSubmissionContent(e.target.value)}
              />
              <Button 
                variant="contained" 
                sx={{ mt: 2 }}
                onClick={() => handleSubmit(assignment.assignment_id)}
              >
                Submit Assignment
              </Button>
            </Box>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}