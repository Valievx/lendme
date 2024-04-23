// import React from 'react';

import { InitialForm } from '../../../entities/InitialForm';
import { Button } from '../../../shared/ui/Button/Button';
import { Input } from '../../../shared/ui/Input/Input';
import useFormAndValidation from '../../../shared/libs/helpers/useFormAndValidation';
import { validationSchemaAuthForms } from '../../../shared/consts/validationSchemas';
import Checkbox from '../../../shared/ui/Checkbox/Checkbox';

export const RegistrationForm = ({ onTitleClick, onClosePopup }) => {
	const { form, errors, isFormValid, handleChange } = useFormAndValidation(
		{
			username: '',
			email: '',
			password: '',
			confirmPass: '',
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
				inputName="username"
				inputValue={form.username}
				placeholder="Ваше имя"
				inputLabelText="Ваше имя на сайте *"
				onChange={handleChange}
				inputError={errors.username}
			/>

			<Input
				inputClass="input__form"
				inputName="email"
				inputValue={form.email}
				placeholder="E-mail"
				inputLabelText="E-mail*"
				onChange={handleChange}
				inputError={errors.email}
			/>

			<Input
				inputClass="input__form"
				inputType="password"
				inputName="password"
				inputValue={form.password}
				placeholder="Введите пароль"
				inputLabelText="Пароль *"
				onChange={handleChange}
				inputError={errors.password}
			/>
			<Input
				inputClass="input__form"
				inputType="password"
				inputName="confirmPass"
				inputValue={form.confirmPass}
				placeholder="Введите пароль"
				inputLabelText="Подтвердитe пароль *"
				onChange={handleChange}
				inputError={errors.confirmPass}
			/>
			<Checkbox label="Запомнить меня" />
			<Button
				className="button__coral button__coral_forms"
				type="submit"
				disabled={!isFormValid}
			>
				Зарегистрироваться
			</Button>
			<a href="#" className="forms__link" onClick={() => onTitleClick(2)}>
				Забыли пароль?
			</a>
		</InitialForm>
	);
};
