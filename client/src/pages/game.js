import {GameSettings} from "../services";


function Square(props) {
    return (
        <button className="square">
            {props.value}
        </button>
    );
}


function Board() {
    const state = GameSettings
    const status = `There are ${state["mines"]} mines in the field`;
    const square = i => <Square value={i}/>
    const row = (rowData) => (
        <div className="board-row">
            {rowData}
        </div>
    )
    let field = []
    for (let i = 0; i < state.height; i++) {
        let fieldRow = [];
        for (var j = 0; j < state.width; j++) {
            fieldRow.push(square(" "))
        }
        field.push(row(fieldRow))
    }
    return (
        <div>
            <div className="status">{status}</div>
            <div>
                {field}
            </div>
        </div>
    );
}

function Game() {
    return (
        <div className="game">
            <div className="game-board">
                <Board/>
            </div>
            <div className="game-info">
                <div>{/* status */}</div>
                <ol>{/* TODO */}</ol>
            </div>
        </div>
    );
}

export default Game;