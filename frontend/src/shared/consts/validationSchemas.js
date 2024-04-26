import * as Yup from 'yup';
import { MINLENGTHNAME, MINLENGTPASSWORD, NAMEREGEX } from './constants';

const validationSchemaAuthForms = Yup.object().shape({
	username: Yup.string()
		.min(MINLENGTHNAME, 'Имя должно быть больше одного символа')
		.matches(NAMEREGEX, 'Имя должно состоять только из букв') // регулярное выражение для проверки на буквы
		.required('Обязательное поле'),
	email: Yup.string()
		.trim()
		.email('Введите верный формат email')
		.required('Обязательное поле'),
	password: Yup.string()
		.min(MINLENGTPASSWORD, 'Пароль должен содержать минимум 6 символов')
		.required('Обязательное поле'),
	confirmPass: Yup.string()
		.oneOf([Yup.ref('password'), null], 'Пароли должны совпадать') // проверка на совпадение с паролем
		.required('Обязательное поле'),
});

const validationSchemaSearch = Yup.object().shape({
	search: Yup.string()
		.matches(NAMEREGEX, 'Некорректный запрос')
		.required('Обязательное поле'),
});
export { validationSchemaAuthForms, validationSchemaSearch };
