import React from 'react';
import { Paper, List, ListItem, ListItemText, Typography, Box } from '@mui/material';

interface PersonDetailProps {
  personData: { [key: string]: string | string[] };
}

const PersonDetail: React.FC<PersonDetailProps> = ({ personData }) => {
  if (!personData || Object.keys(personData).length === 0) {
    return <Typography>No data available for this person.</Typography>;
  }

  // Extract thumbnail field if present
  const { thumbnail, ...filteredData } = personData;
  const thumbnailStr = Array.isArray(thumbnail) ? thumbnail[0] : thumbnail;

  return (
    <Paper elevation={3} sx={{ padding: 2 }}>
      {thumbnail && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <img
            src={thumbnailStr}
            alt="Person Thumbnail"
            style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px' }}
          />
        </Box>
      )}
      <List>
        {Object.entries(filteredData).map(([key, value]) => (
          <ListItem key={key} sx={{ display: 'block' }}>
            <ListItemText
              primary={`${key.replace(/_/g, ' ')}:`}
              secondary={
                Array.isArray(value) ? (
                  <ul style={{ paddingLeft: 20, margin: 0 }}>
                    {value.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  value
                )
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default PersonDetail;
