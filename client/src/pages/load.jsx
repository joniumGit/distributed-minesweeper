import React, {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import { start } from '../services';

function Load(props) {
    const state = props.settings
    const nav = useNavigate()

    useEffect(() => start(state, nav))
        
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