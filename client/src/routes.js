import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route  } from 'react-router-dom';
const FieldForm = lazy(() => import('./pages/homepage.tsx'));
const Load = lazy(() => import('./pages/load.js'));
const Game = lazy(() => import('./pages/game.js'));

const MyRoutes = () =>(
    <Router>
       <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/" element={<FieldForm />} />
        <Route path="/loading" element={<Load />} />
        <Route path='/game' element = {<Game />} />
      </Routes>
    </Suspense>
    </Router>
);


export default MyRoutes