% Code provided by Dr. Abdalla Nassar
% Used for "INVESTIGATION OF LASER-SUSTAINED PLASMA AND THE ROLE OF PLASMA 
% IN CARBON DIOXIDE LASER NITRIDING OF TITANIUM" 2012, PhD Thesis, 
% Pennsylvania State University

clear all;
Pre=101325;
PI=pi;
T=1e3:1e3:2e4;
Nh=Pre*(10^23)./(1.3.*T);
%if(T<30000)
Z_ratio=-2.3077E-29*(T.^7)+2.3474E-24*(T.^6)-8.8453E-20*(T.^5)+1.4851E-15*(T.^4)-9.843E-12*(T.^3)-1.2477E-8*(T.^2)+0.00047534.*T+3.7971;

saha_fac=Z_ratio.*(2.0./Nh).*1.68391E20.*((2.0*(PI).*T).^1.5).*exp(-1*15.6*1.6E-19./(1.3E-23.*T));
x=(sqrt(saha_fac.*saha_fac+saha_fac)-saha_fac);
x2 = (sqrt(saha_fac.*saha_fac+4.*saha_fac)-saha_fac)/2;
Ne=x.*Nh %in [m^-3]
% semilogy(T,Ne);
% hold on
% semilogy(T,Nh.*x2);
plot(T, Nh.*x2./Ne)