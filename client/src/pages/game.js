import React from "react";
import FieldForm from "./homepage";

const state = JSON.parse(window.localStorage.getItem('mine-settings'))
console.log(state)

class Square extends React.Component {
    render() {
      return (
        <button className="square"
        >
          {this.props.value}
        </button>
      );
    }
  }
  
  class Board extends React.Component {
    renderSquare(i) {
      return <Square value={i} />;
    }

    renderRow(fieldRow){
        return (
        <div className="board-row">
            {fieldRow}
        </div>)
    }

    render() {
      const status = `There are ${state["mines"]} mines in the field`;

      let field = []
      
        for (let i = 0; i < state["height"]; i++) {
            let fieldRow = [];
            for (var j = 0; j < state["width"]; j++) {
                fieldRow.push(this.renderSquare(0))
            }
            field.push(this.renderRow(fieldRow))
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
  }
  
  class Game extends React.Component {
    render() {
      return (
        <div className="game">
          <div className="game-board">
            <Board />
          </div>
          <div className="game-info">
            <div>{/* status */}</div>
            <ol>{/* TODO */}</ol>
          </div>
        </div>
      );
    }
  }

export default Game;