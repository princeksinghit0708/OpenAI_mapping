import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  LinearProgress,
  Alert,
  Chip,
  Paper,
} from '@mui/material';
import {
  Upload as UploadIcon,
  Transform as TransformIcon,
  SmartToy as AgentIcon,
  CheckCircle as ValidateIcon,
  BugReport as TestIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { getWorkflowHistory } from '../utils/api';

const Dashboard = () => {
  const [workflowHistory, setWorkflowHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadWorkflowHistory();
  }, []);

  const loadWorkflowHistory = async () => {
    try {
      setLoading(true);
      const history = await getWorkflowHistory();
      setWorkflowHistory(history.slice(0, 5)); // Show last 5 workflows
    } catch (error) {
      console.error('Failed to load workflow history:', error);
      setWorkflowHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Upload Excel File',
      description: 'Upload your mapping Excel file to get started',
      icon: <UploadIcon sx={{ fontSize: 40 }} />,
      color: '#4CAF50',
      path: '/upload',
    },
    {
      title: 'Generate Mapping',
      description: 'Create PySpark transformations from your data',
      icon: <TransformIcon sx={{ fontSize: 40 }} />,
      color: '#2196F3',
      path: '/mapping',
    },
    {
      title: 'Agent Workflow',
      description: 'Run AI agents for comprehensive processing',
      icon: <AgentIcon sx={{ fontSize: 40 }} />,
      color: '#FF9800',
      path: '/agents',
    },
    {
      title: 'Validate Metadata',
      description: 'Validate table schemas and data quality',
      icon: <ValidateIcon sx={{ fontSize: 40 }} />,
      color: '#9C27B0',
      path: '/metadata',
    },
    {
      title: 'Generate Tests',
      description: 'Create comprehensive test suites',
      icon: <TestIcon sx={{ fontSize: 40 }} />,
      color: '#F44336',
      path: '/tests',
    },
  ];

  const stats = [
    { label: 'Total Workflows', value: workflowHistory.length, color: '#1976d2' },
    { label: 'Successful', value: workflowHistory.filter(w => w.status === 'completed').length, color: '#4CAF50' },
    { label: 'In Progress', value: workflowHistory.filter(w => w.status === 'in_progress').length, color: '#FF9800' },
    { label: 'Failed', value: workflowHistory.filter(w => w.status === 'failed').length, color: '#F44336' },
  ];

  return (
    <Container maxWidth="xl" className="fade-in">
      {/* Welcome Section */}
      <Box mb={4}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          🤖 Welcome to Agentic Mapping AI
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Intelligent data transformation and mapping platform powered by AI agents
        </Typography>
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3} mb={4}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ textAlign: 'center', height: '100%' }}>
              <CardContent>
                <Typography variant="h4" sx={{ color: stat.color, fontWeight: 'bold' }}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Quick Actions */}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        🚀 Quick Actions
      </Typography>
      
      <Grid container spacing={3} mb={4}>
        {quickActions.map((action, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card 
              sx={{ 
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
              onClick={() => navigate(action.path)}
            >
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Box sx={{ color: action.color, mb: 2 }}>
                  {action.icon}
                </Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                  {action.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {action.description}
                </Typography>
                <Button
                  variant="contained"
                  sx={{ 
                    mt: 2,
                    backgroundColor: action.color,
                    '&:hover': {
                      backgroundColor: action.color,
                      opacity: 0.8,
                    },
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(action.path);
                  }}
                >
                  Get Started
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Workflow History */}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        📊 Recent Workflow History
      </Typography>
      
      <Paper sx={{ p: 3 }}>
        {loading ? (
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Loading workflow history...
            </Typography>
            <LinearProgress />
          </Box>
        ) : workflowHistory.length > 0 ? (
          <Grid container spacing={2}>
            {workflowHistory.map((workflow, index) => (
              <Grid item xs={12} key={index}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    p: 2,
                    border: '1px solid #e0e0e0',
                    borderRadius: 1,
                    '&:hover': {
                      backgroundColor: '#f5f5f5',
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <TimelineIcon color="primary" />
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                        {workflow.workflow_type || 'Data Processing'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {workflow.created_at ? new Date(workflow.created_at).toLocaleString() : 'Unknown time'}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Chip
                    label={workflow.status || 'Unknown'}
                    color={
                      workflow.status === 'completed' ? 'success' :
                      workflow.status === 'in_progress' ? 'warning' :
                      workflow.status === 'failed' ? 'error' : 'default'
                    }
                    size="small"
                  />
                </Box>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Alert severity="info" sx={{ textAlign: 'center' }}>
            <Typography variant="body1">
              No workflows found. Start by uploading an Excel file or running an agent workflow!
            </Typography>
          </Alert>
        )}
      </Paper>

      {/* Getting Started Guide */}
      <Box mt={4}>
        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
            🎯 Getting Started:
          </Typography>
          <Typography variant="body2">
            1. Upload your Excel mapping file • 2. Configure mapping settings • 3. Run agent workflow • 4. Review generated code and tests
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default Dashboard;
