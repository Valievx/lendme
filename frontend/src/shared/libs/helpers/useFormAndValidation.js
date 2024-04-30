import { useEffect, useState } from "react";
import { EMAILREGEX } from "../../consts/constants";

// кастомный хук валидации
const useFormAndValidation = (initialState, validationSchema) => {
  const [form, setForm] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [isActiveInput, setIsActiveInput] = useState({});
  const [inputType, setInputType] = useState("email");

  const handleFocus = (evt) => {
    setIsActiveInput(evt.target);
    const input = evt.target;
    setForm({
      ...form,
      activeInput: input.name,
    });
  };

  const handleBlur = () => {
    setForm({
      ...form,
      activeInput: "",
    });
  };

  // обновляет значения полей формы
  const updateFormInput = (data) => {
    setForm((prevForm) => ({
      ...prevForm,
      ...data,
    }));
  };

  // сброс формы
  const resetForm = () => {
    setForm(initialState);
    setErrors(null);
  };

  const handleChange = (evt) => {
    const input = evt.target;

    setForm((prevState) => ({
      ...prevState,
      [input.name]: input.value,
    }));

    validationSchema
      .validateAt(input.name, form)
      .then(() => {
        setErrors((prevState) => ({
          ...prevState,
          [input.name]: "",
        }));
      })
      .catch((error) => {
        setIsFormValid(false);
        setErrors((prevState) => ({
          ...prevState,
          [input.name]: error.message,
        }));
      });
  };

  const handleInputChangeEmail = (e) => {
    const { value } = e.target;
    setInputType(EMAILREGEX.test(value) ? "email" : "tel");
    handleChange(e);
  };

  const handleSelectChange = (selectedObj) => {
    setForm((prevState) => ({
      ...prevState,
      ...selectedObj,
    }));
  };

  useEffect(() => {
    const isValid = Object.values(form).every((value) => value !== "") && !Object.values(errors).some((value) => value !== "");
    setIsFormValid(isValid);
  }, [form, errors]);

  return {
    form,
    setForm,
    errors,
    isFormValid,
    inputType,
    handleChange,
    handleInputChangeEmail,
    handleSelectChange,
    resetForm,
    handleFocus,
    handleBlur,
    updateFormInput,
    isActiveInput,
  };
};

export default useFormAndValidation;
