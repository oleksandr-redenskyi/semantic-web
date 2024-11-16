import React from 'react';
import NextLink from 'next/link';
import { List, ListItem, ListItemText, Paper, Link } from '@mui/material';

export interface Alumni {
    id: string;
    name: string;
    alt_names: string[];
}

interface AlumniListProps {
  alumni: Alumni[];
}

const AlumniList: React.FC<AlumniListProps> = ({ alumni }) => (
  <Paper elevation={3} sx={{ padding: 2 }}>
    <List>
      {alumni.map((person) => (
        <ListItem key={person.id}>
          <NextLink href={`/page/${encodeURIComponent(person.id)}`} passHref>
            <Link>
              <ListItemText primary={person.name} />
            </Link>
          </NextLink>
        </ListItem>
      ))}
    </List>
  </Paper>
);

export default AlumniList;
