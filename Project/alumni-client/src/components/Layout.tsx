import React from 'react';
import { AppBar, Toolbar, Typography, Button, Container, Link as MuiLink } from '@mui/material';
import NextLink from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <NextLink href="/" passHref legacyBehavior>
            <MuiLink color="inherit">
              Home
            </MuiLink>
          </NextLink>
        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 3 }}>{children}</Container>
    </>
  );
};

export default Layout;
