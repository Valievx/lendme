import './Header.scss';
import HeaderInfoLinks from '../../shared/ui/HeaderInfoLinks/HeaderInfoLinks';
import { NavBar } from '../NavBar/NavBar';
import { Button } from '../../shared/ui/Button/Button';
import { LinkIcons } from '../../shared/ui/Links/LinksIcons/LinkIcons';
import profileLogo from '../../shared/assets/icons/login-profile-icon.svg';

export const Header = () => {
  return (
    <header className="header">
      <HeaderInfoLinks />
      <section className="header__main">
        <p className="header_logo">LendMe</p>
        <div className="header__main_box">
          <NavBar />
          <div className="header__login">
            <LinkIcons title="Вход и регистрация" icon={profileLogo} className="linkIconLogin"/>
            <Button className="button__coral">Разместить объявление</Button>
          </div>
        </div>
      </section>
    </header>
  );
};
