import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';

const Schedule: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        일정 관리
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              일정 캘린더
            </Typography>
            <Typography color="text.secondary">
              일정 관리 기능이 준비 중입니다.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Schedule;