import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AlumniList, { Alumni } from '../components/AlumniList';
import { Container, Typography, CircularProgress, TextField } from '@mui/material';


const HomePage: React.FC = () => {
  const [alumni, setAlumni] = useState<Alumni[]>([]);
  const [filteredAlumni, setFilteredAlumni] = useState<Alumni[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    axios.get<Alumni[]>(`${process.env.NEXT_PUBLIC_API_BASE_URL}/alumni`)
      .then(response => {
        setAlumni(response.data);
        setFilteredAlumni(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching alumni data:", error);
        setLoading(false);
      });
  }, []);

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);

    if (!query) {
      setFilteredAlumni(alumni);
      return;
    }

    const filtered = alumni.filter(person => {
      const altNames = person.alt_names || [];
      return (
        person.name.toLowerCase().includes(query) ||
        altNames.some(name => name.toLowerCase().includes(query))
      );
    });

    setFilteredAlumni(filtered);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Alumni of Taras Shevchenko Kyiv National University
      </Typography>
      <TextField
        fullWidth
        variant="outlined"
        label="Search"
        value={searchQuery}
        onChange={handleSearch}
        sx={{ mb: 3 }}
      />
      {loading ? <CircularProgress /> : <AlumniList alumni={filteredAlumni} />}
    </Container>
  );
};

export default HomePage;
