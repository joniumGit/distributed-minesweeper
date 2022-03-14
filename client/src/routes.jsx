import React, {lazy, Suspense, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import {getAPI} from "./services";

const HomePage = lazy(() => import('./pages/homepage.jsx'));
const Load = lazy(() => import('./pages/load.jsx'));
const Game = lazy(() => import('./pages/game.js'));

function CenterDiv(props) {
    return (
        <div style={{left: "50%", top: "50%", transform: "translate(-50%,-50%)", position: "absolute"}}>
            {props.children}
        </div>
    )
}

export const AppRoutes = () => {
    const [state, setState] = useState({
        width: 8,
        height: 8,
        mines: 10
    })
    const settings = getAPI(state, {
        width: (e) => setState({...state, width: parseInt(e.target.value)}),
        height: (e) => setState({...state, height: parseInt(e.target.value)}),
        mines: (e) => setState({...state, mines: parseInt(e.target.value)}),
        update: (o) => setState({...o})
    })

    return (
        <CenterDiv>
            <Router>
                <Suspense fallback={<div>Loading...</div>}>
                    <Routes>
                        <Route path="/" element={<HomePage settings={settings}/>}/>
                        <Route path="/loading" element={<Load settings={settings}/>}/>
                        <Route path='/game' element={<Game settings={settings}/>}/>
                    </Routes>
                </Suspense>
            </Router>
        </CenterDiv>
    )
}