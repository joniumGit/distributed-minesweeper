import React from 'react';
import '../App.css';
import {useNavigate} from "react-router-dom";

function HomePage(props) {
    const nav = useNavigate()
    const state = props.settings

    const onSubmit = (event) => {
        event.preventDefault()
        nav('/loading')
    }

    return (
        <div>
            <h1>
                Welcome to Distributed Minesweeper!
            </h1>
            <h2>
                Please customize the game as instructed below.
            </h2>
            <form onSubmit={onSubmit}>
                <label>
                    Enter the width:
                    <input
                        type="number"
                        min='4'
                        name="width"
                        value={state.width}
                        onChange={state.setters.width}/>
                </label>
                <br/>
                <label>
                    Enter the height:
                    <input
                        type="number"
                        min="4"
                        name="height"
                        value={state.height}
                        onChange={state.setters.height}/>
                </label>
                <br/>
                <label>
                    Enter the mines amount:
                    <input
                        type="number"
                        min="1"
                        name="mines"
                        value={state.mines}
                        onChange={state.setters.mines}/>
                </label>
                <br/>
                <input type="submit"
                       value="Start playing!"/>
            </form>
        </div>
    )
}

export default HomePage