import React, {Suspense, lazy} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

const HomePage = lazy(() => import('./pages/homepage.jsx'));
const Load = lazy(() => import('./pages/load.jsx'));
const Game = lazy(() => import('./pages/game.js'));

export const AppRoutes = () => (
    <Router>
        <Suspense fallback={<div>Loading...</div>}>
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/loading" element={<Load/>}/>
                <Route path='/game' element={<Game/>}/>
            </Routes>
        </Suspense>
    </Router>
);