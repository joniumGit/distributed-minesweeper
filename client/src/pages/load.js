import '../App.css';
import FieldForm, { globalState } from './homepage';
import React from 'react';
import { getNode, startGame, waitGame } from './services'

function Load() {
    const state = JSON.parse(window.localStorage.getItem('mine-settings'))

    getNode(state, s => startGame(s, t => waitGame(t, k => {
        window.localStorage.setItem('mine-settings', JSON.stringify(k));
        window.location.href='/game'
    })))



    return (

        <div >
            <h1>
                Loading...
            </h1>
            <h2>
                Your customized minefield:
            </h2>
            <h3>
                Width: {state['width']}
                <br></br>
                Height: {state['height']}
                <br></br>
                Mines: {state['mines']}
            </h3>

        </div>
    );
}

export default Load