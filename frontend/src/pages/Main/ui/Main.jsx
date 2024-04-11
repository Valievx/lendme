// import React from 'react';
import { Categories } from '../../../entities/Categories/ui';
import { MainPageInfo } from '../../../widgets/MainPageInfo/MainPageInfo';
import './Main.scss';
export const Main = () => {
  
  return (
    <main className='main'>
      <MainPageInfo/>
      <Categories/>
    </main>
  );
};
