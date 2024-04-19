// import React from 'react';
import './Input.scss';
export const Input = (props) => {
	const {
		inputClass,
		inputType = 'text',
		inputName,
		inputValue,
		inputError,
		inputInfo,
		inputLabelText,
		...otherProps
	} = props;

	return (
		<>
			{inputValue && (
				<label
					htmlFor={inputName}
					tabIndex="-1"
					className={`input__label ${inputError ? 'input__label-error' : ''}`}
				>
					{inputLabelText}
				</label>
			)}
			<input
				className={`input ${inputClass} ${inputError ? 'input-error' : ''}`}
				type={inputType}
				name={inputName}
				value={inputValue || ''}
				onChange={() => {}}
				{...otherProps}
			/>
			{inputError ? (
				<span className="input__text input__text_error">{inputError}</span>
			) : (
				<span className="input__text input__text_info">{inputInfo}</span>
			)}
		</>
	);
};
