import { useEffect, useState } from "react";

// кастомный хук валидации 
const useFormAndValidation = (initialState,validationSchema ) => {
  const [form, setForm] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [isActiveInput, setIsActiveInput] = useState({});

   // проверяет, есть ли значения в объекте
  const hasValues = (val) => !Object.values(val).some((value) => value === "");

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
    setErrors(null)
  };

  const hardChangeIsFormValid = (boolean) => {
    setIsFormValid(boolean);
  };

  const handleChange = (evt) => {
    const input = evt.target;

    setForm((prevState) => ({
      ...prevState,
      [input.name]: input.value,
    }));

    validationSchema.validateAt(input.name, form)
      .then(() => {
        setErrors((prevState) => ({
          ...prevState,
          [input.name]: "",
        }));
      })
      .catch((error) => {
        setIsFormValid(false)
        setErrors((prevState) => ({
          ...prevState,
          [input.name]: error.message,
        }));
      });
  };

  const handleSelectChange = (selectedObj) => {
    setForm((prevState) => ({
      ...prevState,
      ...selectedObj,
    }));
  };

  useEffect(() => {
    setIsFormValid(hasValues(form));
  }, [form]);

  return {
    form,
    setForm,
    errors,
    isFormValid,
    handleChange,
    handleSelectChange,
    resetForm,
    hardChangeIsFormValid,
    handleFocus,
    handleBlur,
    updateFormInput,
    isActiveInput,
  };
};

export default useFormAndValidation;