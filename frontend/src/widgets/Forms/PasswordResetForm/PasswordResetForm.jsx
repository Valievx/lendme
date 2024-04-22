// import React from 'react';

import { InitialForm } from '../../../entities/InitialForm';
import { validationSchemaAuthForms } from '../../../shared/consts/validationSchemas';
import useFormAndValidation from '../../../shared/libs/helpers/useFormAndValidation';
import { Input } from '../../../shared/ui/Input/Input';
// import './PasswordResetForm.scss';
import { Button } from '../../../shared/ui/Button/Button';
import usePopupOpen from '../../../shared/libs/helpers/usePopupOpen';

export const PasswordResetForm = ({ onTitleClick }) => {
	const { handleClosePopup } = usePopupOpen();
	const { form, errors, isFormValid, handleChange, handleSubmit } =
		useFormAndValidation(
			{
				email: '',
			},
			validationSchemaAuthForms
		);

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
				onClick={handleClosePopup}
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
