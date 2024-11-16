import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import { Container, Typography, CircularProgress } from '@mui/material';
import PersonDetail from '../../components/PersonDetail';

interface PersonData {
  [key: string]: string;
}

const PersonPage: React.FC = () => {
  const router = useRouter();
  const { uri } = router.query;

  const [personData, setPersonData] = useState<PersonData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (uri) {
      axios.get<PersonData>(process.env.NEXT_PUBLIC_API_BASE_URL + `/page/${encodeURIComponent(uri as string)}`)
        .then(response => {
          setPersonData(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching person data:", error);
          setLoading(false);
        });
    }
  }, [uri]);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Details</Typography>
      {loading ? <CircularProgress /> : <PersonDetail personData={personData || {}} />}
    </Container>
  );
};

export default PersonPage;
