// import React from 'react';
import './Input.scss';
export const Input = (props) => {
  const {
    inputClass,
    inputType = 'text',
    inputName,
    inputValue,
    inputError,
    ...otherProps
  } = props;

  return (
    <input
      className={`input ${inputClass} ${inputError ? 'input-error' : ''}`}
      type={inputType}
      name={inputName}
      value={inputValue || ''}
      onChange={()=>{}}
      {...otherProps}
    />
  );
};
