import React, {useEffect} from 'react';
import '../App.css';
import {useNavigate} from "react-router-dom";
import {GameSettings} from "../services";

function HomePage() {
    const nav = useNavigate()
    const state = GameSettings
    useEffect(() => {
        console.log('update')
    }, [state])
    const onChange = (event) => {
        const target = event.target;
        const name = target.name;
        state[name] = parseInt(target.value)
        console.log(state)
        console.log(name)
    }
    const onSubmit = (event) => {
        event.preventDefault()
        // TODO: Request node and start game
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
                        onChange={onChange}/>
                </label>
                <br/>
                <label>
                    Enter the height:
                    <input
                        type="number"
                        min="4"
                        name="height"
                        value={state.height}
                        onChange={onChange}/>
                </label>
                <br/>
                <label>
                    Enter the mines amount:
                    <input
                        type="number"
                        min="1"
                        name="mines"
                        value={state.mines}
                        onChange={onChange}/>
                </label>
                <br/>
                <input type="submit"
                       value="Start playing!"/>
            </form>
        </div>
    )
}

export default HomePage