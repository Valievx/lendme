// import React from 'react';
import './CardProduct.scss';
import { CardItem } from '../../shared/ui/CardItem/CardItem';
import { LinkIcons } from '../../shared/ui/Links/LinksIcons/LinkIcons';
import { Button } from '../../shared/ui/Button/Button';

export const CardProduct = (props) => {
  const { data } = props;

  return (
    <div className="cardProduct">
      <CardItem  className="cardItem__product" data={data} />
      <div className="cardProduct__description">
        <div className="cardProduct__text-box">
          <p className="cardProduct__category">{data.category}</p>
          <p className="cardProduct__price">{data.price}</p>
          <p className="cardProduct__date">{data.date}</p>
        </div>
        <LinkIcons className="linkIconCity" title={data.location} icon={data.icon} />
      </div>
      <Button className="button__like button__like-product"/>
    </div>
  );
};
