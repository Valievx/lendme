import * as Yup from 'yup';
import { EMAILREGEX } from './constants';

const validationSchemaAuthForms = Yup.object().shape({
	username: Yup.string()
		.matches(/^[A-Za-z]+$/, 'Имя должно состоять только из букв') // регулярное выражение для проверки на буквы
		.required('Обязательное поле'),
	email: Yup.string()
		.trim()
		.matches(EMAILREGEX, 'Введите верный формат email')
		.required('Обязательное поле'),
	password: Yup.string()
		.min(6, 'Пароль должен содержать минимум 6 символов')
		.required('Обязательное поле'),
	confirmPass: Yup.string()
		.oneOf([Yup.ref('password'), null], 'Пароли должны совпадать') // проверка на совпадение с паролем
		.required('Обязательное поле'),
});

const validationSchemaSearch = Yup.object().shape({
	search: Yup.string()
		.matches(/^[A-Za-z]+$/, 'Некорректный запрос')
		.required('Обязательное поле'),
});
export { validationSchemaAuthForms, validationSchemaSearch };
