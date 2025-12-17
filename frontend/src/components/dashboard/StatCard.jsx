import React from 'react';
import PropTypes from 'prop-types';

const StatCard = ({ label, value, icon, colorClass, bgClass }) => {
    return (
        <div className="bg-white p-4 rounded-2xl shadow-sm flex flex-col justify-center border border-gray-50 transition-transform active:scale-95 duration-200">
            <div className="flex items-start space-x-2 mb-2">
                <div className={`${bgClass} p-2 rounded-full ${colorClass}`}>
                    {icon}
                </div>
                <span className="text-gray-500 text-sm font-medium">{label}</span>
            </div>
            <p className="text-3xl font-bold text-gray-800 ml-1">{value}</p>
        </div>
    );
};

StatCard.propTypes = {
    label: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    icon: PropTypes.element.isRequired,
    colorClass: PropTypes.string,
    bgClass: PropTypes.string,
};

export default StatCard;
