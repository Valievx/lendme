import { InitialForm } from '../../../entities/InitialForm';
import { Input } from '../../../shared/ui/Input/Input';
import { Button } from '../../../shared/ui/Button/Button';
import Checkbox from '../../../shared/ui/Checkbox/Checkbox';
import useFormAndValidation from '../../../shared/libs/helpers/useFormAndValidation';
import { validationSchemaAuthForms } from '../../../shared/consts/validationSchemas';

export const LoginForms = ({ onTitleClick, onClosePopup }) => {
	const { form, errors, isFormValid, handleChange } = useFormAndValidation(
		{
			email: '',
			password: '',
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
				inputError={errors.email}
			/>
			<Input
				inputClass="input__form"
				inputType="password"
				inputValue={form.password}
				placeholder="Введите пароль"
				inputLabelText="Пароль*"
				inputName="password"
				onChange={handleChange}
				inputError={errors.password}
			/>
			<Checkbox label="Запомнить меня" />

			<Button
				className="button__coral button__coral_forms"
				type="submit"
				disabled={!isFormValid}
			>
				Войти
			</Button>
			<a href="#" className="loginForm__link" onClick={() => onTitleClick(2)}>
				Забыли пароль?
			</a>
		</InitialForm>
	);
};
