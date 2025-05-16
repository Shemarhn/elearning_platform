import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api/apiService';
import { Typography, List, ListItem, Paper } from '@mui/material';

export default function Calendar() {
  const { courseId } = useParams();
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await API.get(`/calendar/course/${courseId}`);
        setEvents(res.data);
      } catch (err) {
        console.error('Failed to load events', err);
      }
    };
    fetchEvents();
  }, [courseId]);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Course Events
      </Typography>
      <List>
        {events.map((event) => (
          <ListItem key={event.event_id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <Typography variant="h6">{event.title}</Typography>
            <Typography variant="body2" color="text.secondary">
              {new Date(event.event_date).toLocaleString()}
            </Typography>
            <Typography>{event.description}</Typography>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}