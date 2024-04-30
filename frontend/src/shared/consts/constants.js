const titlesLogin = ['Вход', 'Регистрация'];
const titlesPassword = ['Восстановление пароля'];

const EMAILREGEX = /\s*^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const NAMEREGEX = /^[а-яА-Яa-zA-Z]+$/;
const PHONEREGEX = /^\+7\d{10}$/;
const MINLENGTHNAME = 2;
const MINLENGTPASSWORD = 8;

const validationMessages = {
	name: 'Имя должно состоять только из букв',
	name_min: 'Имя должно быть больше одного символа',
	email: 'Введите корректный email',
	phone: 'Введите номер телефона в формате +7XXXXXXXXXX',
	date: 'Введите дату в формате гггг-мм-дд',
	confirmation_code: 'Некорректный код',
	current_password: 'Пароль должен содержать не менее 8 символов',
	re_password: 'Пароли должны совпадать',
	required: 'Обязательное поле',
	search: 'Некорректный запрос',
	emailOrPhone: 'Введите корректные данные',
};

export {
	titlesLogin,
	titlesPassword,
	validationMessages,
	EMAILREGEX,
	NAMEREGEX,
	PHONEREGEX,
	MINLENGTHNAME,
	MINLENGTPASSWORD,
};
