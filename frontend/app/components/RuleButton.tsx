import React from 'react';

interface RuleButtonProps {
  title: string;
  description: string;
  selected: boolean;
  disabled: boolean;
  onClick: () => void;
}

export function RuleButton({ title, description, selected, disabled, onClick }: RuleButtonProps) {
  return (
    <div className="flex flex-col gap-2">
      <button
        className={`
          w-full rounded-xl px-3 py-3 text-[15px] font-semibold text-[#2D2640] transition-all
          ${selected 
            ? 'bg-[#EEE8FF] border-[3px] border-[#7D5FB5]' 
            : 'bg-white border-2 border-[#CFC7EE] hover:border-[#B8ACD8] hover:bg-[#FAFAFE]'
          }
          disabled:opacity-50 disabled:cursor-not-allowed
        `}
        onClick={onClick}
        disabled={disabled}
      >
        {title}
      </button>
      <p className="text-center text-[13px] text-[#4E4A63] leading-tight m-0">
        {description}
      </p>
    </div>
  );
}
