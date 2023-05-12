import React from "react";
import './styles/Input.css';

function Input(props) {
  return (
    <div className="input-container">
        <label>{ props.label }</label>
        <input type="text" value={ props.text } onChange={ props.onChange } placeholder={ props.placeholder } />
    </div>
  );
};

export default Input;