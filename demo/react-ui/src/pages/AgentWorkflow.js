import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Alert,
  LinearProgress,
  Chip,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  CheckCircle as CompleteIcon,
  Error as ErrorIcon,
  Schedule as PendingIcon,
} from '@mui/icons-material';
import { startAgentWorkflow, getAgentStatus } from '../utils/api';

const AgentWorkflow = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [workflowRunning, setWorkflowRunning] = useState(false);
  const [workflowResult, setWorkflowResult] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState({
    workflowType: 'full_mapping_pipeline',
    excelFile: 'ebs_IM_account_DATAhub_mapping_v8.0.xlsx',
    targetFormat: 'pyspark',
    includeTests: true,
    includeValidation: true,
  });

  const workflowSteps = [
    {
      label: 'Metadata Extraction',
      description: 'Extract and analyze Excel mapping data',
      agent: 'MetadataValidator',
    },
    {
      label: 'Code Generation',
      description: 'Generate PySpark transformation code',
      agent: 'CodeGenerator',
    },
    {
      label: 'Test Generation',
      description: 'Create comprehensive test suites',
      agent: 'TestGenerator',
    },
    {
      label: 'Validation & Quality Check',
      description: 'Validate generated code and tests',
      agent: 'MetadataValidator',
    },
  ];

  useEffect(() => {
    let interval;
    if (workflowRunning && taskId) {
      interval = setInterval(checkStatus, 2000);
    }
    return () => clearInterval(interval);
  }, [workflowRunning, taskId]);

  const checkStatus = async () => {
    if (!taskId) return;

    try {
      const status = await getAgentStatus(taskId);
      
      if (status.status === 'completed') {
        setWorkflowRunning(false);
        setWorkflowResult(status);
        setActiveStep(workflowSteps.length);
      } else if (status.status === 'failed') {
        setWorkflowRunning(false);
        setError(status.error || 'Workflow failed');
      } else if (status.current_step !== undefined) {
        setActiveStep(status.current_step);
      }
    } catch (err) {
      console.error('Status check failed:', err);
    }
  };

  const startWorkflow = async () => {
    setWorkflowRunning(true);
    setError(null);
    setActiveStep(0);
    setWorkflowResult(null);

    try {
      const request = {
        excel_file: config.excelFile,
        workflow_type: config.workflowType,
        options: {
          target_format: config.targetFormat,
          include_tests: config.includeTests,
          include_validation: config.includeValidation,
        },
      };

      const result = await startAgentWorkflow(config.workflowType, request);
      setTaskId(result.task_id);
    } catch (err) {
      setWorkflowRunning(false);
      setError(err.response?.data?.detail || err.message || 'Failed to start workflow');
    }
  };

  const stopWorkflow = () => {
    setWorkflowRunning(false);
    setTaskId(null);
    setActiveStep(0);
  };

  const getStepIcon = (index) => {
    if (index < activeStep) {
      return <CompleteIcon color="success" />;
    } else if (index === activeStep && workflowRunning) {
      return <PendingIcon color="primary" />;
    } else if (error) {
      return <ErrorIcon color="error" />;
    }
    return null;
  };

  return (
    <Container maxWidth="lg" className="fade-in">
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        🤖 Agent Workflow Orchestration
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom sx={{ mb: 4 }}>
        Run AI agents to process your mapping data end-to-end
      </Typography>

      <Grid container spacing={3}>
        {/* Configuration Panel */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ⚙️ Workflow Configuration
              </Typography>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Workflow Type</InputLabel>
                  <Select
                    value={config.workflowType}
                    onChange={(e) => setConfig({ ...config, workflowType: e.target.value })}
                    disabled={workflowRunning}
                  >
                    <MenuItem value="full_mapping_pipeline">Full Mapping Pipeline</MenuItem>
                    <MenuItem value="code_generation_only">Code Generation Only</MenuItem>
                    <MenuItem value="test_generation_only">Test Generation Only</MenuItem>
                    <MenuItem value="validation_only">Validation Only</MenuItem>
                  </Select>
                </FormControl>

                <TextField
                  label="Excel Filename"
                  value={config.excelFile}
                  onChange={(e) => setConfig({ ...config, excelFile: e.target.value })}
                  disabled={workflowRunning}
                  fullWidth
                />

                <FormControl fullWidth>
                  <InputLabel>Target Format</InputLabel>
                  <Select
                    value={config.targetFormat}
                    onChange={(e) => setConfig({ ...config, targetFormat: e.target.value })}
                    disabled={workflowRunning}
                  >
                    <MenuItem value="pyspark">PySpark</MenuItem>
                    <MenuItem value="sql">SQL</MenuItem>
                    <MenuItem value="python">Python</MenuItem>
                  </Select>
                </FormControl>

                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label="Include Tests"
                    color={config.includeTests ? "success" : "default"}
                    clickable
                    onClick={() => setConfig({ ...config, includeTests: !config.includeTests })}
                    disabled={workflowRunning}
                  />
                  <Chip
                    label="Include Validation"
                    color={config.includeValidation ? "success" : "default"}
                    clickable
                    onClick={() => setConfig({ ...config, includeValidation: !config.includeValidation })}
                    disabled={workflowRunning}
                  />
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    startIcon={<PlayIcon />}
                    onClick={startWorkflow}
                    disabled={workflowRunning}
                    fullWidth
                  >
                    Start Workflow
                  </Button>
                  {workflowRunning && (
                    <Button
                      variant="outlined"
                      startIcon={<StopIcon />}
                      onClick={stopWorkflow}
                      color="error"
                    >
                      Stop
                    </Button>
                  )}
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Current Status */}
          {workflowRunning && (
            <Card sx={{ mt: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📊 Current Status
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <Chip label="Running" color="warning" size="small" />
                  <Typography variant="body2">
                    Task ID: {taskId}
                  </Typography>
                </Box>
                <LinearProgress />
              </CardContent>
            </Card>
          )}
        </Grid>

        {/* Workflow Steps */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              🔄 Workflow Progress
            </Typography>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <Stepper activeStep={activeStep} orientation="vertical">
              {workflowSteps.map((step, index) => (
                <Step key={index}>
                  <StepLabel 
                    icon={getStepIcon(index)}
                    optional={
                      <Typography variant="caption" color="text.secondary">
                        Agent: {step.agent}
                      </Typography>
                    }
                  >
                    {step.label}
                  </StepLabel>
                  <StepContent>
                    <Typography variant="body2" color="text.secondary">
                      {step.description}
                    </Typography>
                    {index === activeStep && workflowRunning && (
                      <Box sx={{ mt: 1 }}>
                        <LinearProgress size="small" />
                        <Typography variant="caption" color="text.secondary">
                          Processing...
                        </Typography>
                      </Box>
                    )}
                  </StepContent>
                </Step>
              ))}
            </Stepper>

            {/* Results */}
            {workflowResult && (
              <Box sx={{ mt: 3 }}>
                <Alert severity="success" sx={{ mb: 2 }}>
                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                    ✅ Workflow Completed Successfully!
                  </Typography>
                </Alert>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Card variant="outlined">
                      <CardContent sx={{ textAlign: 'center' }}>
                        <Typography variant="h4" color="primary">
                          {workflowResult.generated_files || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Files Generated
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Card variant="outlined">
                      <CardContent sx={{ textAlign: 'center' }}>
                        <Typography variant="h4" color="success.main">
                          {workflowResult.test_cases || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Test Cases Created
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>

                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={() => window.location.reload()}
                  sx={{ mt: 2 }}
                >
                  Start New Workflow
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Help Section */}
      <Box sx={{ mt: 4 }}>
        <Alert severity="info">
          <Typography variant="body2" component="div">
            <strong>🎯 Workflow Types:</strong>
            <ul>
              <li><strong>Full Pipeline:</strong> Complete end-to-end processing with all agents</li>
              <li><strong>Code Generation:</strong> Generate PySpark transformations only</li>
              <li><strong>Test Generation:</strong> Create test suites for existing code</li>
              <li><strong>Validation:</strong> Validate metadata and data quality</li>
            </ul>
          </Typography>
        </Alert>
      </Box>
    </Container>
  );
};

export default AgentWorkflow;
