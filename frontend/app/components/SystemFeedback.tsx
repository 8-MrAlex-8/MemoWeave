import React from 'react';

interface SystemFeedbackProps {
  message: string;
}

export function SystemFeedback({ message }: SystemFeedbackProps) {
  if (!message) return null;

  return (
    <div className="bg-[#F2F0FF] border border-[#CFC7EE] rounded-md px-4 py-2.5 text-[13px] text-[#4A3F7A] text-center animate-[fadeIn_0.3s_ease-in]">
      {message}
    </div>
  );
}
