// import React from 'react';
import { cardItemsData } from '../../../shared/consts/cardItemsData';
import { CardItem } from '../../../shared/ui/CardItem/CardItem';
import { Button } from '../../../shared/ui/Button/Button';
import './Categories.scss';

export const Categories = () => {
  return (
    <section className="categories">
      <h2 className="categories__title">Выберите категорию</h2>
      <div className="categories__inner">
        <Button className="button__coral button__coral_slider button__coral_slider-left" />
        <ul className="categories__items">
          {cardItemsData.map((item) => (
            <CardItem key={item.id} src={item.src} text={item.text} className="categories__list" />
          ))}
        </ul>
        <Button className="button__coral button__coral_slider button__coral_slider-right" />
      </div>
    </section>
  );
};
