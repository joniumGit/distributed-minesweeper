import { url } from 'inspector';
import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

class FieldForm extends React.Component<any, any, any>{
  constructor(props: any) {
    super(props);
    this.state = {
      width: 4,
      height: 4,
      mines: 2
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange(event: any) {
    const target = event.target;
    const name = target.name;

    this.setState(
      {
        [name]: parseInt(target.value)
      });
  }

  handleSubmit = (e: any) => {
    e.preventDefault();

    // console.log(globalState);
    // this.props.history.push('/loading')
    window.localStorage.setItem('mine-settings', JSON.stringify({
      width: this.state['width'],
      height: this.state['height'],
      mines: this.state['mines']
    }));
    window.location.href = '/game';
  }
  render() {
    return (
      <div>
        <h1>
          Welcome to Distributed Minesweeper!
        </h1>
        <h2>
          Please customize the game as instructed below.
        </h2>
        <form
          onSubmit={this.handleSubmit}
        >
          <label>
            Enter the width:
            <input
              type="number"
              min='4'
              name="width"
              value={this.state.width}
              onChange={this.handleChange} />
          </label>
          <br />
          <label>
            Enter the height:
            <input
              type="number"
              min="4"
              name="height"
              value={this.state.height}
              onChange={this.handleChange} />
          </label>
          <br />
          <label>
            Enter the mines amount:
            <input
              type="number"
              min="1"
              name="mines"
              value={this.state.mines}
              onChange={this.handleChange} />
          </label>
          <br />
          <input type="submit"
            value="Start playing!" />
        </form>

      </div>

    )
  }

}

export default FieldForm;
