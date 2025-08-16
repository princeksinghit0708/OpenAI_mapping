import React from 'react';
import { Container, Typography, Alert, Box } from '@mui/material';

const TestGeneration = () => {
  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        🧪 Test Generation
      </Typography>
      
      <Box sx={{ mt: 4 }}>
        <Alert severity="info">
          <Typography variant="body1">
            <strong>🚧 Coming Soon!</strong> This page will generate comprehensive test suites 
            for your PySpark transformations with mock data and validation rules.
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default TestGeneration;
