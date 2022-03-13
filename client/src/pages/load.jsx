import '../App.css';
import React from 'react';
import {GameSettings, getNode, startGame, waitGame} from '../services'
import {useNavigate} from "react-router-dom";

function Load() {
    const state = GameSettings
    const nav = useNavigate()

    getNode(state, s => startGame(s, t => waitGame(t, k => nav('/game'))))

    return (
        <div>
            <h1>
                Loading...
            </h1>
            <h2>
                Your customized minefield:
            </h2>
            <h3>
                Width: {state['width']}
                <br/>
                Height: {state['height']}
                <br/>
                Mines: {state['mines']}
            </h3>
        </div>
    );
}

export default Load