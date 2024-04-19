import './LoginForms.scss';
import { useState } from 'react';
import { InitialForm } from '../../../entities/InitialForm';
import { Popup } from '../../../shared/ui/Popup/Popup';
import { Input } from '../../../shared/ui/Input/Input';
import { Button } from '../../../shared/ui/Button/Button';
import SwiperSubtitle from '../../../shared/ui/SwiperSubtitle/SwiperSubtitle';
import { RegisterSocialLinks } from '../../../entities/RegisterSocialLinks';
import { socialLinksIcons } from '../../../shared/consts/socialLinksIcons';
import { titlesLogin } from '../../../shared/consts/constants';
import useFormAndValidation from '../../../shared/libs/helpers/useFormAndValidation';
import { validationSchemaLogin } from '../../../shared/consts/validationSchemas';

export const LoginForms = (props) => {
  const { isOpenPopup, onClosePopup } = props;
  const [activeIndex, setActiveIndex] = useState(0);

  const { form, errors, isFormValid, handleChange, resetForm } = useFormAndValidation(
    {
      email: '',
      password: '',
    },
    validationSchemaLogin,
  );

  const handleTitleClick = (index) => {
    setActiveIndex(index);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    resetForm();
  };

  return (
    <Popup isOpen={isOpenPopup} btnCls="button__close">
      <SwiperSubtitle
        titles={titlesLogin}
        activeIndex={activeIndex}
        OnTitleClick={handleTitleClick}
      />
      <InitialForm formClass="loginForms" onSubmit={handleSubmit}>
        <Input
          className="input__form"
          inputName="email"
          inputValue={form.email}
          placeholder="E-mail"
          inputLabelText="E-mail*"
          onChange={handleChange}
          inputError={errors.email}
        />
        <Input
          className="input__form"
          inputType="password"
          inputValue={form.password}
          placeholder="Введите пароль"
          inputLabelText="Пароль*"
          inputName="password"
          onChange={handleChange}
          inputError={errors.password}
        />
        <div>
          <input className="input__form" type="checkbox" name="checkbox" />
          <span>Запомнить меня</span>
        </div>

        <Button
          className="button__coral button__coral_forms"
          type="submit"
          onClick={onClosePopup}
          disabled={!isFormValid}>
          Войти
        </Button>
        <a href="#" className="loginForm__link">
          Забыли пароль?
        </a>
      </InitialForm>
      <RegisterSocialLinks data={socialLinksIcons} />
    </Popup>
  );
};
