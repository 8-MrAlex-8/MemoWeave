import React from 'react';

interface CardProps {
  title?: string;
  tint?: string;
  children: React.ReactNode;
}

export function Card({ title, tint = '#F0EAFE', children }: CardProps) {
  return (
    <div className="bg-white border border-[#E4DDF5] rounded-lg overflow-hidden flex flex-col">
      {title && (
        <div 
          className="px-3.5 py-2 text-base font-semibold text-[#2D2640]"
          style={{ background: tint }}
        >
          {title}
        </div>
      )}
      <div className="flex-1 flex flex-col">
        {children}
      </div>
    </div>
  );
}
