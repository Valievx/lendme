import './Button.scss'

export const Button = (props) => {
  const { className, children, ...otherProps } = props;
  return (
    <button type="button" className={className} {...otherProps}>
      {children}
    </button>
  );
};
