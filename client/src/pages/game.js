import { openSquare } from "../services";

function Game(props) {
    const state = props.settings
    const status = `There are ${state.mines} mines in the field`;

    const makeSquare = (x, y, value) => (
        <button className="square" style={{ width: 30, height: 30, display: 'inline-block', verticalAlign: 'top'}}
            onClick={() => value === -1 ? openSquare(x, y, state) : null} disabled={value !== -1}>
            {value === -1 ? "" : value.toString()}
        </button>
    )

    const makeRow = (rowData) => (
        <div className="board-row">
            {rowData}
        </div>
    )

    const makeBoard = (columnData) => (
        <div>
            <div className="status" style={{ textAlign: "center" }}>{status}</div>
            <div>{columnData}</div>
        </div>
    )


    const columns = []
    for (let i = 0; i < state.height; i++) {
        const rows = [];
        for (let j = 0; j < state.width; j++) {
            rows.push(makeSquare(j, i, state.field[i][j]))
        }
        columns.push(makeRow(rows))
    }


    return (
        <div className="game">
            <div className="game-board">
                {makeBoard(columns)}
            </div>
        </div>
    );
}

export default Game;