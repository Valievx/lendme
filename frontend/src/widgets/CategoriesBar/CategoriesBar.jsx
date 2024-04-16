// import React from 'react';
import './CategoriesBar.scss';
import { Button } from '../../shared/ui/Button/Button';
import { LinkIcons } from '../../shared/ui/Links/LinksIcons/LinkIcons';
import { Input } from '../../shared/ui/Input/Input';
import { Icon } from '../../shared/ui/Icon/Icon';

export const CategoriesBar = () => {
  return (
    <section className="categories-bar" aria-label="панель выбора категорий и поиска">
      <Button className="button__coral button__coral_categories">
      <Icon id="list-btn" className='svg'/>
        Все категории
      </Button>
      <div className="categories-bar__inner">
        <div className="categories-bar__input-box">
          <Input inputClass="input__search input__search_type_search" inputName="inputSearch" />
          <Button className="button__coral button__coral_search">Найти</Button>
        </div>
        <LinkIcons title="Город"  className="linkIconCategories" iconId="map-city" classIcon="svg" />
      </div>
    </section>
  );
};
