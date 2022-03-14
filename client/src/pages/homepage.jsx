import React from 'react';
import {useNavigate} from "react-router-dom";

function NumberInput(props) {
    return (
        <label style={{textAlign: "left", display: "block"}}>
            {props.text}
            <input
                type="number"
                min={props.min}
                max={props.max}
                name="width"
                defaultValue={props.value}
                onChange={props.onChange}
            />
        </label>
    )
}

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
                Input Game Settings:
            </h2>
            <div>
                <form onSubmit={onSubmit}>
                    <NumberInput
                        text={'Width:'}
                        min={4}
                        max={32}
                        value={state.width}
                        onChange={state.setters.width}
                    />
                    <NumberInput
                        text={'Height:'}
                        min={4}
                        max={32}
                        value={state.height}
                        onChange={state.setters.height}
                    />
                    <NumberInput
                        text={'Mines:'}
                        min={1}
                        max={961}
                        value={state.mines}
                        onChange={state.setters.mines}
                    />
                    <label>
                        {''}
                        <input type="submit" value="Start!"/>
                    </label>
                </form>
            </div>
        </div>
    )
}

export default HomePage