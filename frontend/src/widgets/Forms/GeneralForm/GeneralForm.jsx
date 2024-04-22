// import React from 'react';

import { useState } from 'react';

import './GeneralForm.scss';
import { RegisterSocialLinks } from '../../../entities/RegisterSocialLinks';
import { titlesLogin, titlesPassword } from '../../../shared/consts/constants';
import { Popup } from '../../../shared/ui/Popup/Popup';
import SwiperSubtitle from '../../../shared/ui/SwiperSubtitle/SwiperSubtitle';
import { socialLinksIcons } from '../../../shared/consts/socialLinksIcons';
import { LoginForms, RegistrationForm, PasswordResetForm } from '../';

// import './GeneralForm.scss';
export const GeneralForm = (props) => {
	let formComponent = null;
	let titlesForm = [];
	const { isOpenPopup } = props;
	const [activeIndex, setActiveIndex] = useState(0);

	const handleTitleClick = (index) => {
		setActiveIndex(index);
	};

	switch (activeIndex) {
		case 0:
			titlesForm = titlesLogin;
			formComponent = <LoginForms onTitleClick={handleTitleClick} />;
			break;
		case 1:
			titlesForm = titlesLogin;
			formComponent = <RegistrationForm onTitleClick={handleTitleClick} />;
			break;
		case 2:
			titlesForm = titlesPassword;
			formComponent = <PasswordResetForm onTitleClick={handleTitleClick} />;
			break;
		default:
			formComponent = null;
			break;
	}

	return (
		<Popup isOpen={isOpenPopup} btnCls="button__close">
			<SwiperSubtitle
				titles={titlesForm}
				activeIndex={activeIndex}
				OnTitleClick={handleTitleClick}
			/>
			{formComponent}
			<RegisterSocialLinks data={socialLinksIcons} />
		</Popup>
	);
};
