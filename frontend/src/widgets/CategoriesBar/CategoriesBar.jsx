// import React from 'react';
import './CategoriesBar.scss';
import iconList from './icons/list-btn-icon.svg';
import iconCity from './icons/map-city-icon.svg';
import { Button } from '../../shared/ui/Button/Button';
import { LinkIcons } from '../../shared/ui/Links/LinksIcons/LinkIcons';
import { Input } from '../../shared/ui/Input/Input';

//  ДОБАВИТЬ В ИМПУТ ИКОНКУ ПОИСКА 
export const CategoriesBar = () => {
  return (
    <section className="categories" aria-label="панель выбора категорий и поиска">
      <Button className="button__coral button__coral_categories">
        <img src={iconList} alt="иконка категорий" />
        Все категории
      </Button>
      <div className="categories__inner">
        <div className="categories__input-box">
          <Input inputClass="input__search input__search_type_search" inputName="inputSearch" />
          <Button className="button__coral button__coral_search">Найти</Button>
        </div>

        <LinkIcons title="Город" icon={iconCity} className="linkIconCategories" />
      </div>
    </section>
  );
};
