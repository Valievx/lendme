import './Button.scss';

export const Button = (props) => {
	const { className, children, type = 'button', ...otherProps } = props;
	return (
		<button className={`button ${className}`} type={type} tabIndex="0" {...otherProps}>
			{children}
		</button>
	);
};
