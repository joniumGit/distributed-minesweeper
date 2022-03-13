import '../App.css';
import React, {useEffect} from 'react';
import {useNavigate} from "react-router-dom";

function Load(props) {
    const state = props.settings
    const nav = useNavigate()

    useEffect(() => {
        (async () => {
            await state.reserveNode()
            await state.startGame()
            await state.waitInit()
            nav('/game')
        })();
    })

    return (
        <div>
            <h1>
                Loading...
            </h1>
            <h2>
                Your customized minefield:
            </h2>
            <h3>
                Width: {state.width}
                <br/>
                Height: {state.height}
                <br/>
                Mines: {state.mines}
            </h3>
        </div>
    );
}

export default Load