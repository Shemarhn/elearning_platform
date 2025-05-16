import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api/apiService';
import { Button, TextField, Typography, List, ListItem, Paper, Box } from '@mui/material';

export default function Forums() {
  const { courseId } = useParams();
  const [threads, setThreads] = useState([]);
  const [newThreadTitle, setNewThreadTitle] = useState('');
  const [newThreadContent, setNewThreadContent] = useState('');

  useEffect(() => {
    const fetchThreads = async () => {
      try {
        // First get forum ID for this course
        const forumRes = await API.get(`/forums?course_id=${courseId}`);
        if (forumRes.data.length > 0) {
          const threadsRes = await API.get(`/forums/${forumRes.data[0].forum_id}/threads`);
          setThreads(threadsRes.data);
        }
      } catch (err) {
        console.error('Failed to load threads', err);
      }
    };
    fetchThreads();
  }, [courseId]);

  const handleCreateThread = async () => {
    try {
      // Get forum ID for this course
      const forumRes = await API.get(`/forums?course_id=${courseId}`);
      if (forumRes.data.length > 0) {
        await API.post(`/forums/${forumRes.data[0].forum_id}/threads`, {
          title: newThreadTitle,
          content: newThreadContent
        });
        alert('Thread created successfully!');
        setNewThreadTitle('');
        setNewThreadContent('');
        // Refresh threads
        const threadsRes = await API.get(`/forums/${forumRes.data[0].forum_id}/threads`);
        setThreads(threadsRes.data);
      }
    } catch (err) {
      alert('Failed to create thread: ' + err.response?.data?.error);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Course Discussions
      </Typography>
      
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6">Create New Thread</Typography>
        <TextField
          fullWidth
          label="Title"
          value={newThreadTitle}
          onChange={(e) => setNewThreadTitle(e.target.value)}
          sx={{ mb: 2 }}
        />
        <TextField
          fullWidth
          multiline
          rows={4}
          label="Content"
          value={newThreadContent}
          onChange={(e) => setNewThreadContent(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" onClick={handleCreateThread}>
          Post Thread
        </Button>
      </Box>

      <List>
        {threads.map((thread) => (
          <ListItem key={thread.thread_id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <Typography variant="h6">{thread.title}</Typography>
            <Typography variant="body2" color="text.secondary">
              Posted by {thread.user_id}
            </Typography>
            <Typography>{thread.content}</Typography>
            <Button size="small" sx={{ mt: 1 }}>
              View Replies
            </Button>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}