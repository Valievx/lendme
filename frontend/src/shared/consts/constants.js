const titlesLogin = ['Вход', 'Регистрация'];
const titlesPassword = ['Восстановление пароля'];

const EMAILREGEX = /\s*^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const NAMEREGEX = /^[а-яА-Яa-zA-Z]+$/;
const MINLENGTHNAME = 2;
const MINLENGTPASSWORD = 2;

export {
	titlesLogin,
	titlesPassword,
	EMAILREGEX,
	NAMEREGEX,
	MINLENGTHNAME,
	MINLENGTPASSWORD,
};
