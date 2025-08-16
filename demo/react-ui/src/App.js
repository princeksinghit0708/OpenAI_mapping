import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';

// Components
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ExcelUpload from './pages/ExcelUpload';
import MappingGeneration from './pages/MappingGeneration';
import AgentWorkflow from './pages/AgentWorkflow';
import MetadataValidation from './pages/MetadataValidation';
import TestGeneration from './pages/TestGeneration';
import Settings from './pages/Settings';

// Utils
import { checkApiHealth } from './utils/api';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
});

function App() {
  const [apiStatus, setApiStatus] = useState('checking');
  
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await checkApiHealth();
      setApiStatus(health ? 'connected' : 'disconnected');
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar apiStatus={apiStatus} onHealthCheck={checkHealth} />
          
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<ExcelUpload />} />
              <Route path="/mapping" element={<MappingGeneration />} />
              <Route path="/agents" element={<AgentWorkflow />} />
              <Route path="/metadata" element={<MetadataValidation />} />
              <Route path="/tests" element={<TestGeneration />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
