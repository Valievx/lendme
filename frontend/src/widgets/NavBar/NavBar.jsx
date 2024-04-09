import './NavBar.scss'
import { dataNavLinks } from '../../shared/lib/utils/dataNavLinks';
import { LinkIcons } from '../../shared/ui/Links/LinksIcons/LinkIcons';

export const NavBar = () => {
  return (
    <div className="navbar">
      {dataNavLinks.map((navLink) => (
        <LinkIcons key={navLink.id} title={navLink.title} icon={navLink.icon} className="linkIcon" />
      ))}
    </div>
  );
};
