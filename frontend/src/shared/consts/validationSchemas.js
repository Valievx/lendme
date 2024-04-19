import * as Yup from 'yup';

const validationSchemaLogin = Yup.object().shape({
  email: Yup.string().email('Неверный email').required('Обязательное поле'),
  password: Yup.string().min(6, 'Пароль должен содержать минимум 6 символов').required('Обязательное поле'),
});

export {validationSchemaLogin}