// import React from 'react';
import './CardItem.scss';
export const CardItem = (props) => {
  const { className, src, text } = props;

  return (
    <li className={`cartItem ${className}`}>
      <img className="cartItem__img" src={src} alt={text} />
     <p className="cartItem__text">{text}</p> 
    </li>
  );
};
