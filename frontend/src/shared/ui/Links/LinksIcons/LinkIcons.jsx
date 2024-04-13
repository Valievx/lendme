import './LinkIcons.scss';

export const LinkIcons = (props) => {
  const { title, icon, className = 'linkIcon' } = props;
  return (
    <div className={className}>
      <img src={icon} alt={title} />
      <span>{title}</span>
    </div>
  );
};
