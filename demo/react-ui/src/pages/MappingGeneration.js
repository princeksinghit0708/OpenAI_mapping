import React from 'react';
import { Container, Typography, Alert, Box } from '@mui/material';

const MappingGeneration = () => {
  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        🔄 Mapping Generation
      </Typography>
      
      <Box sx={{ mt: 4 }}>
        <Alert severity="info">
          <Typography variant="body1">
            <strong>🚧 Coming Soon!</strong> This page will allow you to generate PySpark transformations 
            from your Excel mapping files with custom configuration options.
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default MappingGeneration;
