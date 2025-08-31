import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';

const Compliance: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        규정 검토
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              규정 검사 결과
            </Typography>
            <Typography color="text.secondary">
              규정 검토 기능이 준비 중입니다.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Compliance;