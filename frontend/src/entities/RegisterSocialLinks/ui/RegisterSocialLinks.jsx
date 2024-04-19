// import React from 'react';
import { Icon } from '../../../shared/ui/Icon/Icon';
import './RegisterSocialLinks.scss';

export const RegisterSocialLinks = ({ data }) => {
	return (
		<div className="social-links">
			<p className="social-links__header">Или войдите с помощью соц. сетей</p>
			<div className="social-links__list">
				{data.map((item) => (
					<a className="social-links__link" key={item.id}>
						<Icon className="svg-social_link" id={item.iconId} />
					</a>
				))}
			</div>
			<p className="social-links__info">
				Регистрируясь, вы принимаете{' '}
				<a href="" className="social-links__link social-links__link-rules">
					правила и условия
				</a>
			</p>
		</div>
	);
};
