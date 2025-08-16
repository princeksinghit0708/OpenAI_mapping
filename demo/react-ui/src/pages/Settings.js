import React from 'react';
import { Container, Typography, Alert, Box } from '@mui/material';

const Settings = () => {
  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        ⚙️ Settings
      </Typography>
      
      <Box sx={{ mt: 4 }}>
        <Alert severity="info">
          <Typography variant="body1">
            <strong>🚧 Coming Soon!</strong> This page will allow you to configure 
            API endpoints, LLM providers, and application preferences.
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default Settings;
