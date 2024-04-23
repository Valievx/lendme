// import React from 'react';

import { InitialForm } from '../../../entities/InitialForm';
import { validationSchemaAuthForms } from '../../../shared/consts/validationSchemas';
import useFormAndValidation from '../../../shared/libs/helpers/useFormAndValidation';
import { Input } from '../../../shared/ui/Input/Input';
// import './PasswordResetForm.scss';
import { Button } from '../../../shared/ui/Button/Button';

export const PasswordResetForm = ({ onTitleClick, onClosePopup }) => {
	const { form, errors, handleChange, isFormValid } = useFormAndValidation(
		{
			email: '',
		},
		validationSchemaAuthForms
	);

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log(form);
		onClosePopup();
	};

	return (
		<InitialForm formClass="forms" onSubmit={handleSubmit}>
			<Input
				inputClass="input__form"
				inputName="email"
				inputValue={form.email}
				placeholder="E-mail"
				inputLabelText="E-mail*"
				onChange={handleChange}
				inputInfo="Введите ваш E-mail указанный при регистрации. Мы отправим на него временный пароль"
				inputError={errors.email}
			/>

			<Button
				className="button__coral button__coral_forms"
				type="submit"
				disabled={!isFormValid}
			>
				Отправить пароль
			</Button>
			<a href="#" className="loginForm__link" onClick={() => onTitleClick(0)}>
				Назад
			</a>
		</InitialForm>
	);
};
