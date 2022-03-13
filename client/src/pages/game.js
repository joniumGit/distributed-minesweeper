function Game(props) {
    const state = props.settings
    const status = `There are ${state.mines} mines in the field`;

    const makeSquare = (value) => (
        <button className="square" style={{width: 50, height: 50}}>
            {value === -1 ? "" : value}
        </button>
    )

    const makeRow = (rowData) => (
        <div className="board-row">
            {rowData}
        </div>
    )

    const makeBoard = (columnData) => (
        <div style={{left: "50%", top: "50%", transform: "translate(-50%,-50%)", position: "absolute"}}>
            <div className="status" style={{textAlign: "center"}}>{status}</div>
            {columnData}
        </div>
    )


    const columns = []
    for (let i = 0; i < state.height; i++) {
        const rows = [];
        for (let j = 0; j < state.width; j++) {
            rows.push(makeSquare(" "))
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